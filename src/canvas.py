import tkinter as tk


def create_canvas(frame: tk.Tk) -> tk.Canvas:
    width = 700
    height = width
    circle_diameter = width // 10
    canvas = tk.Canvas(frame, width=width, height=height, bg="#881177")
    canvas.pack()
    for i in range(0, width, width // 10):
        for j in range(0, height, height // 10):
            canvas.create_oval(
                i,
                j,
                i + circle_diameter,
                j + circle_diameter,
                fill=f"#{(i * 10) // width}{(j * 10) // height}5",
            )
    return canvas
