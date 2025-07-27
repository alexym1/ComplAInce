"""Expose ComplAInce AI agent as an API."""

from complaince.core.agent import run_agent
from complaince.schemas.exposition_models import Root
from fastapi import FastAPI

app = FastAPI(
    title="ComplAInce API",
    description="Accelerate code remediation using AI agent",
    version="1.0.0",
)


@app.get("/")
def get_info() -> Root:
    """How to run the ComplAInce agent."""
    return Root(
        version="ComplAInce API 0.1.0",
        message="Welcome to the ComplAInce API",
        description="This API allows you to accelerate code remediation using AI agent",
        usage="Send a POST request to /run_agent?prompt=your_prompt",
    )

@app.post("/run_agent")
def run_agent_api(prompt: str):
    """
    Run the ComplAInce AI agent.

    Parameters
    ----------
    prompt
        natural language text describing the task that an AI should perform

    Returns
    -------
    Lists of messages embedded in a dictionnary
    """
    return run_agent(prompt)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("complaince.core.exposition:app", host="0.0.0.0", port=8000)
