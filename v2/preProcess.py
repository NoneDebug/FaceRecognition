import cv2
import numpy as np
import os.path
import json


def darker(image, percetage=0.9):
    image_copy = image.copy()
    w = image.shape[1]
    h = image.shape[0]
    # get darker
    for xi in range(0, w):
        for xj in range(0, h):
            image_copy[xj, xi, 0] = int(image[xj, xi, 0]*percetage)
            image_copy[xj, xi, 1] = int(image[xj, xi, 1]*percetage)
            image_copy[xj, xi, 2] = int(image[xj, xi, 2]*percetage)
    return image_copy

# 亮度 n


def brighter(image, percetage=1.5):
    image_copy = image.copy()
    w = image.shape[1]
    h = image.shape[0]
    # get brighter
    for xi in range(0, w):
        for xj in range(0, h):
            image_copy[xj, xi, 0] = np.clip(
                int(image[xj, xi, 0]*percetage), a_max=255, a_min=0)
            image_copy[xj, xi, 1] = np.clip(
                int(image[xj, xi, 1]*percetage), a_max=255, a_min=0)
            image_copy[xj, xi, 2] = np.clip(
                int(image[xj, xi, 2]*percetage), a_max=255, a_min=0)
    return image_copy


def count_users():
    with open('Face lib/map.txt', 'r') as f:
        name_folder_map = json.load(f)
    user_count = len(name_folder_map)
    return user_count


def preProcess(idx):

    # 图片文件夹路径
    file_dir = f"./Face lib//{idx}//"
    if not os.path.exists(file_dir):
        print("{idx}文件夹不存在！")

    for img_name in os.listdir(file_dir):
        img_path = file_dir + img_name
        img = cv2.imread(img_path)

        img_name_without_ext = os.path.splitext(img_name)[0]
        # 变暗
        img_darker = darker(img)
        cv2.imwrite(file_dir + img_name_without_ext +
                    '_darker.jpg', img_darker)

        # 变亮
        img_brighter = brighter(img)
        cv2.imwrite(file_dir + img_name_without_ext +
                    '_brighter.jpg', img_brighter)

        # 高斯模糊
        blur = cv2.GaussianBlur(img, (7, 7), 1.5)
        #      cv2.GaussianBlur(图像，卷积核，标准差）
        cv2.imwrite(file_dir + img_name_without_ext + '_blur.jpg', blur)


def preProcessFor():

    if not os.path.exists('Face lib/map.txt'):
        print("map.txt文件不存在")
        return
    user_count = count_users()
    for idx in range(user_count):
        # 图片文件夹路径
        file_dir = f"./Face lib//{idx}//"

        for img_name in os.listdir(file_dir):
            img_path = file_dir + img_name
            img = cv2.imread(img_path)

            img_name_without_ext = os.path.splitext(img_name)[0]
            # 变暗
            img_darker = darker(img)
            cv2.imwrite(file_dir + img_name_without_ext +
                        '_darker.jpg', img_darker)

            # 变亮
            img_brighter = brighter(img)
            cv2.imwrite(file_dir + img_name_without_ext +
                        '_brighter.jpg', img_brighter)

            # 高斯模糊
            blur = cv2.GaussianBlur(img, (7, 7), 1.5)
            #      cv2.GaussianBlur(图像，卷积核，标准差）
            cv2.imwrite(file_dir + img_name_without_ext + '_blur.jpg', blur)


if __name__ == "__main__":
    preProcessFor()
