import cv2
from scipy import ndimage
import matplotlib.pyplot as plt
from super_gradients.training import models
import torch
import os

DEVICE = 'cuda' if torch.cuda.is_available() else "cpu"
model_path = '/home/bazilyq/Рабочий стол/MLSD/photo_anonymization/telegram_bot/models'
best_model = models.get(
    'yolo_nas_l',
    num_classes=1,
    checkpoint_path=f"{model_path}/average_model.pth"
).to(DEVICE)


def rotate_image(input_path='input_photo', output_path='output_photo', show=False):
    in_photo_path = f'{input_path}/image.jpg'
    out_photo_path = f'{output_path}/image.jpg'

    image = cv2.imread(in_photo_path)
    rotated = ndimage.rotate(image, 90)

    cv2.imwrite(out_photo_path, rotated)

    if show:
        plt.imshow(rotated)
        plt.show()


def get_blure_image(predict):
    img = predict._images_prediction_lst[0].image.copy()

    for bb in predict._images_prediction_lst[0].prediction.bboxes_xyxy:
        bb = list(bb)

        x = bb[0]
        y = bb[1]
        width = bb[2] - x
        height = bb[3] - y

        blur_x = int(x)
        blur_y = int(y)
        blur_width = int(width)
        blur_height = int(height)

        roi = img[blur_y:blur_y+blur_height, blur_x:blur_x+blur_width]
        blur_image = cv2.GaussianBlur(roi,(51,51),0)

        img[blur_y:blur_y+blur_height, blur_x:blur_x+blur_width] = blur_image

    return img


def detect_face(input_path='telegram_bot/input_photo', output_path='telegram_bot/output_photo', show=False):
    in_photo_path = f'{input_path}/image.jpg'
    predict = best_model.predict(in_photo_path)
    blured_img = get_blure_image(predict)
    cv2.imwrite(f"{output_path}/image.jpg", blured_img)

