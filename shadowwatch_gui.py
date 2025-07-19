import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import datetime

# ---------- UTILITIES ----------
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

def save_output(output_widget, tool_name):
    content = output_widget.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Save Failed", f"No content to save from {tool_name}.")
        return
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{tool_name.lower()}_{timestamp()}.txt"
    with open(filename, "w") as f:
        f.write(content)
    messagebox.showinfo("Saved", f"{tool_name} result saved to:\n{filename}")

# ---------- THEME SWITCH ----------
def toggle_theme():
    bg, fg = ("#121212", "#39ff14") if theme_var.get() == "Dark" else ("white", "black")
    root.configure(bg=bg)
    style.configure(".", background=bg, foreground=fg)
    for widget in [nmap_output, sherlock_output, whois_output]:
        widget.config(bg=bg, fg=fg, insertbackground=fg)

# ---------- NMAP SCAN ----------
def run_nmap():
    target = nmap_target.get().strip()
    if not target:
        nmap_output.insert(tk.END, "⚠️ Please enter a target.\n")
        return
    cmd = ["nmap"]
    if var_sV.get(): cmd.append("-sV")
    if var_O.get(): cmd.append("-O")
    if var_p.get(): cmd.extend(["-p", "1-1000"])
    if var_A.get(): cmd.append("-A")
    cmd.append(target)

    nmap_output.delete("1.0", tk.END)
    nmap_output.insert(tk.END, f"🔍 Running: {' '.join(cmd)}\n\n")

    def run():
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            nmap_output.insert(tk.END, result + "\n")
        except subprocess.CalledProcessError as e:
            nmap_output.insert(tk.END, f"❌ Error:\n{e.output}\n")
        nmap_output.see(tk.END)

    threading.Thread(target=run).start()

# ---------- SHERLOCK SCAN ----------
def run_sherlock():
    username = sherlock_entry.get().strip()
    if not username:
        sherlock_output.insert(tk.END, "⚠️ Please enter a username.\n")
        return

    sherlock_output.delete("1.0", tk.END)
    sherlock_output.insert(tk.END, f"🔎 Searching for username: {username}\n\n")
    search_button.config(state="disabled")

    def run():
        try:
            sherlock_cli = os.path.join("venv", "bin", "sherlock")
            if not os.path.exists(sherlock_cli):
                sherlock_output.insert(tk.END, "❌ Sherlock not found in venv/bin/sherlock\n")
                return
            result = subprocess.run(
                [sherlock_cli, "--no-color", username],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            output = result.stdout.strip()
            if output:
                sherlock_output.insert(tk.END, "\n✅ Scan complete!\n\n" + output + "\n")
            else:
                sherlock_output.insert(tk.END, "\n⚠️ No results found.\n")
        except Exception as e:
            sherlock_output.insert(tk.END, f"\n❌ Error:\n{str(e)}\n")
        finally:
            search_button.config(state="normal")
            sherlock_output.see(tk.END)

    threading.Thread(target=run).start()

# ---------- WHOIS LOOKUP ----------
def run_whois():
    domain = whois_entry.get().strip()
    if not domain:
        whois_output.insert(tk.END, "⚠️ Please enter a domain or IP.\n")
        return

    whois_output.delete("1.0", tk.END)
    whois_output.insert(tk.END, f"🌐 WHOIS Lookup for: {domain}\n\n")

    def run():
        try:
            result = subprocess.run(["whois", domain], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            whois_output.insert(tk.END, result.stdout)
        except Exception as e:
            whois_output.insert(tk.END, f"\n❌ Error:\n{str(e)}\n")
        whois_output.see(tk.END)

    threading.Thread(target=run).start()

# ---------- GUI ----------
root = tk.Tk()
root.title("🛡️ ShadowWatch: Personal Threat Intelligence")
root.geometry("1000x740")

style = ttk.Style()
style.theme_use("clam")

# Theme toggle
theme_var = tk.StringVar(value="Dark")
theme_frame = ttk.Frame(root)
theme_frame.pack(pady=5, anchor="ne", padx=10)
ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
ttk.OptionMenu(theme_frame, theme_var, "Dark", "Dark", "Light", command=lambda _: toggle_theme()).pack(side=tk.LEFT)

# Tabs
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

# ---------- NMAP TAB ----------
nmap_tab = ttk.Frame(tabs)
tabs.add(nmap_tab, text="🛰️ Nmap Scanner")
ttk.Label(nmap_tab, text="🎯 Enter Target IP / Hostname:").pack(pady=5)
nmap_target = ttk.Entry(nmap_tab, width=60)
nmap_target.pack(pady=5)

options_frame = ttk.LabelFrame(nmap_tab, text="Nmap Options")
options_frame.pack(pady=10)
var_sV = tk.BooleanVar()
var_O = tk.BooleanVar()
var_p = tk.BooleanVar()
var_A = tk.BooleanVar()
ttk.Checkbutton(options_frame, text="Version Detection (-sV)", variable=var_sV).pack(anchor='w')
ttk.Checkbutton(options_frame, text="OS Detection (-O)", variable=var_O).pack(anchor='w')
ttk.Checkbutton(options_frame, text="Port Scan (-p 1-1000)", variable=var_p).pack(anchor='w')
ttk.Checkbutton(options_frame, text="Aggressive Scan (-A)", variable=var_A).pack(anchor='w')

ttk.Button(nmap_tab, text="🚀 Start Nmap Scan", command=run_nmap).pack(pady=10)
nmap_output = scrolledtext.ScrolledText(nmap_tab, wrap=tk.WORD, width=120, height=25, font=("Courier", 10))
nmap_output.pack()
ttk.Button(nmap_tab, text="💾 Save Nmap Results", command=lambda: save_output(nmap_output, "nmap")).pack(pady=10)

# ---------- SHERLOCK TAB ----------
sherlock_tab = ttk.Frame(tabs)
tabs.add(sherlock_tab, text="🕵️ Sherlock Username Scan")
ttk.Label(sherlock_tab, text="👤 Enter Username:").pack(pady=5)
sherlock_entry = ttk.Entry(sherlock_tab, width=50)
sherlock_entry.pack(pady=5)
search_button = ttk.Button(sherlock_tab, text="🔍 Search Username", command=run_sherlock)
search_button.pack(pady=10)
sherlock_output = scrolledtext.ScrolledText(sherlock_tab, wrap=tk.WORD, width=120, height=25, font=("Courier", 10))
sherlock_output.pack()
ttk.Button(sherlock_tab, text="💾 Save Sherlock Results", command=lambda: save_output(sherlock_output, "sherlock")).pack(pady=10)

# ---------- WHOIS TAB ----------
whois_tab = ttk.Frame(tabs)
tabs.add(whois_tab, text="🌐 WHOIS Lookup")
ttk.Label(whois_tab, text="🔗 Enter Domain or IP:").pack(pady=5)
whois_entry = ttk.Entry(whois_tab, width=60)
whois_entry.pack(pady=5)
ttk.Button(whois_tab, text="🔍 Run WHOIS Lookup", command=run_whois).pack(pady=10)
whois_output = scrolledtext.ScrolledText(whois_tab, wrap=tk.WORD, width=120, height=25, font=("Courier", 10))
whois_output.pack()
ttk.Button(whois_tab, text="💾 Save WHOIS Results", command=lambda: save_output(whois_output, "whois")).pack(pady=10)

# ---------- Final Setup ----------
toggle_theme()
root.mainloop()
