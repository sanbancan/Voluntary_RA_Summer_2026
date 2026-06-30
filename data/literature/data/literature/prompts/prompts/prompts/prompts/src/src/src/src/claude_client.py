from anthropic import Anthropic
from .config import ANTHROPIC_API_KEY, MODEL_NAME

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def messages(system, user, max_tokens=1200, temperature=0.2):
    resp = client.messages.create(
        model=MODEL_NAME,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text
