import cv2

def cut_top_left_corner(image_path, corner_width, corner_height):
    # Read the image
    img = cv2.imread(image_path)

    # Define the coordinates for the top left corner
    x0 = 0
    y0 = 0
    x1 = corner_width
    y1 = corner_height

    # Crop the image
    cropped_left = img[y0:y1, x0:x1]

    # Display or save the cropped image
    cv2.imwrite("cropped_left.png", cropped_left)

    # If you want to save the cropped image:
    # cv2.imwrite("cropped_image.png", cropped_img)

# Example usage:
image_path = "/content/depositCheque1.jpg"
corner_width = 75  # Width of the top left corner to be cut
corner_height = 50  # Height of the top left corner to be cut
cut_top_left_corner(image_path, corner_width, corner_height)


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
        # print region.area # (for debugging)
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
    plt.imsave('pre_version_leftcorner.png', pre_version)
    img = cv2.imread('pre_version_leftcorner.png', 0)
    # ensure binary
    img = cv2.threshold(img, 0, 255,
                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    return img
inputImg= cv2.imread(r"/content/cropped_left.png")
gray=cv2.cvtColor(inputImg,cv2.COLOR_BGR2GRAY)
img=extract_signature(gray)
cv2.imwrite("line_cropped_left.jpg", img)
print("Cropped left corner OK!!!")

import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
# TODO add contour detection for enhanced accuracy

def removeWhiteSpace(img):
    # img = cv2.imread('ws.png') # Read in the image and convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
    coords = cv2.findNonZero(gray) # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
    rect = img[y:y+h, x:x+w]
    return rect

def match(path1, path2):
    # read the images
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    img1 = removeWhiteSpace(img1)
    img2 = removeWhiteSpace(img2)
    # turn images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # resize images for comparison
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    # display both images
    #cv2.imshow("One", img1)
    #cv2.imshow("Two", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    similarity_value = "{:.2f}".format(ssim(img1, img2,gaussian_weights = True,sigma= 1.2,use_sample_covariance = False)*100)
    # print("answer is ", float(similarity_value),
    #       "type=", type(similarity_value))
    return float(similarity_value)

path1 = '/content/line_cropped_left.jpg'
path2 = '/content/topleft.PNG'
similarity_value = match(path1,path2)
print(similarity_value)