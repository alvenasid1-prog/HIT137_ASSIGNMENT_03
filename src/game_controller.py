# Jahid Hasan
# GameController
# Handles click detection, mistakes, reveal system and game state
class GameController:

    def __init__(self, gui, generator):

        self.gui = gui
        self.generator = generator

        self.found = 0
        self.mistakes = 0

        self.found_regions = []

    def on_click(self, event):

        x = event.x
        y = event.y

        region = self.check_difference(x, y)

        if region:

            self.mark_found(region)

        else:

            self.mistakes += 1

            print("Wrong Click")

            print("Mistakes:", self.mistakes)

            if self.mistakes >= 3:

                print("GAME OVER")

    def check_difference(self, x, y):

        for region in self.generator.differences:

            rx, ry, rw, rh = region

            if rx <= x <= rx + rw and ry <= y <= ry + rh:

                if region not in self.found_regions:

                    return region

        return None

    def mark_found(self, region):

        self.found += 1

        self.found_regions.append(region)

        print("FOUND!")

        print("Found:", self.found)

    def reveal_all(self):

        print("Reveal all differences")