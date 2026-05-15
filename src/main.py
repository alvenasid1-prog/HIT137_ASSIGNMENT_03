import cv2
import random
from tkinter import messagebox
from PIL import Image, ImageTk

from gui import GameGUI


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

    def __init__(self):

        self.gui = GameGUI()

        self.file_path = "src/img.jpg"

        self.stats = GameStats()

        self.original_clean = None
        self.original = None
        self.modified = None

        self.original_display = None
        self.modified_display = None

        self.differences = []

        self.start_game()

        self.gui.canvas_right.bind(
            "<Button-1>",
            self.check_click
        )

        self.gui.button_reveal.config(
            command=self.reveal_answers
        )

        self.gui.button_load.config(
            command=self.restart_game
        )

        self.gui.run()

    def start_game(self):

        image = cv2.imread(self.file_path)

        if image is None:

            messagebox.showerror(
                "Image Error",
                "img.jpg not found inside src folder."
            )

            return

        image = cv2.resize(
            image,
            (400, 400)
        )

        self.original_clean = image.copy()

        self.original = image.copy()

        self.modified = image.copy()

        self.differences = []

        self.stats.mistakes = 0

        self.generate_differences()

        self.update_images()

        self.update_labels()

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

            overlap = False

            for diff in self.differences:

                if abs(x - diff.x) < 60 and abs(y - diff.y) < 60:

                    overlap = True

                    break

            if overlap:
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

            self.stats.mistakes += 1

            if self.stats.mistakes >= self.stats.max_mistakes:

                messagebox.showwarning(
                    "Game Over",
                    "You made 3 mistakes."
                )

        self.update_labels()

    def draw_found_circle(self, diff):

        center = (
            diff.x + diff.size // 2,
            diff.y + diff.size // 2
        )

        cv2.circle(
            self.original,
            center,
            25,
            (0, 0, 255),
            2
        )

        cv2.circle(
            self.modified,
            center,
            25,
            (0, 0, 255),
            2
        )

        self.update_images()

    def reveal_answers(self):

        for diff in self.differences:

            if not diff.found:

                center = (
                    diff.x + diff.size // 2,
                    diff.y + diff.size // 2
                )

                cv2.circle(
                    self.original,
                    center,
                    25,
                    (255, 0, 0),
                    2
                )

                cv2.circle(
                    self.modified,
                    center,
                    25,
                    (255, 0, 0),
                    2
                )

        self.update_images()

    def restart_game(self):

        self.original = self.original_clean.copy()

        self.modified = self.original_clean.copy()

        self.differences = []

        self.stats.mistakes = 0

        self.generate_differences()

        self.update_images()

        self.update_labels()

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

        self.gui.display_images(
            self.original_display,
            self.modified_display
        )

    def update_labels(self):

        self.gui.label_remaining.config(
            text=f"Remaining: {self.remaining_differences()}"
        )

        self.gui.label_mistakes.config(
            text=f"Mistakes: {self.stats.mistakes}"
        )


game = DifferenceGame()