import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("700x500")
        self.resizable(False, False)
        
        ## Inits categories
        self.stop_event = threading.Event()
        self.organizer_thread = None
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
        
        ## Widget creation
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        ## Label
        ttk.Label(self, text="File Organizer", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        ## Frame controller
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.btn_choose = ttk.Button(control_frame, text="Choose folder", command=self.choose_directory)
        self.btn_choose.pack(side=tk.LEFT, padx=5)
        
        ## Path
        self.path_var = tk.StringVar()
        self.entry_path = ttk.Entry(control_frame, textvariable=self.path_var, width=50)
        self.entry_path.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.btn_start = ttk.Button(control_frame, text="Start", command=self.start_organizing, state=tk.DISABLED)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        ## Logs
        self.log_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.log_area.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
        ## ProgressBar
        self.progress = ttk.Progressbar(self, mode='determinate')
        self.progress.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        # StatusBar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=4, column=0, sticky="ew")

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            self.btn_start["state"] = tk.NORMAL
            self.log(f"Choosen folder: {directory}")

    def start_organizing(self):
        directory = self.path_var.get()
        if not directory:
            messagebox.showerror("Error", "Choose folder before!")
            return
        
        self.btn_start["state"] = tk.DISABLED
        self.btn_choose["state"] = tk.DISABLED
        self.stop_event.clear()
        
        self.organizer_thread = threading.Thread(target=self.organize_files, args=(directory,))
        self.organizer_thread.start()
        self.check_thread_status()

    def check_thread_status(self):## status check
        if self.organizer_thread.is_alive():
            self.after(100, self.check_thread_status)
        else:
            self.btn_start["state"] = tk.NORMAL
            self.btn_choose["state"] = tk.NORMAL

    def organize_files(self, directory):## Main logic
        try:
            files = [
                f for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))
                and f != os.path.basename(__file__)
                and not f.startswith('.')
            ]
            
            if not files:
                self.log("NO files to organize!")
                return

            total_files = len(files)
            self.progress["maximum"] = total_files
            
            for idx, file_name in enumerate(files, 1):
                if self.stop_event.is_set():
                    self.log("Operation has been canceled by you!")
                    return
                
                file_path = os.path.join(directory, file_name)
                file_extension = os.path.splitext(file_name)[1].lower()

                ## Category Check
                category = "Other"
                for cat, exts in self.file_categories.items():
                    if file_extension in exts:
                        category = cat
                        break

                ## Directory creation
                category_dir = os.path.join(directory, category)
                os.makedirs(category_dir, exist_ok=True)

                destination = os.path.join(category_dir, file_name)
                
                try:
                    if os.path.exists(destination):
                        action = self.handle_duplicate(file_name, category)
                        
                        if action == 1:  ## Skip
                            continue
                        elif action == 2:  ## Rewrite
                            os.remove(destination)
                        elif action == 3:  ## Rename
                            base, ext = os.path.splitext(file_name)
                            counter = 1
                            while os.path.exists(destination):
                                new_name = f"{base}_{counter}{ext}"
                                destination = os.path.join(category_dir, new_name)
                                counter += 1
                    
                    shutil.move(file_path, destination)
                    self.log(f"Fine: {file_name} → {category}")
                    
                except (PermissionError, shutil.Error) as e:
                    self.log(f"Error, can't move: {file_name} - {str(e)}")
                
                self.progress["value"] = idx
                self.status_var.set(f"Used: {idx}/{total_files} files")
            
            self.status_var.set("Complete")
            messagebox.showinfo("Congrats", "File organization complete!")
            
        except Exception as e:
            self.log(f"Critical error: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.btn_start["state"] = tk.NORMAL
            self.btn_choose["state"] = tk.NORMAL

    def handle_duplicate(self, file_name, category):## Duplication Check
        dialog = tk.Toplevel(self)
        dialog.title("File conflict")
        dialog.geometry("400x200")
        
        msg = f"File '{file_name}' already exists in this category'{category}':\nChoose option:"
        ttk.Label(dialog, text=msg).pack(pady=10)
        
        choice = tk.IntVar(value=0)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Skip", command=lambda: choice.set(1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rewrite", command=lambda: choice.set(2)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rename", command=lambda: choice.set(3)).pack(side=tk.LEFT, padx=5)
        
        dialog.grab_set()
        self.wait_window(dialog)
        
        return choice.get()

    def log(self, message):## Logs
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.update_idletasks()

    def on_close(self): ## Close window
        if messagebox.askokcancel("Exit", "Are you sure to exit?"):
            self.stop_event.set()
            self.destroy()

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()