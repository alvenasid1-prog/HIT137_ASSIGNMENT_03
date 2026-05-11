import tkinter as tk

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spot the Difference")
        self.root.geometry("900x600") 

        self.canvas_left = tk.Canvas(self.root, width=400, height=400, bg="grey")
        self.canvas_right = tk.Canvas(self.root, width=400, height=400, bg="grey")

        self.canvas_left.grid(row=0, column=0, padx=10, pady=10)
        self.canvas_right.grid(row=0, column=1, padx=10, pady=10)

        self.button_load = tk.Button(self.root, text="Load Image")
        self.button_reveal = tk.Button(self.root, text="Reveal Differences")

        self.button_load.grid(row=1, column=0, pady=10)
        self.button_reveal.grid(row=1, column=1, pady=10)

        self.label_remaining = tk.Label(self.root, text="Remaining: 5", font=("Arial", 12))
        self.label_mistakes = tk.Label(self.root, text="Mistakes: 0", font=("Arial", 12))

        self.label_remaining.grid(row=2, column=0, pady=5)
        self.label_mistakes.grid(row=2, column=1, pady=5)

    def display_images(self, img_left, img_right):
        self.tk_left = img_left
        self.tk_right = img_right

        self.canvas_left.create_image(0, 0, anchor="nw", image=self.tk_left)
        self.canvas_right.create_image(0, 0, anchor="nw", image=self.tk_right)

    def run(self):
        self.root.mainloop()