"""Expose ComplAInce AI agent as an API."""

from fastapi import FastAPI

from complaince.core.agent import run_agent
from complaince.schemas.exposition_models import Root

app = FastAPI(
    title="ComplAInce API",
    description="Accelerate code remediation using AI agent",
    version="1.0.0",
)


@app.get("/")
def get_info() -> Root:
    """How to run the ComplAInce agent."""
    return Root(
        version="ComplAInce API 1.0.0",
        message="Welcome to the ComplAInce API",
        description="This API allows you to accelerate code remediation using AI agent",
        usage="Send a POST request to /run_agent?prompt=your_prompt",
    )


@app.post("/run_agent")
def run_agent_api(prompt: str, thread_id: str = ""):
    """
    Run the ComplAInce AI agent.

    Parameters
    ----------
    prompt
        natural language text describing the task that an AI should perform

    tread_id
        ID of the discussion thread

    Returns
    -------
    Lists of messages embedded in a dictionnary
    """
    return run_agent(prompt, thread_id=thread_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("complaince.exposition.complaince_api:app", host="0.0.0.0", port=8000)
