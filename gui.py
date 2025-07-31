# library imports
import tkinter as tk
import ttkbootstrap as ttk
# local imports
from components import app_list


def main():
    root = ttk.Window(themename="cyborg")
    root.geometry("600x350")
    root.title("Game Addiction Cure")
    hero_frame = ttk.Frame(master=root)
    text_hero_frame = ttk.Label(master=hero_frame, text="Game Addiction Cure", font="Calibri 24 bold")
    text_hero_frame.pack()
    hero_frame.pack()
    app_list.list_apps(root)
    
    root.mainloop()
    
main()