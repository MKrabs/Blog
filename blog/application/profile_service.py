from abstraction.image_processor import ImageProcessor


class ProfileService:
    def __init__(self):
        self.image_processor = ImageProcessor()

    def save_profile(self, profile, new_image=False):
        profile.save()

        if new_image:
            processed_image_path = self.image_processor.process(profile.picture.path)
            profile.picture = processed_image_path
            profile.save()
