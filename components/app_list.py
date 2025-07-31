import tkinter as tk
import ttkbootstrap as ttk

def list_apps(root):
    app_list_frame = ttk.Frame(master=root)
    app_list_label = ttk.Label(master=app_list_frame, text="List of apps", font="Ariel 16")
    app_list_label.pack()
    app_list_frame.pack()