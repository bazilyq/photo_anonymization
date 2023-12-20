import cv2
from scipy import ndimage
import matplotlib.pyplot as plt


def rotate_image(input_path='input_photo', output_path='output_photo', show=False):
    in_photo_path = f'{input_path}/image.jpg'
    out_photo_path = f'{output_path}/image.jpg'

    image = cv2.imread(in_photo_path)
    rotated = ndimage.rotate(image, 90)

    cv2.imwrite(out_photo_path, rotated)

    if show:
        plt.imshow(rotated)
        plt.show()
