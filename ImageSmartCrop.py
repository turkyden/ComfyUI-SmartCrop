from .SmartCrop import SmartCrop
from PIL import Image, ImageDraw
import torch
import numpy as np


# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
    
class ImageSmartCrop:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "stroke_width": ("INT", {
                    "default": 1024, 
                    "min": 0, #Minimum value
                    "max": 2048, #Maximum value
                    "step": 1, #Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
                "stroke_height": ("INT", {
                    "default": 1024, 
                    "min": 0, #Minimum value
                    "max": 2048, #Maximum value
                    "step": 1, #Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
            },
        }

    CATEGORY = "👽 ComfyLab/📐 SmartCrop 智能裁剪"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "imageSmartCrop"

    def imageSmartCrop(self, image, stroke_width, stroke_height):
        cropper = SmartCrop()
        image = tensor2pil(image)
        result = cropper.crop(image, stroke_width, stroke_height)
        box = (
            result['top_crop']['x'],
            result['top_crop']['y'],
            result['top_crop']['width'] + result['top_crop']['x'],
            result['top_crop']['height'] + result['top_crop']['y']
        )
        cropped_image = image.crop(box)
        image_tensor = pil2tensor(cropped_image)
        return (image_tensor,)