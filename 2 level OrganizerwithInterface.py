import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer 2.0")
        self.geometry("666x666")
        self.resizable(False, False)
        
        # Button style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Categories
        self.file_categories = {
            "Images": [".jpg", ".jpeg", ".png", ".bmp", ".svg", ".tiff"],
            "Video": [".mov", ".mp4", ".gif", ".avi", ".flv", ".wmv", ".mkv"],
            "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".xlsx", ".xls", ".ppt", ".pptx", ".odt"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".json"],
            "Design": [".psd", ".ai", ".indd", ".blend", ".vsd", ".mpp", ".max", ".fbx", ".prproj", ".stl", ".glx", ".obj"],
            "Executables": [".exe", ".msi", ".deb", ".dmg", ".cmd"]
        }

    def create_widgets(self):
        # Label
        ttk.Label(self, text="File Organizer", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Frame control
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        # Choose path button
        self.btn_choose = ttk.Button(control_frame, text="Choose folder", command=self.choose_directory)
        self.btn_choose.pack(side=tk.LEFT, padx=5)
        
        # Path
        self.path_var = tk.StringVar()
        self.entry_path = ttk.Entry(control_frame, textvariable=self.path_var, width=50)
        self.entry_path.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Start button
        self.btn_start = ttk.Button(control_frame, text="Старт", command=self.start_organizing, state=tk.DISABLED)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        # Logs
        self.log_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.log_area.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
        # Status
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=3, column=0, sticky="ew")

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            self.btn_start["state"] = tk.NORMAL
            self.log("Choosen path: " + directory)
            
    def start_organizing(self):
        directory = self.path_var.get()
        if not directory:
            messagebox.showerror("Error", "Choose folder before!")
            return
        
        try:
            self.organize_files(directory)
            messagebox.showinfo("Congrats", "File organization complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def organize_files(self, directory):
        files = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f != os.path.basename(__file__)
        ]

        if not files:
            self.log("NO files to organize")
            return

        for file_name in files:
            file_path = os.path.join(directory, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()

            ## Category check
            category = "Other"
            for cat, exts in self.file_categories.items():
                if file_extension in exts:
                    category = cat
                    break

            ##direcory creation
            category_dir = os.path.join(directory, category)
            os.makedirs(category_dir, exist_ok=True)

            try:
                destination = os.path.join(category_dir, file_name)
                if not os.path.exists(destination):
                    shutil.move(file_path, destination)
                    self.log(f"Moved: {file_name} → {category}")
                else:
                    self.log(f"File already exists: {file_name} в {category}")
            except Exception as e:
                self.log(f"Error: {file_name} - {str(e)}")

        self.status_var.set("Ready")

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.update_idletasks()

    def on_close(self):
        if messagebox.askokcancel("Exit", "Are you sure to exit?"):
            self.destroy()

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()