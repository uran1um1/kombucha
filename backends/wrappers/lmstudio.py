from openai import OpenAI
import subprocess

def prompt(text: str, model: str) -> str:
    client = OpenAI(
        base_url = "http://localhost:1234/v1",
        api_key="lmstudio"
    )

    completion = client.chat.completions.create(
        model = model,
        messages = [{"role": "user", "content": text}],
        temperature = 1,
        max_tokens = 8192,
        stream = False
    )

    result: str = ""

    reasoning = getattr(completion.choices[0].message, "reasoning_content", None)
    if reasoning:
        result = f"<think>\n{reasoning}\n</think>"
    result = f"{result}\n{completion.choices[0].message.content}"

    return result