from .configs import *

CONTACT_PATH = "static/configs/contact.json"
IMAGE_FOLDER = "static/images"

validate_paths([CONTACT_PATH, IMAGE_FOLDER])

__all__ = ["CONTACT_PATH", "IMAGE_FOLDER"]