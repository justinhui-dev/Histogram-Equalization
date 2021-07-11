import numpy as np
import cv2
from matplotlib import pyplot as plt

input_name = input("input image file name (e.g : *.jpg):")

if input_name == '': 
    input_name = 'default.jpg'

input_bgr = cv2.imread(input_name)
input_hsv = cv2.cvtColor(input_bgr, cv2.COLOR_BGR2HSV) 
object_hist = cv2.calcHist([input_hsv], [2], None, [256], [0, 256])
plt.plot(object_hist)

plt.title('Histogram')
plt.savefig('Hist.png')
plt.clf()

H, S, V = cv2.split(input_hsv)
Orig_hist, bins = np.histogram(V.flatten(), 256, [0, 255])

eq_array = Orig_hist.cumsum()
eq_array1 = np.ma.masked_equal(eq_array, 0)
eq_array1 = (eq_array1 - eq_array1.min()) * 255 / (eq_array1.max() - eq_array1.min())
eq_array = np.ma.filled(eq_array1, 0)

eq_V = eq_array[V.astype('uint8')]
eq_hist, bin = np.histogram(eq_V.flatten(), 256, [0, 256])

plt.plot(eq_hist)
plt.title('Equalized Histogram')
plt.savefig('Hist_Equalized.png')
plt.clf()

img_gl = cv2.imread(input_name,0)
height,width = img_gl.shape

img = V
for i in range(width):
    for j in range(height):
        img[j,i]= eq_V[j,i]

output_hsv_eq = cv2.merge([H, S, img])
eq_image = cv2.cvtColor(output_hsv_eq, cv2.COLOR_HSV2BGR)
cv2.imwrite('output.png', eq_image)
