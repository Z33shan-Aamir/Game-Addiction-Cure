import tkinter as tk
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def display_graph(root):
    graph_frame = ttk.Frame(master=root)
    graph_frame.pack(side="left", fill="both", expand=True)

    # Create a sample graph using matplotlib
    figure = Figure(figsize=(5, 3), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker="o")
    ax.set_title("Sample Graph")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    # Embed the graph in the Tkinter GUI
    canvas = FigureCanvasTkAgg(figure, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)