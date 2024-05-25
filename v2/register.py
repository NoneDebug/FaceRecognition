import cv2
import face_recognition
import os
import json
from utils.Interceptor import get_name
from utils.preProcess import *
from utils.createPickle import *


def register_face():
    name = get_name()
    # 检查用户名是否已经存在
    if os.path.exists('Face lib/map.txt') and os.path.getsize('Face lib/map.txt') > 0:
        with open('Face lib/map.txt', 'r') as f:
            name_folder_map = json.load(f)
            if name in name_folder_map:
                print(f"用户名 {name} 已经注册过了。")
                return
            else:
                last_folder_code = max(name_folder_map.values())
                new_folder_code = last_folder_code + 1
    else:
        name_folder_map = {}
        new_folder_code = 0

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    count = 0

    while True:
        # 读取摄像头的图像
        ret, frame = cap.read()

        # 显示图像
        cv2.imshow('Register Face', frame)

        # 按 'q' 键退出循环，按 's' 键保存图像
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # 如果检测到人脸，保存图像
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                os.makedirs(f'Face lib/{new_folder_code}', exist_ok=True)
                cv2.imwrite(
                    f'Face lib/{new_folder_code}/{count}.jpg', frame)
                count += 1

                # 提醒用户调整脸部角度
                if count < 10:
                    print("请调整你的脸部角度，然后按 's' 键拍摄下一张照片。")

        # 如果已经拍摄了10张照片，退出循环
        if count >= 10:
            break

    # 释放摄像头
    cap.release()

    # 关闭所有 OpenCV 窗口
    cv2.destroyAllWindows()

    # 如果用户在拍摄10张照片之前退出，不保存用户信息
    if count < 10:
        return

    # 将姓名和文件夹编码的对应关系保存到map.txt文件中
    name_folder_map[name] = new_folder_code
    with open('Face lib/map.txt', 'w') as f:
        f.write(json.dumps(name_folder_map))

    # 数据预处理模块
    idx = new_folder_code
    preProcess(idx)

    # 保存特征向量
    createPickle(idx)


def registerFaceByGUI(queue, name):

    def update_output(text):
        while not queue.empty():
            queue.get()
        queue.put(text)

    # 检查并创建 map.txt 文件
    map_file_path = 'Face lib/map.txt'
    if not os.path.exists(map_file_path):
        os.makedirs('Face lib', exist_ok=True)
        with open(map_file_path, 'w') as f:
            json.dump({}, f)  # 写入一个空的字典

    # 检查用户名是否已经存在
    with open(map_file_path, 'r') as f:
        name_folder_map = json.load(f)

    if len(name_folder_map.keys()) > 0:

        if name in name_folder_map.keys():
            update_output(f"用户名 {name} 已经注册过了。")
            return
        else:
            last_folder_code = max(name_folder_map.values())
            new_folder_code = last_folder_code + 1
    else:
        name_folder_map = {}
        new_folder_code = 0

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        update_output("无法打开摄像头，请检查连接。")
        return

    count = 0

    update_output(
        "请调整你的脸部角度，然后按 's' 键拍摄下一张照片。\n按'q'键退出窗口。")

    while True:
        # 读取摄像头的图像
        ret, frame = cap.read()

        if not ret:
            update_output("程序暂时无法显示，请重启程序！")
            return

        # 显示图像
        cv2.imshow('Register Face', frame)
        # 按 'q' 键退出循环，按 's' 键保存图像
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # 如果检测到人脸，保存图像
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                os.makedirs(f'Face lib/{new_folder_code}', exist_ok=True)
                cv2.imwrite(
                    f'Face lib/{new_folder_code}/{count}.jpg', frame)
                count += 1

                # 提醒用户调整脸部角度
                if count < 10:
                    update_output(
                        f"第{count}/10 张,请调整你的脸部角度，然后按 's' 键拍摄下一张照片。")

        # 如果已经拍摄了10张照片，退出循环
        if count >= 10:
            break

    # 释放摄像头
    cap.release()

    # 关闭所有 OpenCV 窗口
    cv2.destroyAllWindows()

    # 如果用户在拍摄10张照片之前退出，不保存用户信息
    if count < 10:
        update_output("必须保存10张图片,注册失败!")
        return

    # 将姓名和文件夹编码的对应关系保存到map.txt文件中
    name_folder_map[name] = new_folder_code
    with open('Face lib/map.txt', 'w') as f:
        f.write(json.dumps(name_folder_map))

    update_output("请勿操作,保存中!")
    # 数据预处理模块
    idx = new_folder_code
    preProcess(idx)

    # 保存特征向量
    createPickle(idx)
    update_output("保存成功!")


if __name__ == "__main__":
    name = input("请输入你的姓名：")
    register_face(name)
