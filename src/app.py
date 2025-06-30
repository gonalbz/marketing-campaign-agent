from fastapi import FastAPI
from pydantic import BaseModel
from src import graph

app = FastAPI()


class UserPromptInput(BaseModel):
    prompt: str

class UserPromptOutput(BaseModel):
    prompt_response: str


@app.post("/prompt", response_model=UserPromptOutput)
async def user_prompt(user_prompt: UserPromptInput):
    final_state = graph.graph.invoke(
        {
            "initial_request": user_prompt.prompt
        }
    )
    # TODO: change what gets returned here once we have the full graph in place
    result = '\n\n'.join(final_state['search_results'])
    print(final_state)
    return UserPromptOutput(prompt_response=result)