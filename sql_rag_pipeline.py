import os
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

DB_PATH = "/Users/radeonxfx/RAG_NL_SQL_pipeline_basics/tesla_motors_data.db"

# ---- Load Claude key ----
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    ANTHROPIC_API_KEY = input("Enter your Claude API key: ")
    os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY


def create_tesla_agent():
    # ---------------- Database ----------------
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

    # SQL query execution tool
    sql_tool = QuerySQLDatabaseTool(db=db)

    tools = [sql_tool]

    # ---------------- LLM (Claude) ----------------
    llm = ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=0,
    )

    # ---------------- System Prompt ----------------
    system_prompt = """You are an expert Tesla Motors SQL analyst.
You ONLY use the provided SQL tool for querying the SQLite database.

Rules:
- NEVER modify the database (no INSERT/UPDATE/DELETE)
- Validate column/table names before querying
- If unsure, ask the user for clarification
- Format final answers in clean paragraphs"""

    # ---------------- Agent ----------------
    # Pass system_prompt as a string directly
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt  # Try 'prompt' instead of 'state_modifier'
    )
    
    return agent


def main():
    print("Initializing Tesla SQL Agent...")
    agent = create_tesla_agent()
    print("Agent ready!\n")

    while True:
        query = input("Ask a Tesla SQL question ('quit' to exit): ")

        if query.lower().strip() == "quit":
            print("Goodbye!")
            break

        try:
            response = agent.invoke({"messages": [("user", query)]})
            # Get the last message from the agent
            last_message = response["messages"][-1]
            print(f"\nANSWER:\n{last_message.content}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()