import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Create the main window
root = tk.Tk()
root.title("ShadowWatch - Sherlock Scanner")
root.geometry("700x500")
root.config(bg="#1e1e1e")

# Header label
tk.Label(root, text="ShadowWatch - Sherlock", font=("Helvetica", 20, "bold"),
         fg="#00ffcc", bg="#1e1e1e").pack(pady=10)

# Username input
tk.Label(root, text="Enter Username:", font=("Helvetica", 12),
         fg="white", bg="#1e1e1e").pack()
sherlock_entry = tk.Entry(root, width=40, font=("Helvetica", 12))
sherlock_entry.pack(pady=5)

# Output box
tk.Label(root, text="Scan Output:", font=("Helvetica", 12),
         fg="white", bg="#1e1e1e").pack()
sherlock_output = scrolledtext.ScrolledText(root, height=15, width=80, font=("Courier", 10))
sherlock_output.pack(pady=10)

# Sherlock runner function
def run_sherlock():
    username = sherlock_entry.get().strip()
    if not username:
        messagebox.showerror("Input Error", "Please enter a username.")
        return

    # Set path to sherlock.py
    sherlock_path = os.path.join("sherlock", "sherlock.py")
    if not os.path.exists(sherlock_path):
        messagebox.showerror("Error", f"Sherlock not found at: {sherlock_path}")
        return

    # Run Sherlock using subprocess
    try:
        sherlock_output.delete("1.0", tk.END)
        sherlock_output.insert(tk.END, f"🔎 Searching for username: {username}\n\n")

        result = subprocess.run(
            ["python3", sherlock_path, username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            sherlock_output.insert(tk.END, "❌ Error:\n" + result.stderr)
        else:
            sherlock_output.insert(tk.END, "✅ Results:\n" + result.stdout)

    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

# Button to run Sherlock
tk.Button(root, text="Run Sherlock", font=("Helvetica", 12),
          command=run_sherlock, bg="#00cc66", fg="white", padx=10, pady=5).pack(pady=5)

# Start the GUI loop
root.mainloop()
