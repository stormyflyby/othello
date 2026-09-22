import tkinter as tk

from canvas import create_canvas


# Display the game
def display() -> None:
    root = tk.Tk()
    create_canvas(root)

    root.mainloop()
