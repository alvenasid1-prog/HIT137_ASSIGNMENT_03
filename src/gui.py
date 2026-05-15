import tkinter as tk

class GameGUI:

    def __init__(self):

        self.tk_left = None

        self.tk_right = None

        self.root = tk.Tk()

        self.root.title("Spot the Difference Game")

        self.root.configure(bg="#101010")

        self.root.state("zoomed")

        self.title_label = tk.Label(

            self.root,

            text="SPOT THE DIFFERENCE",

            font=("Arial", 34, "bold"),

            fg="#00ffe5",

            bg="#101010"

        )

        self.title_label.pack(pady=20)

        self.info_frame = tk.Frame(self.root, bg="#101010")

        self.info_frame.pack(pady=10)

        self.label_remaining = tk.Label(

            self.info_frame,

            text="Remaining: 5",

            font=("Arial", 16, "bold"),

            fg="white",

            bg="#101010"

        )

        self.label_remaining.grid(row=0, column=0, padx=25)

        self.label_mistakes = tk.Label(

            self.info_frame,

            text="Mistakes: 0",

            font=("Arial", 16, "bold"),

            fg="white",

            bg="#101010"

        )

        self.label_mistakes.grid(row=0, column=1, padx=25)

        self.button_frame = tk.Frame(self.root, bg="#101010")

        self.button_frame.pack(pady=10)

        self.button_load = tk.Button(

            self.button_frame,

            text="Restart",

            font=("Arial", 14, "bold"),

            width=14,

            bg="#333333",

            fg="white",

            relief="flat",

            cursor="hand2"

        )

        self.button_load.grid(row=0, column=0, padx=20)

        self.button_reveal = tk.Button(

            self.button_frame,

            text="Reveal",

            font=("Arial", 14, "bold"),

            width=14,

            bg="#ff0055",

            fg="white",

            relief="flat",

            cursor="hand2"

        )

        self.button_reveal.grid(row=0, column=1, padx=20)

        self.image_frame = tk.Frame(self.root, bg="#101010")

        self.image_frame.pack(pady=20)

        self.left_panel = tk.Frame(self.image_frame, bg="#202020", padx=15, pady=15)

        self.left_panel.grid(row=0, column=0, padx=40)

        self.left_title = tk.Label(

            self.left_panel,

            text="Original Image",

            font=("Arial", 18, "bold"),

            fg="white",

            bg="#202020"

        )

        self.left_title.pack(pady=10)

        self.canvas_left = tk.Canvas(

            self.left_panel,

            width=450,

            height=450,

            bg="#111111",

            highlightthickness=0

        )

        self.canvas_left.pack()

        self.right_panel = tk.Frame(self.image_frame, bg="#202020", padx=15, pady=15)

        self.right_panel.grid(row=0, column=1, padx=40)

        self.right_title = tk.Label(

            self.right_panel,

            text="Modified Image - Click Here",

            font=("Arial", 18, "bold"),

            fg="white",

            bg="#202020"

        )

        self.right_title.pack(pady=10)

        self.canvas_right = tk.Canvas(

            self.right_panel,

            width=450,

            height=450,

            bg="#111111",

            highlightthickness=0

        )

        self.canvas_right.pack()

    def display_images(self, img_left, img_right):

        self.tk_left = img_left

        self.tk_right = img_right

        self.canvas_left.delete("all")

        self.canvas_right.delete("all")

        self.canvas_left.create_image(0, 0, anchor="nw", image=self.tk_left)

        self.canvas_right.create_image(0, 0, anchor="nw", image=self.tk_right)

    def run(self):

        self.root.mainloop()