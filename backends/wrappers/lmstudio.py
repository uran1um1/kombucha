import subprocess

class lmsmodel():
    def __init__(self):
        self.name = ""
        self.status: bool = False

        if "commit" not in str(subprocess.run(["lms", "--version"], text=True, capture_output=True).stdout).strip():
            raise ValueError("LMStudio is not installed.")
    
    def load(self):
        try:
            subprocess.run(["lms", "load", self.name], timeout=10, text=True, capture_output=True)
        except subprocess.TimeoutExpired:
            raise ValueError(f"Failed to load \"{self.name}\" via LMStudio.")

        self.status = True

    def unload(self):
        if self.name in str(subprocess.run(["lms", "ps"], text=True, capture_output=True).stdout).strip():
            control = subprocess.run(["lms", "unload", self.name], text=True, capture_output=True)

            if "Model Not Found" in str(control.stderr).strip():
                raise ValueError(f"Failed to unload \"{self.name}\" as it is not loaded.")

            self.status = False

    def assign(self, name: str) -> None:

        if name not in str(subprocess.run(["lms", "ls"], text=True, capture_output=True).stdout).strip():
            raise ValueError(f"Model \"{self.name}\" not installed in system.")

        self.name = name

    def prompt(self, text: str) -> str:
        if self.status == True:
            response = str(subprocess.run(["lms", "chat", self.name, "--prompt", f"\"{text}\""], text=True, capture_output=True).stdout).strip()

        return response