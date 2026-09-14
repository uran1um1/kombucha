import importlib, os, types, json, threading
from tkinter import messagebox

# Define function to help with relative imports
def load(library) -> types.ModuleType:
    current = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    ans = importlib.import_module(library)
    os.chdir(current)
    return ans

# Import the packages using the safe relative import function
lmstudio, nvidia, ollama = load("backends.wrappers.lmstudio"), load("backends.wrappers.nvidia"), load("backends.wrappers.ollama")

def distill(backend: str, format: str, model: str, api_key: str, output_dir: str, steps: int, instances: int) -> None:
    os.chdir(output_dir)

    generator: None

    # Define the model object if local model is detected
    if backend == "Ollama":
        generator = ollama.ollamamodel()
    elif backend =="LMStudio":
        generator = lmstudio.lmsmodel()

    # Load model (not dependent on backend)
    generator.assign(model)
    generator.load()

    # Define a unified prompt function for simplicity later on
    def _prompt(text: str) -> str:

        ans: str = ""

        if backend in ["Ollama", "LMStudio"]:
            ans = generator.prompt(text)
        elif backend == "NIM":
            ans = nvidia.prompt(text, api_key, model)

        if backend == "Reasoning" and not "<think>" in ans:
            messagebox.showerror("Configuration Error", "Selected model does not support the reasoning backend.")
            raise ValueError("Selected model does not support the reasoning backend.")

        return ans

    # Define the sibling thread worker function.
    def _sibling():
        with open("data.json", "a") as file:
            for x in range(int(steps/instances)+1):
                if format == "Reasoning":
                    prompt_prompt = "Create a complex problem in the area of mathematics, computer science, or economics. It should have only one possible answer that is short, such as the name of a single term, a number, etc. Output the question and the question only, do not output any explanation, answers, or formatting. The question should be one paragraph."
                else:
                    prompt_prompt = "Create an AI prompt in one of the following topics: programming, economics, philosophy, business, mathematics. It should be a high quality prompt which demostrates the abilities of the AI model it is given to by making it produce high quality output. Provide just the prompt and no explanation and no formatting. You do not need to provide any category, just the raw prompt."

                prompt = _prompt(prompt_prompt)

                if "</think>" in prompt:
                    prompt = prompt.split("</think>")[1]

                result = _prompt(prompt)

                obj_usr = {
                "role": "user",
                "content": prompt
                }

                obj_mdl = {
                "role": "assistant",
                "content": result
                }

                obj_usr = json.dumps(obj_usr, ensure_ascii=False)
                obj_mdl = json.dumps(obj_mdl, ensure_ascii=False)

                file.write("        " + obj_usr + ",\n" + "        " + obj_mdl + ",\n")
                print(f"Checkpoint {str(x)}/1000")

                file.flush()

    # Reset threads list.
    threads = []

    # Write initial JSON formatting.
    with open("data.json", "w") as file:
        file.write("{\n    \"messages\": [\n")

    # Start the threads.
    for x in range(instances):
        t = threading.Thread(target=_sibling)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Write final JSON formatting.
    with open("data.json", "a") as file:
        file.write("    ]\n}")

    # Unload the model class if the model is local.
    if generator:
        generator.unload()

    with open("data.json", "r") as file:
        data = file.read()
    with open("data.json", "w") as file:
        file.write(data.replace(",\n    ]\n}", "\n    ]\n}"))

    if format in ["Rows&Columns", "Reasoning"]:
        with open("data.json", "r") as file:
            j = json.loads(file.read().strip())

        data = {
            "user": [],
            "assistant": []
        }

        for item in j["messages"]:
            if item["role"] == "user":
                data["user"].append({"content": item["content"]})
            else:
                data["assistant"].append({"content": item["content"]})

        with open("data.json", "w") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

        if format == "Reasoning":
            with open ("data.json", "r") as file:
                raw = file.read().strip()

            j = json.loads(raw)

            data = []

            for item in j["assistant"]:
                result = _prompt(f"I have the following AI output: {item["content"]}. From this output, you must find the single answer, stripping all of the reasoning and formatting. Instead of \"The answer is x\", you must directly output x, the answer, and nothing else.")

                if "</think>" in result:
                    result = result.split("</think>")[1]

                data.append({"content": result})

            with open("data.json", "r") as file:
                j = json.loads(file.read().strip())

            j["answer"] = data

            with open("data.json", "w") as file:
                file.write(json.dumps(j, indent=4, ensure_ascii=False))


    with open("data.json", "r") as file:
        data = file.read()
    with open("data.json", "w") as file:
        file.write(data.replace("            \"content\": \"\\n", "            \"content\": \""))