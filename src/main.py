import cv2
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class Difference:
    def __init__(self, x, y, size, alteration_type):
        self.x = x
        self.y = y
        self.size = size
        self.alteration_type = alteration_type
        self.found = False


class GameStats:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.mistakes = 0
        self.max_mistakes = 3
        self.total_differences = 5


class DifferenceGame:
    def __init__(self, root):

        self.root = root

        self.root.title("Spot the Difference Game")

        self.root.geometry("1500x800")

        self.root.configure(bg="#101010")

        # FIXED IMAGE PATH
        self.file_path = "src/img.jpg"

        self.stats = GameStats()

        self.original_clean = None
        self.original = None
        self.modified = None

        self.original_display = None
        self.modified_display = None

        self.differences = []

        self.create_ui()

        self.start_game()

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="SPOT THE DIFFERENCE",
            font=("Arial", 32, "bold"),
            fg="#00ffe5",
            bg="#101010"
        )

        title.pack(pady=12)

        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#101010",
            justify="center"
        )

        self.status_label.pack(pady=8)

        button_frame = tk.Frame(
            self.root,
            bg="#101010"
        )

        button_frame.pack(pady=8)

        self.reveal_btn = tk.Button(
            button_frame,
            text="Reveal",
            font=("Arial", 13, "bold"),
            width=14,
            bg="#ff0055",
            fg="white",
            relief="flat",
            command=self.reveal_answers
        )

        self.reveal_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        self.restart_btn = tk.Button(
            button_frame,
            text="Restart",
            font=("Arial", 13, "bold"),
            width=14,
            bg="#333333",
            fg="white",
            relief="flat",
            command=self.restart_game
        )

        self.restart_btn.grid(
            row=0,
            column=1,
            padx=10
        )

        image_frame = tk.Frame(
            self.root,
            bg="#101010"
        )

        image_frame.pack(pady=15)

        left_frame = tk.Frame(
            image_frame,
            bg="#202020",
            padx=10,
            pady=10
        )

        left_frame.grid(
            row=0,
            column=0,
            padx=18
        )

        right_frame = tk.Frame(
            image_frame,
            bg="#202020",
            padx=10,
            pady=10
        )

        right_frame.grid(
            row=0,
            column=1,
            padx=18
        )

        tk.Label(
            left_frame,
            text="Original Image",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=5)

        tk.Label(
            right_frame,
            text="Modified Image - Click Here",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=5)

        self.left_label = tk.Label(
            left_frame,
            bg="#111111"
        )

        self.left_label.pack()

        self.right_label = tk.Label(
            right_frame,
            bg="#111111"
        )

        self.right_label.pack()

        self.right_label.bind(
            "<Button-1>",
            self.check_click
        )

    def start_game(self):

        try:

            image = cv2.imread(self.file_path)

            if image is None:
                raise FileNotFoundError

            image = cv2.resize(
                image,
                (650, 420)
            )

            self.original_clean = image.copy()

            self.original = image.copy()

            self.modified = image.copy()

            self.differences = []

            self.stats.mistakes = 0

            self.generate_differences()

            self.update_images()

            self.update_status(
                "Find all 5 hidden differences."
            )

        except Exception:

            messagebox.showerror(
                "Image Error",
                "img.jpg not found inside src folder."
            )

    def generate_differences(self):

        height, width, _ = self.original.shape

        while len(self.differences) < self.stats.total_differences:

            size = random.randint(38, 52)

            x = random.randint(
                50,
                width - size - 50
            )

            y = random.randint(
                50,
                height - size - 50
            )

            if self.is_overlapping(x, y, size):
                continue

            alteration_type = random.choice([
                "brightness",
                "blur",
                "colour_shift"
            ])

            diff = Difference(
                x,
                y,
                size,
                alteration_type
            )

            self.differences.append(diff)

            self.apply_alteration(diff)

    def is_overlapping(self, x, y, size):

        for diff in self.differences:

            distance_x = abs(x - diff.x)

            distance_y = abs(y - diff.y)

            if distance_x < size + 55 and distance_y < size + 55:
                return True

        return False

    def apply_alteration(self, diff):

        x = diff.x
        y = diff.y
        size = diff.size

        area = self.modified[
            y:y + size,
            x:x + size
        ]

        if diff.alteration_type == "brightness":

            changed = cv2.convertScaleAbs(
                area,
                alpha=1.45,
                beta=35
            )

            self.modified[
                y:y + size,
                x:x + size
            ] = changed

        elif diff.alteration_type == "blur":

            changed = cv2.GaussianBlur(
                area,
                (31, 31),
                0
            )

            self.modified[
                y:y + size,
                x:x + size
            ] = changed

        elif diff.alteration_type == "colour_shift":

            area[:, :, 1] = cv2.add(
                area[:, :, 1],
                75
            )

            area[:, :, 2] = cv2.subtract(
                area[:, :, 2],
                25
            )

            self.modified[
                y:y + size,
                x:x + size
            ] = area

    def check_click(self, event):

        if self.stats.mistakes >= self.stats.max_mistakes:
            return

        clicked_correct = False

        for diff in self.differences:

            if diff.found:
                continue

            center_x = diff.x + diff.size // 2

            center_y = diff.y + diff.size // 2

            if abs(event.x - center_x) <= 45 and abs(event.y - center_y) <= 45:

                diff.found = True

                clicked_correct = True

                self.stats.score += 10

                self.draw_found_circle(diff)

                break

        if clicked_correct:

            if self.remaining_differences() == 0:

                self.update_status(
                    "Level completed!"
                )

                messagebox.showinfo(
                    "Winner",
                    f"You completed Level {self.stats.level}!"
                )

                self.stats.level += 1

                if self.stats.level <= 5:

                    self.restart_game()

                else:

                    messagebox.showinfo(
                        "Game Completed",
                        "Excellent! You completed all levels."
                    )

            else:

                self.update_status(
                    "Correct difference found!"
                )

        else:

            self.stats.mistakes += 1

            if self.stats.mistakes >= self.stats.max_mistakes:

                self.update_status(
                    "Game over. You made 3 mistakes."
                )

                messagebox.showwarning(
                    "Game Over",
                    "You made 3 mistakes."
                )

            else:

                self.update_status(
                    "Wrong click!"
                )

    def draw_found_circle(self, diff):

        center = (
            diff.x + diff.size // 2,
            diff.y + diff.size // 2
        )

        cv2.circle(
            self.original,
            center,
            28,
            (0, 0, 255),
            2
        )

        cv2.circle(
            self.modified,
            center,
            28,
            (0, 0, 255),
            2
        )

        self.update_images()

    def reveal_answers(self):

        if self.original is None or self.modified is None:
            return

        for diff in self.differences:

            if not diff.found:

                center = (
                    diff.x + diff.size // 2,
                    diff.y + diff.size // 2
                )

                cv2.circle(
                    self.original,
                    center,
                    28,
                    (255, 0, 0),
                    2
                )

                cv2.circle(
                    self.modified,
                    center,
                    28,
                    (255, 0, 0),
                    2
                )

        self.update_images()

        self.update_status(
            "Blue circles show the missing differences."
        )

    def restart_game(self):

        if self.original_clean is None:

            self.start_game()

            return

        self.original = self.original_clean.copy()

        self.modified = self.original_clean.copy()

        self.differences = []

        self.stats.mistakes = 0

        self.generate_differences()

        self.update_images()

        self.update_status(
            f"Level {self.stats.level} started."
        )

    def remaining_differences(self):

        count = 0

        for diff in self.differences:

            if not diff.found:
                count += 1

        return count

    def update_images(self):

        original_rgb = cv2.cvtColor(
            self.original,
            cv2.COLOR_BGR2RGB
        )

        modified_rgb = cv2.cvtColor(
            self.modified,
            cv2.COLOR_BGR2RGB
        )

        original_pil = Image.fromarray(
            original_rgb
        )

        modified_pil = Image.fromarray(
            modified_rgb
        )

        self.original_display = ImageTk.PhotoImage(
            original_pil
        )

        self.modified_display = ImageTk.PhotoImage(
            modified_pil
        )

        self.left_label.config(
            image=self.original_display
        )

        self.right_label.config(
            image=self.modified_display
        )

    def update_status(self, message):

        text = (
            f"LEVEL: {self.stats.level}   |   "
            f"SCORE: {self.stats.score}   |   "
            f"REMAINING: {self.remaining_differences()}   |   "
            f"MISTAKES: {self.stats.mistakes}/3\n\n"
            f"{message}"
        )

        self.status_label.config(
            text=text
        )


root = tk.Tk()

game = DifferenceGame(root)

root.mainloop()