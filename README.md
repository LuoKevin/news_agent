# NewsGenie

AI-powered information and news assistant built with OpenAI, a news API, LangGraph routing, and a Streamlit UI.

## Features
- Intent-aware assistant that routes between news requests and general queries.
- Real-time news fetch with summarization.
- LangGraph-based workflow to classify and dispatch requests efficiently.
- Streamlit chat UI with session history, category/topic selectors, and status indicators.
- Error handling and graceful fallbacks when APIs or keys are missing.

## Architecture
- `src/core`: config and intent classification.
- `src/services`: news API client, factories for external clients.
- `src/workflow`: LangGraph graph plus handler nodes for news/general/unknown.
- `src/ui`: Streamlit app (`app.py`).
- `main.py`: convenience entrypoint to launch the UI.

## Setup
```bash
python -m pip install -r requirements.txt

# Provide keys via environment or .env (pydantic BaseSettings will read .env)
export OPENAI_API_KEY="sk-..."
export NEWS_API_KEY="your-news-api-key"
```

## Run
```bash
# From project root
python main.py
# or
PYTHONPATH=. streamlit run src/ui/app.py
```

## Usage
- Choose a category or enter a custom topic in the sidebar, then ask for news or any question.
- The app keeps chat history per session (`st.session_state`) and shows source/error meta beneath each assistant reply.

## Results (per assignment spec)
1) Interactive AI assistant delivering instant general-query answers and real-time, curated news updates.  
2) Integrated system using a real-time news API, optional web search hook, and a LangGraph-based workflow for efficient query processing.  
3) Demonstration of a user-friendly Streamlit interface with session management, error handling, and responsive design.  
4) Explained fallback mechanisms and optimization strategies to keep responses reliable during API failures (e.g., missing keys, API errors).  

This project demonstrates integrating multiple AI components into a cohesive platform that simplifies information access and improves user experience in a fast-paced digital environment.
