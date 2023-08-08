import base64
import json
import pycocotools.mask as maskutil
from PIL import Image
import numpy as np


def convert_encoded_binary_mask_to_image(mask):
    image_array = maskutil.decode(mask)
    first_image_masks.append(image_array)
    print(type(first_image_masks[0]))
    print(image_array.shape)
    imagesize = mask_results["height"], mask_results["width"]
    x0, y0, x1, y1 = obj["bbox"]
    w, h = x1 - x0, y1 - y0
    mask = np.zeros(imagesize)
    print(w, h)
    mask[y0:y0 + h, x0:x0 + w] = image_array
    return mask


with open('input/64ca5412fbb8640014c9fcc2_objects.json') as maskfile:
    mask_results = json.load(maskfile)
    first_image_objects_encoded = mask_results["objects"]

    first_image_masks = []
    for obj in first_image_objects_encoded.values():
        encoded_mask = obj["rle"]
        encoded_mask["counts"] = base64.b64decode(encoded_mask["counts"])

        # convert json file into binary mask and fit it into original image
        image_mask = convert_encoded_binary_mask_to_image(encoded_mask)
        im = Image.fromarray(image_mask)
        im.save("output/binary_mask01.tif")

    print(f"Binary masks returned {len(first_image_masks)}")
