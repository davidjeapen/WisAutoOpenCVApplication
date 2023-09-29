import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

# approximate RGB color of cone in image
cone_color = [200, 17, 29]


# Helper method to find hsv color range close to given rgb value
def get_color_limits(color):
    np_color = np.uint8([[color]])
    hsc_c = cv2.cvtColor(np_color, cv2.COLOR_RGB2HSV)

    lower_color = (hsc_c[0][0][0] - 10, 100, 100)
    upper_color = (hsc_c[0][0][0] + 10, 255, 255)

    lower_color = np.array(lower_color, dtype=np.uint8)
    upper_color = np.array(upper_color, dtype=np.uint8)
    return lower_color, upper_color


# Loads desired image
img = cv2.imread("red.png")
img_h, img_w, img_c = img.shape

# Converts BGR images to HSV for processing
# and RGB for displaying
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Gets a range of HSV color values which could be a cone
lower_orange, upper_orange = get_color_limits(color=cone_color)

# Finds all pixels in range
mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

# Calculates boundaries of various regions of orange pixels (cones)
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

left_x = []
right_x = []

left_y = []
right_y = []

# Collects the x and y values
# for detections of each half of screen
for i, c in enumerate(contours):
    x, y, w, h = cv2.boundingRect(c)
    # cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 5)
    if x < img_w/2 and y > img_h/4:
        left_x.append(x)
        left_y.append(y)
    elif x > img_w/2 and y > img_h/4:
        right_x.append(x)
        right_y.append(y)

# Calculates linear regression of the cones on left and right side
slopeL, interceptL, _, _, _ = stats.linregress(left_x, left_y)
slopeR, interceptR, _, _, _ = stats.linregress(right_x, right_y)

# Calculates corresponding y values for each edge of image
left_line_y = [slopeL * 0 + interceptL, slopeL * img_w + interceptL]
right_line_y = [slopeR * 0 + interceptR, slopeR * img_w + interceptR]

# Graphs the linear regressions for each line of cones
plt.plot([0, img_w], left_line_y, color='red')
plt.plot([0, img_w], right_line_y, color='red')

plt.subplot(1, 1, 1)
# Displays image
plt.imshow(img_rgb)
plt.show()
