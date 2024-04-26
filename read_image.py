import cv2 as cv
import os

# Load the image
absolute_path = os.path.join(os.getcwd(), 'image_data', 'lena.jpg')
print(os.path.isfile(absolute_path))
image = cv.imread(absolute_path)
print(image)

# Display the image
cv.imshow("Image", image)

# Wait for the user to press a key
cv.waitKey(0)

# Close all windows
cv.destroyAllWindows()
