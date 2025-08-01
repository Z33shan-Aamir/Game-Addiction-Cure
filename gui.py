# library imports
import tkinter as tk
import ttkbootstrap as ttk
# local imports
from components import app_list, graph

def main():
    root = ttk.Window(themename="cyborg")
    root.geometry("800x400")
    root.title("Game Addiction Cure")
    

    # Create a main frame to hold both the app list and the graph
    main_frame = ttk.Frame(master=root)
    main_frame.pack(fill="both", expand=True)

    # Add the app list to the left side
    app_list.list_apps(main_frame)

    # Add the graph to the right side
    graph.display_graph(main_frame)

    root.mainloop()

main()