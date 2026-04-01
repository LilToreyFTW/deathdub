#!/usr/bin/env python3
"""
Minimal test script to isolate ordinal error issues
"""

import tkinter as tk
from tkinter import ttk, messagebox

def test_minimal():
    root = tk.Tk()
    root.title("Test - v3.1.0")
    root.geometry("400x300")
    
    # Test basic tkinter functionality
    label = ttk.Label(root, text="Testing v3.1.0 Build", font=('Arial', 14))
    label.pack(pady=20)
    
    def test_imports():
        try:
            import requests
            messagebox.showinfo("Success", "requests module imported successfully!")
        except ImportError as e:
            messagebox.showerror("Error", f"requests import failed: {e}")
    
    button = ttk.Button(root, text="Test Requests Import", command=test_imports)
    button.pack(pady=10)
    
    # Test basic functionality
    def test_basic():
        try:
            import hashlib
            import uuid
            import json
            import base64
            messagebox.showinfo("Success", "All basic modules imported!")
        except Exception as e:
            messagebox.showerror("Error", f"Basic import failed: {e}")
    
    button2 = ttk.Button(root, text="Test Basic Modules", command=test_basic)
    button2.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_minimal()
