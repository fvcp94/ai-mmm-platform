import requests, os

def openrouter_chat(model, messages):
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "Missing API Key"
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": model, "messages": messages},
    )
    return r.json()["choices"][0]["message"]["content"]
