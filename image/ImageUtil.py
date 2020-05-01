from PIL import Image, ImageFont, ImageDraw
from pathlib import Path


class ImageUtil:

    def __init__(self, image_path):
        self.imagePath = Path(image_path)
        self.image = Image.open(self.imagePath)

    def getImage(self):
        return self.image

    def getHeightAndWidth(self):
        return self.getImage().size

    def getSize(self):
        return self.getImage()

    # @Todo Amir Move this to another class
    def watermark(self, watermark_text, save_to):
        font = ImageFont.truetype('font.ttf', 22)

        width, height = self.getHeightAndWidth()

        # Determining Watermark position
        position_left = int((width * 2) / 100)
        position_top = height - int((height * 2) / 100) - 100

        # Creating Background image for watermark text
        background_image_size = (int((width * 20) / 100), 100)
        text_background = Image.new('RGB', background_image_size, (255, 255, 255))

        drawing = ImageDraw.Draw(text_background)
        drawing.text((10, 30), watermark_text, fill=(10, 50, 100), font=font)

        self.getImage().paste(text_background, (position_left, position_top))

        # @TODO Return Image resource instead of saving from here
        self.getImage().save(save_to)
