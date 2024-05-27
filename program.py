import os
from fnmatch import fnmatch
import customtkinter as ctk
import json
from file_processing import FileProcessingClass
from git import Repo

APP_STATE_FILE = "app_state.json"
class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.checkbox_list = []

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)

        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="w") 
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def clear_frame(self):
        for checkbox in self.checkbox_list:
            checkbox.destroy()
        self.checkbox_list.clear()

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


class FileSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Search and Process")
        self.geometry("800x600")
        self.directory = ctk.StringVar()
        self.pattern = ctk.StringVar()
        self.prompt = ""
        self.use_git = ctk.BooleanVar() 
        self.create_widgets()
        self.load_app_state()
    
    def save_app_state(self):
        state = {
            "directory": self.directory.get(),
            "pattern": self.pattern.get(),
            "prompt": self.get_prompt()
        }
        with open(APP_STATE_FILE, "w") as f:
            json.dump(state, f)

    def load_app_state(self):
        if os.path.exists(APP_STATE_FILE):
            with open(APP_STATE_FILE, "r") as f:
                state = json.load(f)
                self.directory.set(state.get("directory", ""))
                self.pattern.set(state.get("pattern", ""))
                self.prompt_entry.insert("0.0", state.get("prompt", ""))

    def on_closing(self):
        self.save_app_state()
        self.destroy()

    def create_widgets(self):
        # Directory frame
        dir_frame = ctk.CTkFrame(self)
        dir_frame.pack(pady=10)

        dir_label = ctk.CTkLabel(dir_frame, text="Directory:", padx=10)
        dir_label.pack(side=ctk.LEFT)

        dir_entry = ctk.CTkEntry(dir_frame, textvariable=self.directory, width=400)
        dir_entry.pack(side=ctk.LEFT)

        browse_button = ctk.CTkButton(dir_frame, text="Browse", command=self.browse_directory)
        browse_button.pack(side=ctk.LEFT)

        # Extension frame
        ext_frame = ctk.CTkFrame(self)
        ext_frame.pack(pady=10)

        ext_label = ctk.CTkLabel(ext_frame, text="Extension pattern:", padx=10)
        ext_label.pack(side=ctk.LEFT)

        git_frame = ctk.CTkFrame(self)
        git_frame.pack(pady=10)

        git_checkbox = ctk.CTkCheckBox(git_frame, text="Search using git", variable=self.use_git)
        git_checkbox.pack(side=ctk.LEFT)

        ext_entry = ctk.CTkEntry(ext_frame, textvariable=self.pattern, width=200)
        ext_entry.pack(side=ctk.LEFT)

        search_button = ctk.CTkButton(ext_frame, text="Search", command=self.search_files)
        search_button.pack(side=ctk.LEFT)

        # File list frame
        file_list_frame = ctk.CTkFrame(self)
        file_list_frame.pack(pady=10, fill=ctk.BOTH, expand=True)

        self.file_list = ScrollableCheckBoxFrame(master=file_list_frame, width=600, command=self.checkbox_frame_event,
                                                                 item_list=[f"item {i}" for i in range(50)])
        self.file_list.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10, side=ctk.LEFT)

        # Prompt frame
        prompt_frame = ctk.CTkFrame(self)
        prompt_frame.pack(pady=10)

        prompt_label = ctk.CTkLabel(prompt_frame, text="Prompt:", padx=10)
        prompt_label.pack(side=ctk.LEFT)

        prompt_entry = ctk.CTkTextbox(prompt_frame, width=600, height=100, padx=10)
        prompt_entry.pack(side=ctk.LEFT, fill=ctk.BOTH)
        prompt_entry.insert("0.0", self.prompt)
        self.prompt_entry = prompt_entry

        # Process button
        process_button = ctk.CTkButton(self, text="Process", command=self.process_files)
        process_button.pack(pady=10)

    def browse_directory(self):
        directory = ctk.filedialog.askdirectory()
        self.directory.set(directory)

    def search_files(self):
        directory = self.directory.get()
        pattern = self.pattern.get()

        if not directory or not pattern:
            ctk.CTkMessagebox.showerror("Error", "Please select a directory and enter a pattern.")
            return

        self.file_list.clear_frame()
        found_files = []

        def check_file(file_path):
            if fnmatch(file_path, pattern):
                found_files.append((file_path, file_path.count(os.path.sep)))
                if len(found_files) >= 1000:
                    return True
            return False

        if self.use_git.get():
            repo = Repo(directory)
            git_files = [item[0] for item in repo.index.entries]
            for file in git_files:
                file_path = os.path.join(directory, file)
                if check_file(file_path):
                    break
        else:
            def walk_search():
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if check_file(file_path):
                            return
            walk_search()

        found_files.sort(key=lambda x: x[1])
        for item in found_files:
            self.file_list.add_item(item[0].replace(directory, "").lstrip(os.path.sep) + f" - {item[0]}")

    def process_files(self):
        selected_files = self.file_list.get_checked_items()
        prompt = self.get_prompt()

        if not selected_files:
            ctk.CTkMessagebox.showwarning("Warning", "No files selected.")
            return

        # Call your process_file function here
        for file_path in [item.split(" - ")[1] for item in selected_files]:
            self.process_file(file_path, prompt)

    def process_file(self, file_path, prompt):
        print(f"Processing file: {file_path}")
        processing = FileProcessingClass()
        file_path = os.path.join(self.directory.get(), file_path)
        processing.process_file(file_path, prompt)

    def get_prompt(self):
        prompt_entry = self.prompt_entry
        if isinstance(prompt_entry, ctk.CTkTextbox):
            return prompt_entry.get("0.0", "end-1c")
        else:
            return self.prompt

    def checkbox_frame_event(self):
        print(f"File list modified: {self.file_list.get_checked_items()}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = FileSearchApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()