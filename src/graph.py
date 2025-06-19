from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph
from config import settings
from src import prompts
from typing import TypedDict
from pydantic import BaseModel
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage


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
    # TODO: expand state object as needed for other nodes


# define structured output formats
class SearchQueries(BaseModel):
    queries: list[str]


# define graph nodes
def query_generator_node(state: AgentState):
    queries = model.with_structured_output(SearchQueries).invoke([
        SystemMessage(content=prompts.QUERY_PLANNER_PROMPT),
        HumanMessage(content=state['initial_request'])
    ])
    return {'search_queries': queries.queries}


def search_executor_node(state: AgentState):
    results = []
    for q in state['search_queries']:
        response = tavily.invoke({'query': q})
        for r in response['results']:
            results.append(r['content'])
    return {'search_results': results} 


def insight_aggregator_node(state: AgentState):
    # TODO
    pass


def data_summarizer_node(state: AgentState):
    # TODO
    pass


# build graph
graph_builder = StateGraph(AgentState)

graph_builder.add_node('query_generator', query_generator_node)
graph_builder.add_node('search_executor', search_executor_node)
graph_builder.add_node('insight_aggregator', insight_aggregator_node)
graph_builder.add_node('data_summarizer', data_summarizer_node)

graph_builder.add_edge('query_generator', 'search_executor')
graph_builder.add_edge('search_executor', 'insight_aggregator')
graph_builder.add_edge('insight_aggregator', 'data_summarizer')

graph_builder.set_entry_point('query_generator')
graph = graph_builder.compile()