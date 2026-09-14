import subprocess

class ollamamodel():
    def __init__(self):
        self.name = ""
        self.status = False

        if "ollama version is" not in str(subprocess.run(["ollama", "--version"], text=True, capture_output=True).stdout).strip():
            raise ValueError("Ollama is not installed.")
    
    def load(self):
        self.status = True

    def unload(self):
        if self.name in str(subprocess.run(["ollama", "ps"], text=True, capture_output=True).stdout).strip():

            control = subprocess.run(["ollama", "stop", self.name], text=True, capture_output=True)

            if "couldn't find model" in str(control.stderr).strip():
                raise ValueError(f"Failed to unload \"{self.name}\" as it is not loaded.")

            self.status = False

    def assign(self, name: str) -> None:

        if name not in str(subprocess.run(["ollama", "list"], text=True, capture_output=True).stdout).strip():
            raise ValueError(f"Model \"{self.name}\" not installed in system.")

        self.name = name

    def prompt(self, text: str) -> str:
        if self.status == True:
            response = str(subprocess.run(["ollama", "run", self.name, f"\"{text}\""], text=True, capture_output=True).stdout).strip()

        return response