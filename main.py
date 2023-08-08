import base64
import binascii
import json
import pycocotools.mask as maskutil
from PIL import Image
import numpy as np

from polygon_scikit import binary_mask_to_polygons


def print_hex(masks):
    for mask in masks:
        print(binascii.hexlify(bytearray(mask)))


def save_fiji_format(polygons):
    # Save the polygons to a FIJI X Y Coordinate file
    with open("output/Coordinates.txt", 'w') as f:
        f.write('X\tY\n')  # Write column headers

        for polygon in polygons:
            for x, y in polygon:
                f.write(f'{x}\t{y}\n')


with open('input/64ca5412fbb8640014c9fcc2_objects.json') as maskfile:
    mask_results = json.load(maskfile)
    first_image_objects_encoded = mask_results["objects"]

    first_image_masks = []
    for obj in first_image_objects_encoded.values():
        encoded_mask = obj["rle"]
        encoded_mask["counts"] = base64.b64decode(encoded_mask["counts"])

        image_array = maskutil.decode(encoded_mask)
        first_image_masks.append(image_array)
        print(type(first_image_masks[0]))
        print(image_array.shape)
        imagesize = mask_results["width"], mask_results["height"]
        x0, y0, x1, y1 = obj["bbox"]
        w, h = x1 - x0, y1 - y0
        mask = np.zeros(imagesize)
        print(w, h)
        mask[y0:y0+h, x0:x0+w] = image_array

        im = Image.fromarray(mask)
        im.save("output/binary_mask.tif")

    print(f"Binary masks returned {len(first_image_masks)}")

    polygon_output = binary_mask_to_polygons(first_image_masks[0])

    print(polygon_output)

    save_fiji_format(polygon_output)
