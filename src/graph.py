from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph
from config import settings
from src import prompts
import pandas as pd
import ast
from pathlib import Path
from typing import TypedDict
from pydantic import BaseModel
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)
from langchain_core.prompts import ChatPromptTemplate


TEST_DATA_PATH = Path(__file__).parent.parent / "data/Superstore.xlsx"

# define model to use
model = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0,
)

# define tool(s) that are available to use
tavily = TavilySearch(
    max_results=settings.MAX_SEARCH_RESULTS_PER_QUESTION,
    topic="general",
)


# define main state object
class AgentState(TypedDict):
    initial_request: str
    search_queries: list[str]
    search_results: list[str]
    insights_summary: str
    final_report: str


# define structured output formats
class SearchQueries(BaseModel):
    queries: list[str]


# define graph nodes
def query_generator_node(state: AgentState):
    queries = model.with_structured_output(SearchQueries).invoke(
        [
            SystemMessage(content=prompts.QUERY_PLANNER_PROMPT),
            HumanMessage(content=state["initial_request"]),
        ]
    )
    return {"search_queries": queries.queries}


def search_executor_node(state: AgentState):
    results = []
    for q in state["search_queries"]:
        response = tavily.invoke({"query": q})
        for r in response["results"]:
            results.append(r["content"])
    return {"search_results": results}


def data_summarizer_node(state: AgentState):
    df = pd.read_excel(TEST_DATA_PATH)
    initial_request = state["initial_request"]

    # Step 1: Extract category values
    all_categories = df["Category"].dropna().unique().tolist()
    all_subcategories = df["Sub-Category"].dropna().unique().tolist()

    # Step 2: Use LLM to map prompt to subcategories
    category_prompt = ChatPromptTemplate.from_template(
        """
    You are helping analyze a sales dataset. The dataset includes:

    Main Categories: {categories}
    Sub-Categories: {subcategories}

    Given this campaign prompt:
    "{initial_request}"

    Return a dedupped Python list of relevant Sub-Categories that match the prompt.
    Example: ["Binders", "Art", "Appliances"]
    """.strip()
    )

    messages = category_prompt.format_messages(
        categories=all_categories,
        subcategories=all_subcategories,
        initial_request=initial_request,
    )
    response = model.invoke(messages).content

    try:
        matched_subcategories = ast.literal_eval(response)
        if not isinstance(matched_subcategories, list):
            raise ValueError("Parsed response is not a list.")
    except Exception:
        return {"insights_summary": f"LLM response could not be parsed:\n{response}"}

    if not matched_subcategories:
        return {"insights_summary": "No relevant sub-categories found by the LLM."}

    # Step 3: Filter data
    df_filtered = df[df["Sub-Category"].isin(matched_subcategories)].copy()
    df_filtered["Order_Date"] = pd.to_datetime(df_filtered["Order_Date"])
    df_filtered["year"] = df_filtered["Order_Date"].dt.year

    # Step 4: Identify the latest two years in the dataset
    latest_years = sorted(df_filtered["year"].dropna().unique())[-2:]
    if len(latest_years) < 2:
        return {"insights_summary": "Not enough years of data for YoY comparison."}

    year_new, year_old = latest_years[1], latest_years[0]

    # Step 5: YoY aggregation
    grouped = (
        df_filtered.groupby(["Sub-Category", "Region", "year"])
        .agg({"Sales": "sum", "Profit": "sum"})
        .reset_index()
    )

    df_new = grouped[grouped["year"] == year_new].set_index(["Sub-Category", "Region"])
    df_old = grouped[grouped["year"] == year_old].set_index(["Sub-Category", "Region"])

    yoy = df_new.join(
        df_old, lsuffix=f"_{year_new}", rsuffix=f"_{year_old}", how="inner"
    )
    yoy["sales_yoy"] = (
        (yoy[f"Sales_{year_new}"] - yoy[f"Sales_{year_old}"]) / yoy[f"Sales_{year_old}"]
    ) * 100
    yoy["profit_yoy"] = (
        (yoy[f"Profit_{year_new}"] - yoy[f"Profit_{year_old}"])
        / yoy[f"Profit_{year_old}"]
    ) * 100
    yoy.reset_index(inplace=True)

    # Step 6: Generate insight summary with LLM
    summary_prompt = ChatPromptTemplate.from_template(
        """
    You are a BI analyst. Summarize the following YoY data in clear bullet points.
    Focus on major % increases or decreases in sales or profit by sub-category and region.

    Data:
    {yoy_data}
    """.strip()
    )
    summary_input = summary_prompt.format_messages(yoy_data=yoy.to_csv(index=False))
    insight_summary = model.invoke(summary_input).content

    return {"insights_summary": insight_summary}


def insight_aggregator_node(state: AgentState):
    search_results = state["search_results"]
    insight_summary = state["insights_summary"]
    initial_request = state["initial_request"]

    prompt = f"""
    You're a marketing analyst. Create a one-page summary report combining web insights and sales data insight summary for a {initial_request}.
    Focus on trends, regional patterns, and recommended actions.

    Web insights:
    {chr(10).join(f"- {ws}" for ws in search_results)}

    Sales data summaries:
    - {insight_summary}

    Return output as:
    1. Executive Summary
    2. Key Insights
    3. Recommended Actions
    """.strip()
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)

    return {"final_report": response.content}


# build graph
graph_builder = StateGraph(AgentState)

graph_builder.add_node("query_generator", query_generator_node)
graph_builder.add_node("search_executor", search_executor_node)
graph_builder.add_node("data_summarizer", data_summarizer_node)
graph_builder.add_node("insight_aggregator", insight_aggregator_node)

graph_builder.add_edge("query_generator", "search_executor")
graph_builder.add_edge("search_executor", "data_summarizer")
graph_builder.add_edge("data_summarizer", "insight_aggregator")

graph_builder.set_entry_point("query_generator")
graph = graph_builder.compile()
