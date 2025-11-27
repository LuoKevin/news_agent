from src.workflow.router import route_message


def test_route_message_handles_unknown_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = route_message("Hi there")
    assert "not sure" in result.message.lower()
