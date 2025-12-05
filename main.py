"""
CLI entrypoint to run the NewsGenie app.

Usage:
    python main.py
    streamlit run main.py

Environment:
    OPENAI_API_KEY (required for intent/LLM)
    NEWS_API_KEY (required for news fetch)
"""

import os
import sys

import streamlit.web.cli as stcli


def main():
    # Run the Streamlit app located in src/ui/app.py
    app_path = os.path.join(os.path.dirname(__file__), "src", "ui", "app.py")
    sys.argv = ["streamlit", "run", app_path]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
