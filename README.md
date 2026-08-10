# Kombucha

## Summary
Kombucha is a graphical all in one tool for setting up and executing synthetic data generation pipelines from LLMs. The project's aim is to provide a simple and easy interface to accelerate AI development. It is written in Python3 and utilizes the Tkinter framework as a simple frontend. The project prioritizes flexibility, meaning that support for multiple backends is expected.

### Can I contribute?
Of course! We are looking for active contributors. Make sure to discuss new features with the maintainer before trying to create a pull request. Your name will the included automatically by GitHub in the CONTRIBUTORS.md file. The project is MIT licensed.

*Please note that this project is still experimental and incomplete.*

## Installation

### With uv

Clone the repository.
```
git clone https://github.com/uran1um1/kombucha
cd kombucha
```

Create a virtual environment.
```
uv venv
```

Install dependencies.
```
uv pip install -r requirements.txt
```

Run the program.
```
python3 -B kombucha.py
```

### With vanilla Python

Clone the repository.
```
git clone https://github.com/uran1um1/kombucha
cd kombucha
```

Create a virtual environment.
```
python3 -m venv .venv
```

Activate the virual environment.
```
source .venv/bin/activate
```

Install dependencies.
```
pip install -r requirements.txt
```

Run the program.
```
python3 -B kombucha.py
```

## Goals

- Reduce dependencies
  - An important technical goal for this project is to reduce dependencies on external libraries such as OpenAI. We aim to achieve this by writing custom backends for the different supported architectures instead of relying on the OpenAI compatible API system. We are looking for contributors who are willing to help. Another aim is to package the graphics dependencies within the folder structure of this repository, minimizing the need for external installations.
- More features
  - Some features which we are aiming to implement in the future are model training and chatting. The aim of this is to transform Kombucha from a simple data generation tool to a graphical LLM development suite.

## Technical Details

### Supported backends
- LMStudio (llmster)
- NVIDIA NIM
- Ollama

### Supported data formats
- ChatML
- Rows & Columns (traditional)
- Reasoning (intended for GRPO)

## Dependencies (Python)

- openai
  - anyio
  - distro
  - httpx
  - jiter
  - pydantic
  - sniffio
  - tqdm
  - typing-extensions
- sv_ttk
- pyglet
