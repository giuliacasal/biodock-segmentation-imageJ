import base64
import binascii
import json
import pycocotools.mask as maskutil

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
        first_image_masks.append(maskutil.decode(encoded_mask))

    print(f"Binary masks returned {len(first_image_masks)}")

    polygon_output = binary_mask_to_polygons(first_image_masks[0])

    print(polygon_output)

    save_fiji_format(polygon_output)

    # print_hex(first_image_masks)
