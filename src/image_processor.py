"""
image_processor.py
------------------
HIT137 Assignment 3 — Group Member: Alve
Role: ImageProcessor Base Class

This module defines the ImageProcessor class which handles all core
image operations: loading, cloning, converting, and resizing.
It serves as the base (parent) class for DifferenceGenerator.
"""

import cv2
import numpy as np
from PIL import Image, ImageTk


class ImageProcessor:
    """
    A base class for loading, cloning, and converting images.

    This class provides core image-handling functionality using OpenCV
    and Pillow. It is designed to be inherited by DifferenceGenerator.

    Attributes:
        image (numpy.ndarray): The original image loaded from disk (BGR format).
        cloned_image (numpy.ndarray): A deep copy of the original image.
        supported_formats (tuple): File extensions supported for loading.
    """

    # Class-level constant: supported image file formats
    SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp")

    def __init__(self):
        """
        Constructor — initialise ImageProcessor with empty image attributes.

        Instance variables:
            self.image         -- stores the original loaded image
            self.cloned_image  -- stores the modified copy of the image
        """
        self.image = None
        self.cloned_image = None

    def __str__(self):
        """
        Return a human-readable string representation of the ImageProcessor.

        Useful for debugging — prints image dimensions if loaded,
        or a message if no image has been loaded yet.

        Returns:
            str: A string describing the current state of the object.
        """
        if self.image is not None:
            h, w = self.image.shape[:2]
            return f"ImageProcessor — Image loaded: {w}x{h} pixels"
        return "ImageProcessor — No image loaded"

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def load_image(self, path):
        """
        Load an image from disk using OpenCV.

        Supports JPG, JPEG, PNG, and BMP file formats.
        Resets cloned_image whenever a new image is loaded.

        Args:
            path (str): File path to the image on disk.

        Returns:
            numpy.ndarray: The loaded image in BGR colour format,
                           or None if loading fails.
        """
        try:
            # Check the file extension is supported
            lower_path = path.lower()
            if not any(lower_path.endswith(fmt) for fmt in self.SUPPORTED_FORMATS):
                raise ValueError(
                    f"Unsupported format. Supported types: {self.SUPPORTED_FORMATS}"
                )

            # Load the image using OpenCV
            img = cv2.imread(path)

            if img is None:
                raise FileNotFoundError(
                    f"Could not read image at: '{path}'. "
                    "Check the file exists and is not corrupted."
                )

            # Store the image and reset the clone
            self.image = img
            self.cloned_image = None
            return self.image

        except (ValueError, FileNotFoundError) as e:
            print(f"[ImageProcessor] Error loading image: {e}")
            return None

        except Exception as e:
            print(f"[ImageProcessor] Unexpected error: {e}")
            return None

    def clone_image(self):
        """
        Create an exact deep copy of the original loaded image.

        The cloned copy is stored in self.cloned_image and is used by
        DifferenceGenerator to apply alterations without affecting the original.

        Returns:
            numpy.ndarray: A deep copy of the original image,
                           or None if no image is loaded.
        """
        try:
            if self.image is None:
                raise RuntimeError(
                    "No image is loaded. Call load_image() before clone_image()."
                )

            self.cloned_image = self.image.copy()
            return self.cloned_image

        except RuntimeError as e:
            print(f"[ImageProcessor] Error cloning image: {e}")
            return None

    def convert_to_tk(self, img, canvas_width=500, canvas_height=500):
        """
        Convert an OpenCV image to a Tkinter-compatible PhotoImage.

        Converts the colour format from BGR (OpenCV) to RGB (PIL/Tkinter),
        then resizes the image to fit the canvas while preserving aspect ratio.

        Conversion pipeline:
            OpenCV BGR -> RGB -> PIL Image -> Resized -> Tkinter PhotoImage

        Args:
            img (numpy.ndarray): An OpenCV image in BGR format.
            canvas_width (int): Target display width in pixels (default 500).
            canvas_height (int): Target display height in pixels (default 500).

        Returns:
            ImageTk.PhotoImage: A Tkinter-compatible image object,
                                or None if conversion fails.
        """
        try:
            if img is None:
                raise ValueError("Cannot convert a None image to Tkinter format.")

            # Step 1: Convert BGR (OpenCV) -> RGB (standard colour order)
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Step 2: Convert numpy array -> PIL Image
            pil_image = Image.fromarray(rgb_image)

            # Step 3: Resize to fit canvas while preserving aspect ratio
            pil_image = self._resize_with_aspect_ratio(
                pil_image, canvas_width, canvas_height
            )

            # Step 4: Convert PIL Image -> Tkinter PhotoImage
            tk_image = ImageTk.PhotoImage(pil_image)
            return tk_image

        except ValueError as e:
            print(f"[ImageProcessor] Conversion error: {e}")
            return None

        except Exception as e:
            print(f"[ImageProcessor] Unexpected error during conversion: {e}")
            return None

    def is_loaded(self):
        """
        Check whether an image has been successfully loaded.

        Returns:
            bool: True if an image is currently loaded, False otherwise.
        """
        return self.image is not None

    def get_dimensions(self):
        """
        Return the width and height of the currently loaded image.

        Returns:
            tuple: (width, height) in pixels, or (0, 0) if no image is loaded.
        """
        if self.image is not None:
            h, w = self.image.shape[:2]
            return (w, h)
        return (0, 0)

    # ------------------------------------------------------------------
    # Private Helper Method
    # ------------------------------------------------------------------

    def _resize_with_aspect_ratio(self, pil_image, target_width, target_height):
        """
        Resize a PIL Image to fit within target dimensions without distortion.

        Calculates a uniform scale factor so the image fits inside the
        bounding box defined by target_width x target_height.

        Args:
            pil_image (PIL.Image.Image): The PIL image to resize.
            target_width (int): Maximum allowed width in pixels.
            target_height (int): Maximum allowed height in pixels.

        Returns:
            PIL.Image.Image: The resized PIL image.
        """
        original_width, original_height = pil_image.size

        # Calculate scale factor to fit within the canvas
        scale_w = target_width / original_width
        scale_h = target_height / original_height
        scale = min(scale_w, scale_h)  # Use the smaller scale to keep aspect ratio

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        return pil_image.resize((new_width, new_height), Image.LANCZOS)