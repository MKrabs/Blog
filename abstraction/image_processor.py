from PIL import Image, ImageOps


class ImageProcessor:
    @staticmethod
    def process(image_path):
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)

        h = img.height
        w = img.width

        if w > h:
            space_start = round((w - h) / 2)
            crop_area = (space_start, 0, space_start + h, h)
        else:
            space_start = round((h - w) / 2)
            crop_area = (0, space_start, w, space_start + w)

        img = img.crop(crop_area)
        img.save(image_path)
