"""
Minimal CLI demo: classify and route a user message.

Run: python -m scripts.run_intent_demo "What's new in AI today?"
"""

import sys

from src.workflow.router import route_message


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.run_intent_demo '<user message>'")
        return
    user_message = sys.argv[1]
    result = route_message(user_message)
    print(result)


if __name__ == "__main__":
    main()
