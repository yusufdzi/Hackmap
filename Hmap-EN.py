# Wellcome to my Hack tool
"""
╔══════════════════════════════════════════════════════════════╗
║              Hmap All-in-One Tool                           ║
║                                                             ║
╚══════════════════════════════════════════════════════════════╝
Author  : yusuf.dzi
Purpose : Authorized penetration testing & security assessment
License : For authorized security professionals only
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import ipaddress
import sys
import os
import json
from datetime import datetime
import subprocess
import re


def check_nmap():
    try:
        subprocess.run(["nmap", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


try:
    import nmap as nmap_lib
    HAS_NMAP_LIB = True
except ImportError:
    HAS_NMAP_LIB = False

NMAP_AVAILABLE = check_nmap()


COLORS = {
    "bg_dark":    "#0a0e0f",   
    "bg_frame":   "#111618",   
    "bg_widget":  "#1a1f21", 
    "bg_entry":   "#23282a",   
    "fg_green":   "#00ff41",   
    "fg_white":   "#c8d6d1",   
    "fg_red":     "#ff3355",   
    "fg_yellow":  "#ffd700",   
    "fg_cyan":    "#00e5ff",   
    "fg_orange":  "#ff8c00",   
    "accent":     "#00ff41",   
    "accent2":    "#006400",   
    "select_bg":  "#003b00",   
    "select_fg":  "#00ff41",   
    "border":     "#1a3a1a",   
    "progress":   "#00ff41",   
}


FONTS = {
    "title":   ("Consolas", 14, "bold"),
    "heading": ("Consolas", 11, "bold"),
    "normal":  ("Consolas", 10),
    "small":   ("Consolas", 8),
    "mono":    ("Consolas", 10),
}


class NmapHackerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hmap All-in-One Tool | yusuf.dzi ")
        self.root.geometry("1280x820")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.minsize(1024, 700)

        
        self.scanning = False
        self.scan_thread = None
        self.nm = None
        self.scan_history = []

        
        self.style = ttk.Style()
        self.setup_styles()

        
        self.build_header()
        self.build_main_layout()
        self.build_statusbar()

        
        self.log("Hmap all-in-one tool started.")
        if not NMAP_AVAILABLE:
            self.log("⚠️  Nmap is not installed! Please install: sudo apt install nmap", "red")
        elif not HAS_NMAP_LIB:
            self.log("ℹ️  python-nmap not installed. Using subprocess mode.", "yellow")
        else:
            self.log("✅ python-nmap library loaded.", "green")
        self.log("=" * 60)

        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    
    def setup_styles(self):
        self.style.theme_use("clam")
        
        self.style.configure("Hacker.TFrame", background=COLORS["bg_frame"])
        self.style.configure("Widget.TFrame", background=COLORS["bg_widget"])
        
        self.style.configure("Hacker.TLabelframe",
                             background=COLORS["bg_frame"],
                             foreground=COLORS["fg_green"],
                             bordercolor=COLORS["border"],
                             lightcolor=COLORS["border"],
                             darkcolor=COLORS["border"])
        self.style.configure("Hacker.TLabelframe.Label",
                             background=COLORS["bg_frame"],
                             foreground=COLORS["fg_green"],
                             font=FONTS["heading"])
        
        self.style.configure("Hacker.TLabel",
                             background=COLORS["bg_widget"],
                             foreground=COLORS["fg_white"],
                             font=FONTS["normal"])
        self.style.configure("Green.TLabel",
                             background=COLORS["bg_widget"],
                             foreground=COLORS["fg_green"],
                             font=FONTS["normal"])
        self.style.configure("Title.TLabel",
                             background=COLORS["bg_dark"],
                             foreground=COLORS["fg_green"],
                             font=FONTS["title"])
        self.style.configure("Red.TLabel",
                             background=COLORS["bg_widget"],
                             foreground=COLORS["fg_red"],
                             font=FONTS["normal"])
        
        self.style.configure("Hacker.TButton",
                             background=COLORS["bg_entry"],
                             foreground=COLORS["fg_green"],
                             bordercolor=COLORS["accent"],
                             font=FONTS["normal"],
                             padding=(10, 4))
        self.style.map("Hacker.TButton",
                       background=[("active", COLORS["select_bg"]),
                                   ("disabled", COLORS["bg_widget"])],
                       foreground=[("active", COLORS["fg_green"]),
                                   ("disabled", "#555555")])
        
        self.style.configure("Hacker.TEntry",
                             fieldbackground=COLORS["bg_entry"],
                             foreground=COLORS["fg_green"],
                             bordercolor=COLORS["border"],
                             insertcolor=COLORS["fg_green"],
                             font=FONTS["normal"])
        
        self.style.configure("Hacker.TCombobox",
                             fieldbackground=COLORS["bg_entry"],
                             foreground=COLORS["fg_green"],
                             background=COLORS["bg_widget"],
                             arrowcolor=COLORS["fg_green"],
                             bordercolor=COLORS["border"],
                             font=FONTS["normal"])
        self.style.map("Hacker.TCombobox",
                       fieldbackground=[("readonly", COLORS["bg_entry"])])
        
        self.style.configure("Hacker.TCheckbutton",
                             background=COLORS["bg_widget"],
                             foreground=COLORS["fg_white"],
                             font=FONTS["normal"])
        self.style.map("Hacker.TCheckbutton",
                       background=[("active", COLORS["bg_widget"])])
        
        self.style.configure("Hacker.Horizontal.TProgressbar",
                             background=COLORS["progress"],
                             troughcolor=COLORS["bg_entry"],
                             bordercolor=COLORS["border"],
                             lightcolor=COLORS["progress"],
                             darkcolor=COLORS["progress"])
        
        self.style.configure("Hacker.TScale",
                             background=COLORS["bg_widget"],
                             foreground=COLORS["fg_green"],
                             troughcolor=COLORS["bg_entry"],
                             sliderlength=20)

    
    def build_header(self):
        header = tk.Frame(self.root, bg=COLORS["bg_dark"])
        header.pack(fill="x", padx=10, pady=(8, 2))

        
        logo_lines = [
            "╔═══════════════════════════════════════════╗",
            "║   ██╗  ██╗███╗   ███╗ █████╗ ██████╗     ║",
            "║   ██║  ██║████╗ ████║██╔══██╗██╔══██╗    ║",
            "║   ███████║██╔████╔██║███████║██████╔╝    ║",
            "║   ██╔══██║██║╚██╔╝██║██╔══██║██╔═══╝     ║",
            "║   ██║  ██║██║ ╚═╝ ██║██║  ██║██║         ║",
            "║   ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝         ║",
            "╚═══════════════════════════════════════════╝",
        ]
        logo_frame = tk.Frame(header, bg=COLORS["bg_dark"])
        logo_frame.pack(side="left")
        for line in logo_lines:
            lbl = tk.Label(logo_frame, text=line,
                           fg=COLORS["fg_green"], bg=COLORS["bg_dark"],
                           font=("Consolas", 7), anchor="w")
            lbl.pack(anchor="w")

        
        title_frame = tk.Frame(header, bg=COLORS["bg_dark"])
        title_frame.pack(side="right", fill="y", padx=10)
        tk.Label(title_frame, text="ALL-IN-ONE TOOL",
                 font=("Consolas", 16, "bold"),
                 fg=COLORS["fg_green"], bg=COLORS["bg_dark"]).pack(anchor="e")
        tk.Label(title_frame, text="v1.2 | Hackmap Scanner | yusuf.dzi",
                 font=("Consolas", 9),
                 fg=COLORS["fg_cyan"], bg=COLORS["bg_dark"]).pack(anchor="e")

        separator = tk.Frame(self.root, height=2, bg=COLORS["accent"])
        separator.pack(fill="x", padx=10, pady=3)

    
    def build_main_layout(self):
        main_paned = tk.PanedWindow(self.root, bg=COLORS["bg_dark"],
                                    sashwidth=2, sashrelief="sunken",
                                    sashcursor="sb_h_double_arrow")
        main_paned.pack(fill="both", expand=True, padx=10, pady=4)

        
        left_panel = tk.Frame(main_paned, bg=COLORS["bg_frame"])
        main_paned.add(left_panel, width=420, minsize=380)

        
        target_frame = ttk.LabelFrame(left_panel, text="🎯 TARGET", style="Hacker.TLabelframe")
        target_frame.pack(fill="x", padx=5, pady=(5, 3), ipady=2)

        tk.Label(target_frame, text="target IP / Host / Network (e.g. 192.183.175.166):",
                 font=FONTS["small"], fg=COLORS["fg_white"], bg=COLORS["bg_widget"]).pack(anchor="w", padx=8, pady=(5, 0))

        entry_row = tk.Frame(target_frame, bg=COLORS["bg_widget"])
        entry_row.pack(fill="x", padx=8, pady=5)

        self.target_var = tk.StringVar(value="192.168.1.0/24")
        self.target_entry = tk.Entry(entry_row, textvariable=self.target_var,
                                      font=FONTS["normal"], bg=COLORS["bg_entry"],
                                      fg=COLORS["fg_green"], insertbackground=COLORS["fg_green"],
                                      relief="flat", bd=2, highlightthickness=1,
                                      highlightcolor=COLORS["accent"],
                                      highlightbackground=COLORS["border"])
        self.target_entry.pack(side="left", fill="x", expand=True, ipady=3)
        self.target_entry.bind("<Return>", lambda e: self.start_scan())

        
        quick_frame = tk.Frame(target_frame, bg=COLORS["bg_widget"])
        quick_frame.pack(fill="x", padx=8, pady=(0, 5))
        for label, ip in [("Localhost", "127.0.0.1"), ("Gateway", "192.168.1.1"),
                          ("Subnet /24", "192.168.1.0/24"), ("Subnet /16", "192.168.0.0/16")]:
            btn = tk.Button(quick_frame, text=label, font=("Consolas", 7),
                            bg=COLORS["bg_entry"], fg=COLORS["fg_cyan"],
                            relief="flat", bd=1, padx=6, pady=1,
                            activebackground=COLORS["select_bg"],
                            activeforeground=COLORS["fg_green"],
                            command=lambda ip=ip: self.set_target(ip))
            btn.pack(side="left", padx=2)

        
        profile_frame = ttk.LabelFrame(left_panel, text="⚡ SCAN PROFIL", style="Hacker.TLabelframe")
        profile_frame.pack(fill="x", padx=5, pady=3, ipady=2)

        self.profile_var = tk.StringVar(value="Quick Scan")
        profiles = [
            ("Quick Scan",            "-T4 -F"),
            ("Ping Sweep",            "-sn"),
            ("OS Detection",          "-O --osscan-guess"),
            ("Aggressive Scan",       "-A -T4"),
            ("Full Port Scan",        "-p- -T4"),
            ("Service Version",       "-sV -T4"),
            ("Top 1000 Ports",        "--top-ports 1000"),
            ("Vulnerability Scan",    "-sV --script vuln"),
            ("Stealth SYN Scan",      "-sS -T2"),
            ("UDP Scan",              "-sU --top-ports 200"),
            ("Comprehensive",         "-sC -sV -O -T4"),
        ]
        for txt, args in profiles:
            rb = tk.Radiobutton(profile_frame, text=txt, variable=self.profile_var,
                                value=txt, font=FONTS["small"],
                                fg=COLORS["fg_white"], bg=COLORS["bg_widget"],
                                selectcolor=COLORS["bg_dark"],
                                activebackground=COLORS["bg_widget"],
                                activeforeground=COLORS["fg_green"],
                                indicatoron=0, bd=1, relief="flat",
                                padx=6, pady=2)
            rb.pack(fill="x", padx=8, pady=1)
            
            rb.bind("<Enter>", lambda e, b=rb: b.configure(bg=COLORS["select_bg"]))
            rb.bind("<Leave>", lambda e, b=rb: b.configure(bg=COLORS["bg_widget"]))

        self.profile_map = dict(profiles)

        
        adv_frame = ttk.LabelFrame(left_panel, text="🔧 ADVANCED OPTIONS", style="Hacker.TLabelframe")
        adv_frame.pack(fill="x", padx=5, pady=3, ipady=2)

        
        arg_row = tk.Frame(adv_frame, bg=COLORS["bg_widget"])
        arg_row.pack(fill="x", padx=8, pady=3)
        tk.Label(arg_row, text="Extra Args:", font=FONTS["small"],
                 fg=COLORS["fg_white"], bg=COLORS["bg_widget"]).pack(side="left")
        self.args_var = tk.StringVar()
        tk.Entry(arg_row, textvariable=self.args_var, font=("Consolas", 9),
                 bg=COLORS["bg_entry"], fg=COLORS["fg_yellow"],
                 insertbackground=COLORS["fg_yellow"],
                 relief="flat", bd=2, highlightthickness=1,
                 highlightcolor=COLORS["accent"],
                 highlightbackground=COLORS["border"]).pack(side="left", fill="x", expand=True, padx=5, ipady=2)

        
        speed_row = tk.Frame(adv_frame, bg=COLORS["bg_widget"])
        speed_row.pack(fill="x", padx=8, pady=3)
        tk.Label(speed_row, text="Timing (-T):", font=FONTS["small"],
                 fg=COLORS["fg_white"], bg=COLORS["bg_widget"]).pack(side="left")
        self.timing_var = tk.StringVar(value="T4")
        timing_menu = ttk.Combobox(speed_row, textvariable=self.timing_var,
                                    values=["T0 (Paranoid)", "T1 (Sneaky)", "T2 (Polite)",
                                            "T3 (Normal)", "T4 (Aggressive)", "T5 (Insane)"],
                                    state="readonly", width=20, style="Hacker.TCombobox")
        timing_menu.pack(side="left", padx=5)

        
        port_row = tk.Frame(adv_frame, bg=COLORS["bg_widget"])
        port_row.pack(fill="x", padx=8, pady=3)
        tk.Label(port_row, text="Port Range:", font=FONTS["small"],
                 fg=COLORS["fg_white"], bg=COLORS["bg_widget"]).pack(side="left")
        self.port_var = tk.StringVar(value="")
        tk.Entry(port_row, textvariable=self.port_var, font=("Consolas", 9),
                 bg=COLORS["bg_entry"], fg=COLORS["fg_yellow"],
                 insertbackground=COLORS["fg_yellow"],
                 relief="flat", bd=2, width=20,
                 highlightthickness=1, highlightcolor=COLORS["accent"],
                 highlightbackground=COLORS["border"]).pack(side="left", padx=5, ipady=2, fill="x", expand=True)

        
        btn_frame = tk.Frame(left_panel, bg=COLORS["bg_frame"])
        btn_frame.pack(fill="x", padx=8, pady=5)

        self.scan_btn = tk.Button(btn_frame, text="🚀 START SCAN", font=("Consolas", 12, "bold"),
                                   bg="#003b00", fg=COLORS["fg_green"],
                                   relief="ridge", bd=3, padx=15, pady=6,
                                   activebackground="#005a00", activeforeground="#00ff41",
                                   command=self.start_scan)
        self.scan_btn.pack(side="left", fill="x", expand=True)

        self.stop_btn = tk.Button(btn_frame, text="⏹ STOP", font=("Consolas", 12, "bold"),
                                   bg="#3a0000", fg=COLORS["fg_red"],
                                   relief="ridge", bd=3, padx=15, pady=6,
                                   state="disabled",
                                   activebackground="#5a0000", activeforeground="#ff3355",
                                   command=self.stop_scan)
        self.stop_btn.pack(side="right", padx=(5, 0))

        
        exp_frame = tk.Frame(left_panel, bg=COLORS["bg_frame"])
        exp_frame.pack(fill="x", padx=8, pady=2)
        tk.Button(exp_frame, text="📄 Export TXT", font=FONTS["small"],
                  bg=COLORS["bg_entry"], fg=COLORS["fg_cyan"],
                  relief="flat", padx=8, pady=2,
                  activebackground=COLORS["select_bg"],
                  activeforeground=COLORS["fg_green"],
                  command=self.export_txt).pack(side="left", padx=2)
        tk.Button(exp_frame, text="📊 Export JSON", font=FONTS["small"],
                  bg=COLORS["bg_entry"], fg=COLORS["fg_cyan"],
                  relief="flat", padx=8, pady=2,
                  activebackground=COLORS["select_bg"],
                  activeforeground=COLORS["fg_green"],
                  command=self.export_json).pack(side="left", padx=2)
        tk.Button(exp_frame, text="🧹 Clear Output", font=FONTS["small"],
                  bg=COLORS["bg_entry"], fg=COLORS["fg_red"],
                  relief="flat", padx=8, pady=2,
                  activebackground=COLORS["select_bg"],
                  activeforeground=COLORS["fg_red"],
                  command=self.clear_output).pack(side="right", padx=2)

        
        right_panel = tk.Frame(main_paned, bg=COLORS["bg_frame"])
        main_paned.add(right_panel, width=800, minsize=500)

        
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill="both", expand=True, padx=3, pady=3)

       
        self.output_tab = tk.Frame(self.notebook, bg=COLORS["bg_dark"])
        self.notebook.add(self.output_tab, text="  📡 Scan Output  ")

        self.output_text = scrolledtext.ScrolledText(
            self.output_tab,
            bg=COLORS["bg_dark"], fg=COLORS["fg_green"],
            insertbackground=COLORS["fg_green"],
            font=("Consolas", 10),
            relief="flat", bd=2,
            highlightthickness=1, highlightcolor=COLORS["border"],
            state="normal", wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=3, pady=3)
        
        self.output_text.tag_configure("green", foreground=COLORS["fg_green"])
        self.output_text.tag_configure("red", foreground=COLORS["fg_red"])
        self.output_text.tag_configure("yellow", foreground=COLORS["fg_yellow"])
        self.output_text.tag_configure("cyan", foreground=COLORS["fg_cyan"])
        self.output_text.tag_configure("orange", foreground=COLORS["fg_orange"])
        self.output_text.tag_configure("white", foreground=COLORS["fg_white"])
        self.output_text.tag_configure("bold", font=("Consolas", 10, "bold"))
        self.output_text.tag_configure("header", foreground=COLORS["fg_green"],
                                        font=("Consolas", 10, "bold"))
        self.output_text.tag_configure("open_port", foreground="#00ff41",
                                        font=("Consolas", 10, "bold"))

        
        self.history_tab = tk.Frame(self.notebook, bg=COLORS["bg_dark"])
        self.notebook.add(self.history_tab, text="  📜 History  ")

        self.history_text = scrolledtext.ScrolledText(
            self.history_tab,
            bg=COLORS["bg_dark"], fg=COLORS["fg_white"],
            font=("Consolas", 9),
            relief="flat", bd=2,
            highlightthickness=1, highlightcolor=COLORS["border"],
            state="normal", wrap="word")
        self.history_text.pack(fill="both", expand=True, padx=3, pady=3)
        self.history_text.tag_configure("green", foreground=COLORS["fg_green"])
        self.history_text.tag_configure("red", foreground=COLORS["fg_red"])
        self.history_text.tag_configure("yellow", foreground=COLORS["fg_yellow"])
        self.history_text.tag_configure("cyan", foreground=COLORS["fg_cyan"])

        
        self.hosts_tab = tk.Frame(self.notebook, bg=COLORS["bg_dark"])
        self.notebook.add(self.hosts_tab, text="  🖥 Hosts  ")

        
        tree_frame = tk.Frame(self.hosts_tab, bg=COLORS["bg_dark"])
        tree_frame.pack(fill="both", expand=True, padx=3, pady=3)

        columns = ("host", "status", "os", "ports_open", "services")
        self.hosts_tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                       height=10)
        self.hosts_tree.heading("host", text="Host")
        self.hosts_tree.heading("status", text="Status")
        self.hosts_tree.heading("os", text="OS Detection")
        self.hosts_tree.heading("ports_open", text="Open ports")
        self.hosts_tree.heading("services", text="Services")

        self.hosts_tree.column("host", width=150, anchor="w")
        self.hosts_tree.column("status", width=80, anchor="center")
        self.hosts_tree.column("os", width=180, anchor="w")
        self.hosts_tree.column("ports_open", width=120, anchor="center")
        self.hosts_tree.column("services", width=250, anchor="w")

        
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical",
                                    command=self.hosts_tree.yview)
        self.hosts_tree.configure(yscrollcommand=tree_scroll.set)
        self.hosts_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        
        style = ttk.Style()
        style.configure("Treeview",
                        background=COLORS["bg_widget"],
                        foreground=COLORS["fg_white"],
                        rowheight=25,
                        fieldbackground=COLORS["bg_widget"],
                        font=("Consolas", 9))
        style.configure("Treeview.Heading",
                        background=COLORS["bg_entry"],
                        foreground=COLORS["fg_green"],
                        font=("Consolas", 9, "bold"))
        style.map("Treeview",
                  background=[("selected", COLORS["select_bg"])],
                  foreground=[("selected", COLORS["fg_green"])])

        
        self.progress_frame = tk.Frame(right_panel, bg=COLORS["bg_frame"],
                                       height=25)
        self.progress_frame.pack(fill="x", padx=3, pady=(0, 2))
        tk.Label(self.progress_frame, text="Progress:",
                 font=FONTS["small"], fg=COLORS["fg_white"],
                 bg=COLORS["bg_frame"]).pack(side="left", padx=5)
        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                             mode="indeterminate",
                                             style="Hacker.Horizontal.TProgressbar")
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5, pady=3)
        self.progress_label = tk.Label(self.progress_frame, text="Ready",
                                        font=FONTS["small"],
                                        fg=COLORS["fg_green"],
                                        bg=COLORS["bg_frame"])
        self.progress_label.pack(side="right", padx=5)

    
    def build_statusbar(self):
        status_frame = tk.Frame(self.root, height=24, bg=COLORS["bg_dark"])
        status_frame.pack(fill="x", padx=10, pady=(0, 5))

        sep = tk.Frame(status_frame, height=1, bg=COLORS["border"])
        sep.pack(fill="x")

        inner = tk.Frame(status_frame, bg=COLORS["bg_dark"])
        inner.pack(fill="x", pady=(3, 0))

        self.status_label = tk.Label(inner, text="✅ READY | Enter target and start scan",
                                      font=FONTS["small"],
                                      fg=COLORS["fg_green"], bg=COLORS["bg_dark"],
                                      anchor="w")
        self.status_label.pack(side="left")

        nmap_status = "✅ Nmap installed" if NMAP_AVAILABLE else "❌ Nmap is missing."
        tk.Label(inner, text=nmap_status, font=FONTS["small"],
                 fg=COLORS["fg_green"] if NMAP_AVAILABLE else COLORS["fg_red"],
                 bg=COLORS["bg_dark"]).pack(side="right", padx=5)

        tk.Label(inner, text=f"│ {datetime.now().strftime('%H:%M:%S')}",
                 font=FONTS["small"],
                 fg=COLORS["fg_white"], bg=COLORS["bg_dark"]).pack(side="right", padx=3)

    
    def set_target(self, ip):
        self.target_var.set(ip)
        self.log(f"target set: {ip}", "cyan")

    def log(self, msg, tag="white"):
        self.output_text.insert("end", f">> {msg}\n", tag)
        self.output_text.see("end")
        self.root.update_idletasks()

    def clear_output(self):
        self.output_text.delete("1.0", "end")
        self.hosts_tree.delete(*self.hosts_tree.get_children())
        self.log("Output cleared.", "yellow")

    def update_status(self, msg):
        self.status_label.config(text=msg)
        self.root.update_idletasks()

    
    def start_scan(self):
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("error", "Please enter a target!")
            return

        if not NMAP_AVAILABLE:
            messagebox.showerror("Nmap is missing.",
                                 "Nmap is not installed.\n\n"
                                 "Installation: sudo apt install nmap")
            return

        
        self.scanning = True
        self.scan_btn.config(state="disabled", text="🔄 Scan in progress...")
        self.stop_btn.config(state="normal")
        self.progress_bar.start(15)
        self.progress_label.config(text="Scanning...")

        
        self.output_text.delete("1.0", "end")
        self.hosts_tree.delete(*self.hosts_tree.get_children())

        
        args_list = []
        profile = self.profile_map.get(self.profile_var.get(), "-T4 -F")
        args_list.append(profile)

        
        timing = self.timing_var.get().split(" ")[0]
        args_list.append(f"-{timing}")

        
        ports = self.port_var.get().strip()
        if ports:
            args_list.append(f"-p {ports}")

        
        extra = self.args_var.get().strip()
        if extra:
            args_list.append(extra)

        final_args = " ".join(args_list)

        self.log(f"{'='*60}", "header")
        self.log(f"🚀 STARTE SCAN", "bold")
        self.log(f"   Target   : {target}", "cyan")
        self.log(f"   Profil : {self.profile_var.get()}", "cyan")
        self.log(f"   Args   : {final_args}", "yellow")
        self.log(f"   Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "white")
        self.log(f"{'='*60}", "header")

        self.update_status(f"🔍 Scan {target} ...")

        
        self.scan_thread = threading.Thread(
            target=self.run_scan,
            args=(target, final_args),
            daemon=True
        )
        self.scan_thread.start()

    def run_scan(self, target, args):
        try:
            if HAS_NMAP_LIB:
                self.run_scan_python_nmap(target, args)
            else:
                self.run_scan_subprocess(target, args)
        except Exception as e:
            self.root.after(0, self.log, f"❌ ERROR: {str(e)}", "red")
        finally:
            self.root.after(0, self.scan_complete)

    def run_scan_python_nmap(self, target, args):
        self.nm = nmap_lib.PortScanner()

        self.root.after(0, self.log, "[*] Use the python-nmap library...", "green")

        
        scan_result = self.nm.scan(hosts=target, arguments=args)

        self.root.after(0, self.log, f"\n[+] Scan-command: {self.nm.command_line()}", "cyan")
        self.root.after(0, self.log, f"[+] Scan-Info: {self.nm.scaninfo()}\n", "yellow")

        
        for host in self.nm.all_hosts():
            hostname = self.nm[host].hostname() or "N/A"
            ip = host
            state = self.nm[host].state()

            
            os_info = "N/A"
            if 'osmatch' in self.nm[host] and self.nm[host]['osmatch']:
                os_match = self.nm[host]['osmatch'][0]
                os_info = f"{os_match['name']} ({os_match['accuracy']}%)"

            
            open_ports = []
            services_list = []
            for proto in self.nm[host].all_protocols():
                ports = sorted(self.nm[host][proto].keys())
                for port in ports:
                    p_info = self.nm[host][proto][port]
                    if p_info['state'] == 'open':
                        open_ports.append(port)
                        svc = p_info.get('name', 'unknown')
                        ver = p_info.get('version', '')
                        extra = f" ({ver})" if ver else ""
                        services_list.append(f"{port}/{proto} - {svc}{extra}")

            ports_str = ", ".join(map(str, open_ports)) if open_ports else "No open ports"
            svc_str = "\n       ".join(services_list) if services_list else "N/A"

            
            self.root.after(0, self.print_host_result,
                           ip, hostname, state, os_info, ports_str, svc_str)

            
            self.root.after(0, self.add_host_to_tree,
                           ip, state, os_info, str(len(open_ports)),
                           svc_str[:80] + "..." if len(svc_str) > 80 else svc_str)

        
        self.root.after(0, self.log, f"\n{'='*60}", "header")
        self.root.after(0, self.log,
                       f"[✓] Scan complete. {len(self.nm.all_hosts())} Host(s) found.",
                       "green")

      
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {target} | Profil: {self.profile_var.get()} | {len(self.nm.all_hosts())} Hosts"
        self.scan_history.append(entry)
        self.root.after(0, self.update_history)

    def run_scan_subprocess(self, target, args):
        self.root.after(0, self.log, "[*] Use subprocess (nmap CLI)...", "green")

        cmd = ["nmap", "-oX", "-"] + args.split() + [target]
        self.root.after(0, self.log, f"[*] Command: {' '.join(cmd)}", "yellow")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        
        output_lines = []
        for line in process.stdout:
            line = line.rstrip()
            output_lines.append(line)
            self.root.after(0, self.append_output, line + "\n")

        process.wait()

        if process.returncode == 0:
            self.root.after(0, self.log, f"\n{'='*60}", "header")
            self.root.after(0, self.log, "[✓] Scan successfully completed.", "green")
        else:
            self.root.after(0, self.log, f"❌ Scan failed (Code: {process.returncode})", "red")

        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {target} | Profil: {self.profile_var.get()} | subprocess"
        self.scan_history.append(entry)
        self.root.after(0, self.update_history)

    def append_output(self, text):
        self.output_text.insert("end", text, "white")
        self.output_text.see("end")
        self.root.update_idletasks()

    def print_host_result(self, ip, hostname, state, os_info, ports, services):
        color = "green" if state == "up" else "red"
        self.log(f"\n{'─'*50}", "cyan")
        self.log(f"  HOST   : {ip}", "bold")
        self.log(f"  Hostname: {hostname}", "white")
        self.log(f"  Status : {state}", color)
        self.log(f"  OS     : {os_info}", "orange")

        if state == "up":
            if ports and ports != "No open ports":
                self.log(f"  Ports  : {ports}", "open_port")
            if services and services != "N/A":
                for line in services.split("\n"):
                    self.log(f"           {line.strip()}", "white")
        self.log(f"{'─'*50}", "cyan")

    def add_host_to_tree(self, ip, status, os_info, port_count, services):
        try:
            self.hosts_tree.insert("", "end", values=(ip, status, os_info, port_count, services))
        except tk.TclError:
            pass

    def scan_complete(self):
        self.scanning = False
        self.scan_btn.config(state="normal", text="🚀 START SCAN")
        self.stop_btn.config(state="disabled")
        self.progress_bar.stop()
        self.progress_label.config(text="Ready ✓")
        self.update_status("✅ Scan complete")

    def stop_scan(self):
        if self.scanning:
            self.scanning = False
            self.log("\n⛔ SCAN STOPPED BY USER", "red")
            self.scan_complete()

    
    def update_history(self):
        self.history_text.delete("1.0", "end")
        for entry in self.scan_history[-50:]:  # letzte 50 Einträge
            self.history_text.insert("end", entry + "\n", "green")
        self.history_text.see("end")

    
    def export_txt(self):
        content = self.output_text.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Info", "No scan results to export.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nmap_scan_{timestamp}.txt"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=filename,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Export scan results"
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"╔══════════════════════════════════════════╗\n")
                    f.write(f"║   Hmap All-in-One Tool - Report          ║\n")
                    f.write(f"║   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}              ║\n")
                    f.write(f"╚══════════════════════════════════════════╝\n\n")
                    f.write(content)
                self.log(f"📄 Exported to: {filepath}", "green")
            except Exception as e:
                self.log(f"❌ Export error: {e}", "red")

    def export_json(self):
        content = self.output_text.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Info", "No scan results to export.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nmap_scan_{timestamp}.json"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=filename,
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            title="Export scan results"
        )
        if filepath:
            try:
                data = {
                    "tool": "Hmap All-in-One Tool",
                    "timestamp": datetime.now().isoformat(),
                    "target": self.target_var.get(),
                    "profile": self.profile_var.get(),
                    "output": content,
                    "hosts": [
                        {
                            "ip": self.hosts_tree.item(item)["values"][0],
                            "status": self.hosts_tree.item(item)["values"][1],
                            "os": self.hosts_tree.item(item)["values"][2],
                            "ports_open": self.hosts_tree.item(item)["values"][3],
                        }
                        for item in self.hosts_tree.get_children()
                    ]
                }
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self.log(f"📊 JSON exported to: {filepath}", "green")
            except Exception as e:
                self.log(f"❌ JSON export error: {e}", "red")

    
    def on_close(self):
        if self.scanning:
            if messagebox.askyesno("Scan in progress",
                                   "A scan is still active. Really stop it?"):
                self.scanning = False
                self.root.destroy()
        else:
            self.root.destroy()



def main():
    
    if not NMAP_AVAILABLE:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  NMAP IS NOT INSTALLED!                                 ║
║                                                            ║
║  Please install nmap:                                      ║
║    sudo apt update && sudo apt install nmap -y              ║
║                                                            ║
║  Then restart the tool.                                    ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        print("Start GUI anyway (scans will not work)...")

    if not HAS_NMAP_LIB:
        print("""
ℹ️  python-nmap library not found.
   Install them for better results:
     pip install python-nmap

   The tool also works without it (via subprocess).
""")

    root = tk.Tk()
    app = NmapHackerUI(root)

    
    try:
        
        pass
    except:
        pass

    root.mainloop()


if __name__ == "__main__":
    main()