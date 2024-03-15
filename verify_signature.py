import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

def removeWhiteSpace(img):
    # img = cv2.imread('ws.png') # Read in the image and convert to grayscale
    if img is not None:
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
    print("IN")
    if img1 is not None and img2 is not None:
        print("IN 2")
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # resize images for comparison
        img1 = cv2.resize(img1, (300, 300))
        img2 = cv2.resize(img2, (300, 300))
        # display both images
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        similarity_value = "{:.2f}".format(ssim(img1, img2,gaussian_weights = True,sigma= 1.2,use_sample_covariance = False)*100)
        print("done")
        return float(similarity_value)



path1 = '/Users/asvikamahesh/Documents/Developer/signature_verifier/modules/cropped_image copy.png'
path2 = '/Users/asvikamahesh/Documents/Developer/signature_verifier/modules/cropped_image.png'
similarity_value = match(path1,path2)
print(similarity_value)