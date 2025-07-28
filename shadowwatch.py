import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

root = tk.Tk()
root.title("ShadowWatch - Personal Threat Intelligence")
root.geometry("800x600")
root.config(bg="#1e1e1e")

# ----------------------- Tabs ----------------------
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Style
style = ttk.Style()
style.theme_use('default')
style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
style.configure("TNotebook.Tab", background="#333", foreground="#fff", padding=10)
style.map("TNotebook.Tab", background=[("selected", "#00cc66")])

# ---------- Sherlock Tab ----------
frame1 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame1, text='Sherlock')

tk.Label(frame1, text="Enter Username:", font=("Helvetica", 12),
         fg="white", bg="#1e1e1e").pack()
sherlock_entry = tk.Entry(frame1, width=40, font=("Helvetica", 12))
sherlock_entry.pack(pady=5)

sherlock_output = scrolledtext.ScrolledText(frame1, height=20, width=90, font=("Courier", 10))
sherlock_output.pack(pady=10)

def run_sherlock():
    username = sherlock_entry.get().strip()
    if not username:
        messagebox.showerror("Input Error", "Please enter a username.")
        return
    sherlock_path = os.path.join("sherlock", "sherlock.py")
    if not os.path.exists(sherlock_path):
        messagebox.showerror("Error", f"Sherlock not found at: {sherlock_path}")
        return
    sherlock_output.delete("1.0", tk.END)
    sherlock_output.insert(tk.END, f"🔎 Searching for username: {username}\n\n")
    result = subprocess.run(["python3", sherlock_path, username],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        sherlock_output.insert(tk.END, "❌ Error:\n" + result.stderr)
    else:
        sherlock_output.insert(tk.END, "✅ Results:\n" + result.stdout)

tk.Button(frame1, text="Run Sherlock", command=run_sherlock,
          bg="#00cc66", fg="white", font=("Helvetica", 12)).pack()

# ---------- Nmap Tab ----------
frame2 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame2, text='Nmap')

tk.Label(frame2, text="Enter Target IP/Domain:", fg="white", bg="#1e1e1e").pack()
nmap_entry = tk.Entry(frame2, width=40)
nmap_entry.pack(pady=5)

scan_type = tk.StringVar(value="Simple")
tk.Radiobutton(frame2, text="Simple", variable=scan_type, value="Simple", bg="#1e1e1e", fg="white").pack()
tk.Radiobutton(frame2, text="Port Scan (-p-)", variable=scan_type, value="Port", bg="#1e1e1e", fg="white").pack()
tk.Radiobutton(frame2, text="Version Detection (-sV)", variable=scan_type, value="Version", bg="#1e1e1e", fg="white").pack()

nmap_output = scrolledtext.ScrolledText(frame2, height=20, width=90, font=("Courier", 10))
nmap_output.pack(pady=10)

def run_nmap():
    target = nmap_entry.get().strip()
    if not target:
        messagebox.showerror("Input Error", "Please enter a target.")
        return
    nmap_output.delete("1.0", tk.END)
    nmap_output.insert(tk.END, f"🔎 Scanning {target}...\n\n")

    cmd = ["nmap", target]
    if scan_type.get() == "Port":
        cmd = ["nmap", "-p-", target]
    elif scan_type.get() == "Version":
        cmd = ["nmap", "-sV", target]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        nmap_output.insert(tk.END, "❌ Error:\n" + result.stderr)
    else:
        nmap_output.insert(tk.END, "✅ Results:\n" + result.stdout)

tk.Button(frame2, text="Run Nmap", command=run_nmap,
          bg="#00cc66", fg="white", font=("Helvetica", 12)).pack()

# ---------- WHOIS Tab ----------
frame3 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame3, text='WHOIS Lookup')

tk.Label(frame3, text="Enter Domain:", fg="white", bg="#1e1e1e").pack()
whois_entry = tk.Entry(frame3, width=40)
whois_entry.pack(pady=5)

whois_output = scrolledtext.ScrolledText(frame3, height=20, width=90, font=("Courier", 10))
whois_output.pack(pady=10)

def run_whois():
    domain = whois_entry.get().strip()
    if not domain:
        messagebox.showerror("Input Error", "Please enter a domain.")
        return
    whois_output.delete("1.0", tk.END)
    whois_output.insert(tk.END, f"🔍 Performing WHOIS lookup for {domain}...\n\n")
    result = subprocess.run(["whois", domain],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        whois_output.insert(tk.END, "❌ Error:\n" + result.stderr)
    else:
        whois_output.insert(tk.END, "✅ Results:\n" + result.stdout)

tk.Button(frame3, text="Run WHOIS", command=run_whois,
          bg="#00cc66", fg="white", font=("Helvetica", 12)).pack()

# ---------- Save Results ----------
def save_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write("---- Sherlock Output ----\n")
            f.write(sherlock_output.get("1.0", tk.END))
            f.write("\n---- Nmap Output ----\n")
            f.write(nmap_output.get("1.0", tk.END))
            f.write("\n---- WHOIS Output ----\n")
            f.write(whois_output.get("1.0", tk.END))
        messagebox.showinfo("Saved", f"Results saved to {file_path}")

tk.Button(root, text="💾 Save All Results", command=save_results,
          bg="#3333cc", fg="white", font=("Helvetica", 12)).pack(pady=10)

# ---------- Start GUI ----------
root.mainloop()
