"""
HIT137 – Group Assignment 3
Image Processing Module
Author: Nahidul
"""

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
        self.clone_image()
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
                rx1, ry1, rx2, ry2 = reg["region"]
                if not (new_region[2] + 10 < rx1 or
                        new_region[0] > rx2 + 10 or
                        new_region[3] + 10 < ry1 or
                        new_region[1] > ry2 + 10):
                    overlap = True
                    break

            if not overlap:
                alteration = random.choice([
                    'colour_shift',
                    'blur',
                    'shape',
                    'brightness',
                    'pixelate'
                ])

                if alteration == 'colour_shift':
                    self.apply_colour_shift(new_region)
                elif alteration == 'blur':
                    self.apply_blur(new_region)
                elif alteration == 'shape':
                    self.apply_shape_overlay(new_region)
                elif alteration == 'brightness':
                    self.apply_brightness(new_region)
                else:
                    self.apply_pixelate(new_region)

                # Store as dict so GUI can track found/not-found
                self.differences.append({
                    "region": new_region,
                    "found": False,
                    "alteration": alteration
                })

            attempts += 1

        return self.differences

    def apply_colour_shift(self, region):
        x1, y1, x2, y2 = region
        area = self.cloned_image[y1:y2, x1:x2].copy()
        area[:, :, 1] = cv2.add(area[:, :, 1], 60)
        area[:, :, 2] = cv2.subtract(area[:, :, 2], 30)
        self.cloned_image[y1:y2, x1:x2] = area  # fixed: reassign

    def apply_blur(self, region):
        x1, y1, x2, y2 = region
        roi = self.cloned_image[y1:y2, x1:x2]
        self.cloned_image[y1:y2, x1:x2] = cv2.GaussianBlur(
            roi, (21, 21), 0
        )

    def apply_shape_overlay(self, region):
        x1, y1, x2, y2 = region
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        cv2.circle(
            self.cloned_image,
            (cx, cy),
            20,
            (0, 200, 0),
            -1
        )

    def apply_brightness(self, region):
        x1, y1, x2, y2 = region
        area = self.cloned_image[y1:y2, x1:x2]
        self.cloned_image[y1:y2, x1:x2] = cv2.convertScaleAbs(
            area, alpha=1.5, beta=40
        )

    def apply_pixelate(self, region):
        x1, y1, x2, y2 = region
        area = self.cloned_image[y1:y2, x1:x2]
        small = cv2.resize(area, (10, 10))
        self.cloned_image[y1:y2, x1:x2] = cv2.resize(
            small, (x2 - x1, y2 - y1),
            interpolation=cv2.INTER_NEAREST
        )

    def draw_circle_on(self, img, region, color):
        x1, y1, x2, y2 = region
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        cv2.circle(img, (cx, cy), 42, color, 3)
        return img