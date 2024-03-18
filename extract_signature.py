import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.measure import regionprops
import numpy as np

def extract_signature(source_image):
    constant_parameter_1 = 84
    constant_parameter_2 = 250
    constant_parameter_3 = 100
    constant_parameter_4 = 18
    # read the input image
    img = source_image
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    blobs = img > img.mean()
    blobs_labels = measure.label(blobs, background=1)
    fig, ax = plt.subplots(figsize=(10, 6))
    the_biggest_component = 0
    total_area = 0
    counter = 0
    average = 0.0
    for region in regionprops(blobs_labels):
        if (region.area > 10):
            total_area = total_area + region.area
            counter = counter + 1
        # take regions with large enough areas
        if (region.area >= 250):
            if (region.area > the_biggest_component):
                the_biggest_component = region.area

    average = (total_area/counter)
    a4_small_size_outliar_constant = ((average/constant_parameter_1)*constant_parameter_2)+constant_parameter_3
    a4_big_size_outliar_constant = a4_small_size_outliar_constant*constant_parameter_4
    pre_version = morphology.remove_small_objects(blobs_labels, a4_small_size_outliar_constant)
    component_sizes = np.bincount(pre_version.ravel())
    too_small = component_sizes > (a4_big_size_outliar_constant)
    too_small_mask = too_small[pre_version]
    pre_version[too_small_mask] = 0
    plt.imsave('pre_version.png', pre_version)
    img = cv2.imread('pre_version.png', 0)
    # ensure binary
    img = cv2.threshold(img, 0, 255,
                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    return img

def cut_bottom_right_corner(image_path, corner_width, corner_height):
    # Read the image
    img = cv2.imread(image_path)

    # Get image dimensions
    height, width = img.shape[:2]

    # Define the coordinates for the bottom right corner
    x0 = width - corner_width
    y0 = height - corner_height

    # Crop the image
    cropped_img = img[y0:height, x0:width]
    cv2.imwrite(r"images/signature/cropped_image.png", cropped_img)

    


    # Display or save the cropped image
    #cv2.imshow('Cropped Image', cropped_img)
    #cv2.waitKey(0)
    # If you want to save the cropped image:


def extract_sign(image_path):
    inputImg= cv2.imread(fr"{image_path}")
    if inputImg is not None:
        gray=cv2.cvtColor(inputImg,cv2.COLOR_BGR2GRAY)
        img=extract_signature(gray)
        cv2.imwrite(r"images/signature/signature_extracted.jpg", img)
        print("- step2 (signature extractor): OK")

    #cut signature for function
    # Example usage:
    image_path = r"images/signature/signature_extracted.jpg"
    corner_width = 500  # Width of the bottom right corner to be cut
    corner_height = 500  # Height of the bottom right corner to be cut
    cut_bottom_right_corner(image_path, corner_width, corner_height)


