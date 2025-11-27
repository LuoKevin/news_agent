from src.core.intent import Intent, classify_intent


def test_classify_intent_handles_missing_key(monkeypatch):
    # Ensure OPENAI_API_KEY is absent
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = classify_intent("Hello world")
    assert result.intent == Intent.UNKNOWN
    assert result.error == "missing OPENAI_API_KEY"
