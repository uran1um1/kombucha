from openai import OpenAI

def prompt(text: str, api_key: str, model: str) -> str:
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = api_key
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