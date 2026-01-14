import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import threading
from tkinter import filedialog, messagebox
from converter import DataConverter

# Theme settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FlowParquetApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("FlowParquet Converter")
        self.geometry("850x600")
        self.minsize(850, 600)
        
        # State
        self.files = []
        self.is_converting = False
        
        # UI Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_main_area()
        
        # Drag and Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_files)

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) # Spacer
        
        lbl_title = ctk.CTkLabel(self.sidebar, text="FlowParquet", font=("Roboto", 20, "bold"))
        lbl_title.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        btn_add_files = ctk.CTkButton(self.sidebar, text="Add Files...", command=self.browse_files)
        btn_add_files.grid(row=1, column=0, padx=20, pady=10)
        
        btn_add_folder = ctk.CTkButton(self.sidebar, text="Add Folder...", command=self.browse_folder)
        btn_add_folder.grid(row=2, column=0, padx=20, pady=10)
        
        btn_clear = ctk.CTkButton(self.sidebar, text="Clear List", fg_color="transparent", border_width=1, command=self.clear_list)
        btn_clear.grid(row=3, column=0, padx=20, pady=10)
        
        # Footer
        lbl_version = ctk.CTkLabel(self.sidebar, text="v1.0.3", text_color="gray")
        lbl_version.grid(row=5, column=0, padx=20, pady=20)

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1) # List area
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # 1. Options / Toolbar
        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.var_pns = ctk.BooleanVar(value=True)
        chk_pns = ctk.CTkCheckBox(self.options_frame, text="Use Marker Names", variable=self.var_pns)
        chk_pns.pack(side="left", padx=15, pady=10)
        
        self.var_filename = ctk.BooleanVar(value=True)
        chk_filename = ctk.CTkCheckBox(self.options_frame, text="Add SampleID Col", variable=self.var_filename)
        chk_filename.pack(side="left", padx=15, pady=10)
        
        # Compression (Right aligned)
        self.comp_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.comp_frame.pack(side="right", padx=10, pady=5)
        
        ctk.CTkLabel(self.comp_frame, text="Compression:").pack(side="left", padx=5)
        self.var_compression_ui = ctk.StringVar(value="Snappy (Fast)")
        opt_comp = ctk.CTkOptionMenu(self.comp_frame, values=["Snappy (Fast)", "Gzip (Small)", "None"], variable=self.var_compression_ui, width=180)
        opt_comp.pack(side="left", padx=5)

        # 2. File List
        self.file_list_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Queue")
        self.file_list_frame.grid(row=1, column=0, sticky="nsew")
        
        # 3. Action Area (Grid Layout)
        self.action_frame = ctk.CTkFrame(self.main_frame, height=80)
        self.action_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.action_frame.grid_columnconfigure(1, weight=1) # Progress bar expands
        
        self.lbl_status = ctk.CTkLabel(self.action_frame, text="Ready", anchor="w")
        self.lbl_status.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.progress = ctk.CTkProgressBar(self.action_frame)
        self.progress.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        self.progress.set(0)
        
        self.btn_convert = ctk.CTkButton(self.action_frame, text="Convert", command=self.start_conversion, font=("Roboto", 14, "bold"), height=40, fg_color="#2CC985", hover_color="#1FA66B", text_color="black")
        self.btn_convert.grid(row=0, column=2, padx=15, pady=15, sticky="e")

    def browse_files(self):
        filetypes = [("Flow/Data Files", "*.fcs *.csv *.xls *.xlsx"), ("All Files", "*.*")]
        files = filedialog.askopenfilenames(filetypes=filetypes)
        if files:
            self.add_files(files)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            found = []
            for root, _, filenames in os.walk(folder):
                for name in filenames:
                    if name.lower().endswith(('.fcs', '.csv', '.xls', '.xlsx')):
                        found.append(os.path.join(root, name))
            self.add_files(found)

    def drop_files(self, event):
        raw_files = self.tk.splitlist(event.data)
        valid = []
        for f in raw_files:
            if os.path.isfile(f) and f.lower().endswith(('.fcs', '.csv', '.xls', '.xlsx')):
                valid.append(f)
            elif os.path.isdir(f):
                for root, _, filenames in os.walk(f):
                    for name in filenames:
                        if name.lower().endswith(('.fcs', '.csv', '.xls', '.xlsx')):
                            valid.append(os.path.join(root, name))
        self.add_files(valid)

    def add_files(self, file_list):
        new_count = 0
        for f in file_list:
            if f not in self.files:
                self.files.append(f)
                self.create_file_row(f)
                new_count += 1
        self.lbl_status.configure(text=f"Added {new_count} files. Total: {len(self.files)}")

    def create_file_row(self, file_path):
        row = ctk.CTkFrame(self.file_list_frame, height=40)
        row.pack(fill="x", pady=2, padx=5)
        
        name = os.path.basename(file_path)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        lbl_icon = ctk.CTkLabel(row, text="📄", width=30)
        lbl_icon.pack(side="left", padx=5)
        
        lbl_name = ctk.CTkLabel(row, text=name, anchor="w", font=("Roboto", 12, "bold"))
        lbl_name.pack(side="left", padx=5)
        
        lbl_size = ctk.CTkLabel(row, text=f"{size_mb:.1f} MB", text_color="gray", width=60)
        lbl_size.pack(side="right", padx=10)

    def clear_list(self):
        self.files = []
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        self.lbl_status.configure(text="Queue cleared.")

    def start_conversion(self):
        if not self.files:
            messagebox.showwarning("Empty Queue", "No files to convert.")
            return
        if self.is_converting:
            return

        self.is_converting = True
        self.btn_convert.configure(state="disabled", text="Processing...")
        self.progress.set(0)
        
        # Map UI compression to backend values
        comp_ui = self.var_compression_ui.get()
        comp_val = "snappy"
        if "Gzip" in comp_ui: comp_val = "gzip"
        elif "None" in comp_ui: comp_val = None
        
        options = {
            'use_marker_names': self.var_pns.get(),
            'add_filename_col': self.var_filename.get(),
            'compression': comp_val
        }
        
        # Run in thread
        thread = threading.Thread(target=self.run_conversion_thread, args=(options,))
        thread.start()

    def run_conversion_thread(self, options):
        total = len(self.files)
        success = 0
        errors = []

        for i, file_path in enumerate(self.files):
            dir_name = os.path.dirname(file_path)
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(dir_name, f"{base_name}.parquet")
            
            ok, msg = DataConverter.convert_to_parquet(file_path, output_path, options)
            
            if ok:
                success += 1
            else:
                errors.append(f"{os.path.basename(file_path)}: {msg}")
            
            progress_val = (i + 1) / total
            self.progress.set(progress_val)
            self.lbl_status.configure(text=f"Processing {i+1}/{total}...")

        self.is_converting = False
        self.btn_convert.configure(state="normal", text="Convert")
        self.lbl_status.configure(text=f"Done. {success} converted, {len(errors)} failed.")
        
        if errors:
            err_msg = "\n".join(errors[:5])
            if len(errors) > 5: err_msg += "\n..."
            messagebox.showerror("Conversion Errors", f"Some files failed:\n{err_msg}")
        else:
            messagebox.showinfo("Complete", f"Successfully converted {success} files.")

if __name__ == "__main__":
    app = FlowParquetApp()
    app.mainloop()