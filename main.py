import base64
import json
import pycocotools.mask as maskutil
from PIL import Image
import numpy as np
import os


def convert_encoded_binary_mask_to_image(mask, first_image_masks, width, height, bbox):
    # convert json file into binary mask and fit it into original image
    image_array = maskutil.decode(mask)
    first_image_masks.append(image_array)
    print(type(first_image_masks[0]))
    print(image_array.shape)
    imagesize = height, width
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0
    mask = np.zeros(imagesize)
    print(w, h)
    mask[y0:y0 + h, x0:x0 + w] = image_array
    return mask


def convert_binary_mask_file_to_tif(file_name, output_path):
    with open(file_name) as maskfile:
        print(maskfile)
        mask_results = json.load(maskfile)
        first_image_objects_encoded = mask_results["objects"]
        if not first_image_objects_encoded:
            imagesize = mask_results["height"], mask_results["width"]
            mask = np.zeros(imagesize)
            im = Image.fromarray(mask)
            im.save(output_path + "mask-" + mask_results["filename"])

        first_image_masks = []
        for obj in first_image_objects_encoded.values():
            encoded_mask = obj["rle"]
            encoded_mask["counts"] = base64.b64decode(encoded_mask["counts"])

            image_mask = convert_encoded_binary_mask_to_image(
                encoded_mask, first_image_masks, mask_results["width"],
                mask_results["height"], obj["bbox"])

            im = Image.fromarray(image_mask)
            im.save(output_path + "mask-" + mask_results["filename"])

    print(f"Binary masks returned {len(first_image_masks)}")


def read_binary_mask_files_for_dir(directory_path):
    file_list = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            file_list.append(filename)
    return file_list


def create_binary_masks(input_path, output_path):
    binary_mask_files = read_binary_mask_files_for_dir(input_path)
    for binary_mask_file in binary_mask_files:
        if not binary_mask_file.endswith('.json'):
            continue
        print(binary_mask_file)
        convert_binary_mask_file_to_tif(input_path + binary_mask_file, output_path)


create_binary_masks('input/J7784 bv1 nuclei masks data/', 'output/')
