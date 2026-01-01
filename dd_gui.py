import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import re
import shutil
import sys
import os

class DdGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DD Cloner - System Check")
        self.root.geometry("600x750")

        # --- STAP 1: CONTROLE EN BEVESTIGING ---
        self.dependencies = {
            "dd": "coreutils",
            "lsblk": "util-linux",
            "sudo": "sudo",
            "python3-tk": "python3-tk"
        }
        self.check_and_verify()

    def check_and_verify(self):
        """Controleert dependencies en toont resultaat."""
        missing = []
        status_msg = ""
        
        for tool, package in self.dependencies.items():
            if tool == "python3-tk": # Speciale check voor tkinter
                status_msg += f"✅ {tool} (pakket: {package}) is aanwezig\n"
                continue
                
            if shutil.which(tool):
                status_msg += f"✅ {tool} (pakket: {package}) is aanwezig\n"
            else:
                status_msg += f"❌ {tool} ONTBREEKT\n"
                missing.append(package)

        if missing:
            self.show_error_panel(missing)
        else:
            self.show_success_panel(status_msg)

    def show_success_panel(self, status_msg):
        """Toont dat alles in orde is."""
        self.clear_window()
        frame = tk.Frame(self.root, padx=30, pady=30)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Systeemcontrole voltooid", font=("bold", 14), fg="#28a745").pack(pady=10)
        
        log_box = tk.Text(frame, height=6, bg="#f8f9fa", font=("Monospace", 10), relief="flat")
        log_box.insert("1.0", status_msg)
        log_box.config(state="disabled")
        log_box.pack(fill="x", pady=10)

        # Check voor ROOT/SUDO rechten
        if os.geteuid() != 0:
            tk.Label(frame, text="⚠️ Let op: App draait niet als root/sudo.\nJe zult een wachtwoord moeten invoeren bij de start.", 
                     fg="#856404", bg="#fff3cd", padx=10, pady=5).pack(fill="x", pady=10)

        tk.Button(frame, text="Start Applicatie", bg="#28a745", fg="white", font=("bold", 11),
                  command=self.load_main_gui, height=2, width=20).pack(pady=20)

    def show_error_panel(self, missing):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text="⚠️ Dependencies ontbreken!", fg="red", font=("bold", 14)).pack(pady=10)
        
        tk.Label(frame, text="Voer dit uit in je terminal (Debian 13):", font=("bold", 10)).pack(anchor="w")
        cmd = f"sudo apt update && sudo apt install {' '.join(set(missing))}"
        
        cmd_box = tk.Text(frame, height=3, bg="#f0f0f0")
        cmd_box.insert("1.0", cmd)
        cmd_box.pack(fill="x", pady=10)
        tk.Button(frame, text="Sluiten", command=sys.exit).pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_main_gui(self):
        """Laadt de werkelijke DD interface."""
        self.clear_window()
        self.root.title("Python DD Cloner - Debian 13")
        
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.block_size = tk.StringVar(value="1M")
        self.total_bytes = 0
        self.process = None
        self.is_cancelled = False

        self.device_list = self.get_devices()
        self.create_main_widgets()

    # --- MAIN GUI COMPONENTS ---
    def get_devices(self):
        try:
            result = subprocess.check_output(['lsblk', '-dpno', 'NAME,SIZE,MODEL'], text=True)
            return result.splitlines()
        except: return ["Geen schijven gevonden"]

    def create_main_widgets(self):
        container = tk.Frame(self.root, padx=15, pady=15)
        container.pack(fill="both", expand=True)

        # Input Selectie
        tk.Label(container, text="1. Bron (Input):", font=('bold', 10)).pack(anchor="w")
        in_f = tk.Frame(container); in_f.pack(fill="x", pady=5)
        ttk.Combobox(in_f, textvariable=self.input_path, values=self.device_list, width=45).pack(side="left")
        tk.Button(in_f, text="Bestand", command=lambda: self.browse_file(self.input_path)).pack(side="left", padx=5)

        # Output Selectie
        tk.Label(container, text="2. Doel (Output):", font=('bold', 10)).pack(anchor="w")
        out_f = tk.Frame(container); out_f.pack(fill="x", pady=5)
        ttk.Combobox(out_f, textvariable=self.output_path, values=self.device_list, width=45).pack(side="left")
        tk.Button(out_f, text="Bestand", command=lambda: self.browse_file(self.output_path)).pack(side="left", padx=5)

        # Blokgrootte
        tk.Label(container, text="3. Snelheid (Blokgrootte):", font=('bold', 10)).pack(anchor="w", pady=(10,0))
        bs_f = tk.Frame(container); bs_f.pack(fill="x", pady=5)
        for s in ["64K", "1M", "4M"]:
            tk.Radiobutton(bs_f, text=s, variable=self.block_size, value=s).pack(side="left", padx=15)

        # Progress
        self.canvas = tk.Canvas(container, height=35, bg="#eee", highlightthickness=0)
        self.canvas.pack(fill="x", pady=20)
        self.progress_rect = self.canvas.create_rectangle(0, 0, 0, 35, fill="red", width=0)
        self.percent_text = self.canvas.create_text(280, 17, text="0%", font=('bold', 11))

        # Log
        self.log_text = tk.Text(container, height=12, bg="#1e1e1e", fg="#00ff00", font=("Monospace", 9))
        self.log_text.pack(fill="both", expand=True, pady=10)

        # Knoppen
        btn_f = tk.Frame(container); btn_f.pack(fill="x")
        self.start_btn = tk.Button(btn_f, text="START CLONEN", bg="#28a745", fg="white", height=2, font=('bold', 11), command=self.start_work)
        self.start_btn.pack(side="left", expand=True, fill="x", padx=5)
        self.stop_btn = tk.Button(btn_f, text="STOP", bg="#dc3545", fg="white", height=2, font=('bold', 11), command=self.stop_work, state="disabled")
        self.stop_btn.pack(side="left", expand=True, fill="x", padx=5)

    # --- LOGICA ---
    def browse_file(self, var):
        f = filedialog.asksaveasfilename(defaultextension=".img")
        if f: var.set(f)

    def start_work(self):
        if_p = self.input_path.get().split()[0]
        of_p = self.output_path.get().split()[0]
        if not if_p or not of_p: return
        
        # Bereken grootte voor progressie
        try:
            self.total_bytes = int(subprocess.check_output(['lsblk', '-dbno', 'SIZE', if_p], text=True).strip())
        except: self.total_bytes = 0

        if messagebox.askyesno("Bevestig", f"Overschrijf {of_p}?"):
            self.is_cancelled = False
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.log_text.delete(1.0, tk.END)
            threading.Thread(target=self.run_dd, args=(if_p, of_p, self.block_size.get()), daemon=True).start()

    def run_dd(self, if_p, of_p, bs):
        cmd = ["sudo", "dd", f"if={if_p}", f"of={of_p}", f"bs={bs}", "iflag=fullblock", "status=progress", "conv=fsync"]
        try:
            self.process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True, bufsize=1)
            for line in self.process.stderr:
                if self.is_cancelled: break
                m = re.search(r'(\d+)\s+bytes', line)
                if m and self.total_bytes > 0:
                    perc = min(100, (int(m.group(1))/self.total_bytes)*100)
                    self.root.after(0, self.update_ui, perc, line)
                else:
                    self.root.after(0, lambda l=line: self.log_text.insert(tk.END, l) or self.log_text.see(tk.END))
            self.process.wait()
        except Exception as e: self.root.after(0, lambda: messagebox.showerror("Fout", str(e)))
        finally: self.root.after(0, self.reset_ui)

    def update_ui(self, perc, line):
        color = "#dc3545" if perc < 33 else "#ffc107" if perc < 66 else "#28a745"
        w = self.canvas.winfo_width()
        self.canvas.coords(self.progress_rect, 0, 0, (perc/100)*w, 35)
        self.canvas.itemconfig(self.progress_rect, fill=color)
        self.canvas.itemconfig(self.percent_text, text=f"{perc:.1f}%")
        self.log_text.insert(tk.END, line)
        self.log_text.see(tk.END)

    def stop_work(self):
        self.is_cancelled = True
        if self.process: self.process.terminate()

    def reset_ui(self):
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = DdGuiApp(root)
    root.mainloop()
