
import random
import sys
import tkinter as tk

# Rain Drops — Windows Screensaver
# CorruptedConsciousness

FONT_SIZE = 18
COLUMN_SPACING = 17
FRAME_DELAY = 40

COLORS = [
    "#003300",
    "#005500",
    "#008800",
    "#00aa00",
    "#00cc00",
    "#00ff00",
    "#99ff99",
    "#ffffff",
]


class RainDrops:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor="none")

        self.canvas = tk.Canvas(
            self.root,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.root.update_idletasks()

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.columns = []
        self.frame = 0
        self.running = True
        self.start_mouse = None

        for x in range(0, self.width, COLUMN_SPACING):
            self.columns.append({
                "x": x,
                "y": random.randint(-self.height, 0),
                "speed": random.randint(1, 4),
                "length": random.randint(12, 35),
            })

        self.root.bind("<KeyPress>", self.exit)
        self.root.bind("<ButtonPress>", self.exit)
        self.root.bind("<Motion>", self.mouse_moved)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.root.after(FRAME_DELAY, self.animate)
        self.root.mainloop()

    def exit(self, event=None):
        if self.running:
            self.running = False
            self.root.destroy()

    def mouse_moved(self, event):
        position = (event.x_root, event.y_root)

        if self.start_mouse is None:
            self.start_mouse = position
            return

        dx = abs(position[0] - self.start_mouse[0])
        dy = abs(position[1] - self.start_mouse[1])

        if dx > 8 or dy > 8:
            self.exit()

    def animate(self):
        if not self.running:
            return

        self.canvas.delete("all")
        self.frame += 1

        for column in self.columns:
            if self.frame % column["speed"] == 0:
                column["y"] += FONT_SIZE

            x = column["x"]
            head_y = column["y"]

            for i in range(column["length"]):
                y = head_y - i * FONT_SIZE

                if y < 0 or y >= self.height:
                    continue

                digit = str(random.randint(0, 1))

                color_index = max(
                    0,
                    len(COLORS) - 1 -
                    int(i / column["length"] * len(COLORS))
                )

                self.canvas.create_text(
                    x,
                    y,
                    text=digit,
                    fill=COLORS[color_index],
                    font=("Consolas", FONT_SIZE, "bold"),
                )

            if head_y - column["length"] * FONT_SIZE > self.height:
                column["y"] = random.randint(-500, -20)
                column["speed"] = random.randint(1, 4)
                column["length"] = random.randint(12, 35)

        self.root.after(FRAME_DELAY, self.animate)


def main():
    args = [arg.lower() for arg in sys.argv[1:]]

    if not args or args[0] in ("/s", "-s"):
        RainDrops()

    elif args[0] in ("/c", "-c"):
        # Configuration dialog will be added later.
        root = tk.Tk()
        root.withdraw()
        from tkinter import messagebox
        messagebox.showinfo(
            "Rain Drops",
            "Rain Drops screensaver\n"
            "No configuration options yet."
        )
        root.destroy()

    elif args[0] in ("/p", "-p"):
        # Windows preview embedding is not implemented yet.
        pass

    else:
        RainDrops()


if __name__ == "__main__":
    main()
