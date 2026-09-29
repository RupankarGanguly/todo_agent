# AI Todo Manager

A smart Todo Manager powered by LangChain + Groq + Streamlit.

## Features

- Create, list, update, and delete todos
- Filter by status (pending / in_progress / done)
- Filter by priority (low / medium / high)
- Natural language chat interface

## Quick Start

### 1. Extract the zip

```bash
unzip todo-agent.zip
cd todo-agent
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Add your Groq API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and paste your real key
# Get free key from: https://console.groq.com
```

### 4. Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501)

## Deploy on Streamlit Cloud

1. Push this folder to a public GitHub repository
2. Go to https://share.streamlit.io
3. Click **New app** → select your repo → Main file: `app.py`
4. In **Advanced settings → Secrets** add:

```toml
GROQ_API_KEY = "gsk_your_real_key_here"
```

5. Click Deploy

## Project Structure

```
todo-agent/
├── app.py              # Streamlit UI
├── agent.py            # LangChain agent
├── tools.py            # CRUD tools
├── database.py         # SQLite models
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Notes

- Database file (`todos.db`) is created automatically on first run
- On Streamlit Cloud the SQLite database is temporary (resets when app sleeps)
- For permanent storage, switch to PostgreSQL later
