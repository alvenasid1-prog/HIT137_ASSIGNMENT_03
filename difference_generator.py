import cv2
import random
from PIL import Image, ImageTk


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.cloned_image = None

    def load_image(self, path):
        self.image = cv2.imread(path)
        return self.image

    def clone_image(self):
        self.cloned_image = self.image.copy()
        return self.cloned_image

    def convert_to_tk(self, img, width, height):
        img_resized = cv2.resize(img, (width, height))
        rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        return ImageTk.PhotoImage(pil)


class DifferenceGenerator(ImageProcessor):
    def __init__(self):
        super().__init__()
        self.differences = []

    def generate_differences(self):
        self.differences = []
        h, w = self.cloned_image.shape[:2]
        region_size = 60
        attempts = 0

        while len(self.differences) < 5 and attempts < 1000:
            x = random.randint(0, w - region_size)
            y = random.randint(0, h - region_size)
            new_region = (x, y, x + region_size, y + region_size)

            overlap = False
            for reg in self.differences:
                if not (new_region[2] < reg[0] or new_region[0] > reg[2] or
                        new_region[3] < reg[1] or new_region[1] > reg[3]):
                    overlap = True
                    break

            if not overlap:
                alteration = random.choice(['colour_shift', 'blur', 'shape'])
                self.differences.append(new_region)
                if alteration == 'colour_shift':
                    self.apply_colour_shift(new_region)
                elif alteration == 'blur':
                    self.apply_blur(new_region)
                else:
                    self.apply_shape_overlay(new_region)

            attempts += 1

        return self.differences

    def apply_colour_shift(self, region):
        x1, y1, x2, y2 = region
        self.cloned_image[y1:y2, x1:x2, 2] = \
            cv2.add(self.cloned_image[y1:y2, x1:x2, 2], 60)

    def apply_blur(self, region):
        x1, y1, x2, y2 = region
        roi = self.cloned_image[y1:y2, x1:x2]
        self.cloned_image[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (15, 15), 0)

    def apply_shape_overlay(self, region):
        x1, y1, x2, y2 = region
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(self.cloned_image, (cx, cy), 20, (0, 255, 0), -1)