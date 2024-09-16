from draw64.image import Image


class ImageIDAlreadyExistsException(Exception):
    pass


class ImageCollection:
    def __init__(self):
        self._images: dict[str, Image] = {}

    def __len__(self):
        return len(self._images)

    def __iter__(self):
        return iter(self._images)

    def __contains__(self, image_id: str):
        return image_id in self._images

    def __getitem__(self, image_id: str):
        return self._images[image_id]

    def __delitem__(self, image_id: str):
        del self._images[image_id]

    def values(self):
        return self._images.values()

    def create_image(self, image_id: str | None = None) -> Image:
        if image_id and image_id in self:
            raise ImageIDAlreadyExistsException(image_id)
        image = Image(image_id=image_id) if image_id else Image()
        self._images[image.image_id] = image
        return image