from skimage import measure


def binary_mask_to_polygons(binary_mask):
    # Find contours in the binary mask
    contours = measure.find_contours(binary_mask)

    # The function may return multiple contours for disjoint regions
    # In this example, we assume there is only one contour
    print(f"Contours returned: {len(contours)}")

    # Convert the contour points to a polygon
    polygons = []
    for contour in contours:
        # Convert the contour points to a polygon
        polygon = [(int(point[1]), int(point[0])) for point in contour]
        polygons.append(polygon)

    return polygons
