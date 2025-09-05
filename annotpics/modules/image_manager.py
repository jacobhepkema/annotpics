from PIL import ImageTk, Image

class ImageManager:
    def __init__(self, resize_w, resize_h):
        self.resize_w = resize_w
        self.resize_h = resize_h
        self._cache = {}

    def get_image(self, image_path):
        if image_path in self._cache:
            return self._cache[image_path]

        try:
            img = Image.open(image_path)
            img = img.resize((self.resize_w, self.resize_h))
            photo_img = ImageTk.PhotoImage(img)
            self._cache[image_path] = photo_img
            return photo_img
        except FileNotFoundError:
            # Return a placeholder image if the file is not found
            return self.get_placeholder_image()
        except Exception as e:
            import logging
            logging.warning(f"Error loading image {image_path}: {e}")
            return self.get_placeholder_image()

    def get_placeholder_image(self):
        # Create a blank black image
        img = Image.new('RGB', (self.resize_w, self.resize_h), 'black')
        # You can add text to the image to indicate an error
        # from PIL import ImageDraw
        # draw = ImageDraw.Draw(img)
        # draw.text((10, 10), "Image not found", fill="white")
        photo_img = ImageTk.PhotoImage(img)
        # Don't cache the placeholder image in the main cache, but we can have a separate cache for it
        if "placeholder" not in self._cache:
            self._cache["placeholder"] = photo_img
        return self._cache["placeholder"]
