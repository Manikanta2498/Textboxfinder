import numpy as np
import argparse
import imutils
import cv2

def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

def box_extraction(img_for_box_extraction_path, cropped_dir_path):
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    mani = cv2.imread(img_for_box_extraction_path, 1)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  
    # cv2.imwrite("./output/Image_bin.jpg",img_bin)
   
    hor_kernel_length = np.array(img).shape[1]//40
    ver_kernel_length = np.array(img).shape[0]//40
     
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, ver_kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hor_kernel_length, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # cv2.imwrite("./output/verticle_lines.jpg",verticle_lines_img)
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # cv2.imwrite("./output/horizontal_lines.jpg",horizontal_lines_img)
# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    # img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=0)
    # (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    cv2.imwrite("./output/img_final_bin.jpg",img_final_bin)
    kernel = np.ones((3,3),np.uint8)
    # opening = cv2.morphologyEx(img_final_bin, cv2.MORPH_OPEN, kernel)
    dilated = cv2.dilate(img_final_bin,kernel,iterations = 3)
    # eroded = cv2.erode(dilated,kernel,iterations = 3)
    
    cv2.imwrite("./output/dilated.jpg",dilated)
    # Find contours for image, which will detect all the boxes
    img, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    final = cv2.drawContours(mani, contours, -1, (0,255,0), 3)
    cv2.imshow('Boxes',final)
    cv2.waitKey(0)
    # Sort all the contours by top to bottom.
#     (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
#     idx = 0
#     for c in contours:
#         # Returns the location and width,height for every contour
#         x, y, w, h = cv2.boundingRect(c)
# # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
#         if (w > 80 and h > 5) and w > 3*h:
#             idx += 1
#             new_img = img[y:y+h, x:x+w]
#             cv2.imwrite(cropped_dir_path+str(idx) + '.png', new_img)

for i in range(1,5):
    box_extraction("./input/"+str(i)+".png", "./output/")
    box_extraction("./input/"+str(i)+".jpg", "./output/")