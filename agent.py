import os
import streamlit as st
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from tools import create_todo, list_todos, update_todos, delete_todo
from database import init_db

init_db()

# ---------- Get API Key safely ----------
def get_groq_api_key():
    # 1. Try Streamlit Secrets first (for Streamlit Cloud)
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    # 2. Try environment variable
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key

    # 3. Fail clearly
    raise ValueError(
        "GROQ_API_KEY not found!\n"
        "→ On Streamlit Cloud: Add it in App Settings → Secrets\n"
        "→ Locally: Put it in .env file"
    )

api_key = get_groq_api_key()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key,          # ← explicitly pass the key
    temperature=0.3,
)

all_tools = [create_todo, list_todos, update_todos, delete_todo]

SYSTEM_PROMPT = """You are a smart and friendly Todo Manager AI assistant.
You help users manage their tasks using a database. You can:
  - Create new tasks
  - List / filter tasks by status or priority
  - Update any field of a task (title, description, status, priority, due date)
  - Delete tasks by ID

Guidelines:
- Always confirm what action you took after each tool call.
- When listing todos, present them in a readable markdown table.
- "mark as done"      → update with status='done'
- "start working on"  → update with status='in_progress'
- "show pending"      → list with status='pending'
- "high priority"     → list with priority='high'
- Be concise and friendly.

Status values:   pending | in_progress | done
Use Status Icons:
  pending      - 🕣 Pending
  in_progress  - ⏳ In Progress
  done         - ✅ Done

Priority values: low | medium | high
"""

memory = InMemorySaver()


def createAgent():
    agent = create_agent(
        model=llm,
        tools=all_tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )
    return agent