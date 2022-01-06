
    # plt.figure(figsize=(20, 20))
    # plt.subplot(3, 2, 1)
    # plt.title("Original")
    # plt.imshow(image)
    # plt.subplot(3, 2, 2)
    # plt.title("Sobel X")
    # plt.imshow(x_sobel)
    # plt.subplot(3, 2, 3)
    # plt.title("Sobel Y")
    # plt.imshow(y_sobel)
    # sobel_or = cv2.bitwise_or(x_sobel, y_sobel)
    # plt.subplot(3, 2, 4)
    # plt.imshow(sobel_or)
    # laplacian = cv2.Laplacian(image, cv2.CV_64F)
    # plt.subplot(3, 2, 5)
    # plt.title("Laplacian")
    # plt.imshow(laplacian)
    # ## There are two values: threshold1 and threshold2.
    # ## Those gradients that are greater than threshold2 => considered as an edge
    # ## Those gradients that are below threshold1 => considered not to be an edge.
    # ## Those gradients Values that are in between threshold1 and threshold2 => either classiﬁed as edges or non-edges
    # # The first threshold gradient
    # canny = cv2.Canny(image, 50, 120)
    # plt.subplot(3, 2, 6)
    # plt.imshow(canny)
import cv2
import numpy as np
# from deepface import DeepFace
# print("Turning on your camera...")
# faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
# print("Analyzing your live facial sentiments!")
print("Cam on!")
while True:
    try:
        ret, img = cap.read()

        img = cv2.blur(img, (20,20))



        cv2.imshow('Original Video', img)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(e)

cv2.destroyAllWindows()
cap.release()
