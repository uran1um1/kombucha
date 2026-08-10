import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk, pyglet
import importlib, os, types

def load(library) -> types.ModuleType:
    current = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    ans = importlib.import_module(library)
    os.chdir(current)
    return ans

distillery_backend = load("backends.distill")

root = tk.Tk()
pyglet.font.add_file("assets/Fira_Mono/FiraMono-Regular.ttf")

root.title("Kombucha - Open Source AI development")
root.geometry("1200x800")

tabs = ttk.Notebook(root)

distillery = ttk.Frame(tabs)

tk.Label(distillery, text="Welcome to Kombucha Distillery!", font=("Fira Code Mono", 16)).pack()
tk.Label(distillery, text="Kombucha Distillery is an open source GUI tool for generating distillation datasets from different large language models. To get started, select the type of dataset, backend, and click start!", font=("Fira Code Mono", 9), wraplength=1200).pack()
tk.Label(distillery, text="\nSetting more than 1 threads for non API backends will likely not have an effect on speed.\n\nLeave API key empty for local models.", font=("Fira Code Mono", 9), wraplength=1200).pack()

distillery_options = tk.Frame(distillery)

backends = ["LMStudio", "Ollama", "NIM"]
backend_opt = tk.StringVar(value="LMStudio")
backend = tk.OptionMenu(distillery_options, backend_opt, *backends).grid(row=1, column=0)

formats = ["Rows&Columns", "Reasoning", "ChatML"]
format_opt = tk.StringVar(value="ChatML")
format = tk.OptionMenu(distillery_options, format_opt, *formats).grid(row=1, column=1)

name = tk.Text(distillery_options, width=10, height=1)
name.grid(row=1, column=3)
name.insert("1.0", "Model ID")

api = tk.Text(distillery_options, width=10, height=1)
api.grid(row=1, column=4)
api.insert("1.0", "API Key")

steps = tk.Text(distillery_options, width=10, height=1)
steps.grid(row=1, column=5)
steps.insert("1.0", "Steps")

threads = tk.Text(distillery_options, width=10, height=1)
threads.grid(row=1, column=6)
threads.insert("1.0", "Threads")

def start_distillery():
    arguments = {
        "backend": backend_opt.get(),
        "format": format_opt.get(),
        "name": name.get("1.0", "end-1c").strip(),
        "api_key": api.get("1.0", "end-1c").strip(),
        "output_dir": filedialog.askdirectory(),
        "steps": int(steps.get("1.0", "end-1c").strip()),
        "threads": int(threads.get("1.0", "end-1c").strip()),
    }

    distillery_backend.distill(arguments["backend"], arguments["format"], arguments["name"], arguments["api_key"], arguments["output_dir"], arguments["steps"], arguments["threads"])

start = tk.Button(distillery_options, text="Start", command=start_distillery).grid(row=1, column=7)

distillery_options.pack(expand=1)

tabs.add(distillery, text="Distillery")

tabs.pack(expand=1, fill="both")

sv_ttk.set_theme("dark")
root.mainloop()