import face_recognition
import os
import pickle
import json


def count_users():
    with open('Face lib/map.txt', 'r') as f:
        name_folder_map = json.load(f)
    user_count = len(name_folder_map)
    return user_count


def createPickle(idx):
    # TODO: Has not been implemented
    # 图片文件夹路径
    file_dir = f"./Face lib//{idx}//"
    # 检查文件夹是否存在
    if not os.path.exists(file_dir):
        return -1

    person_codes = []
    for img_name in os.listdir(file_dir):
        face_path = file_dir + img_name
        face_img = face_recognition.load_image_file(face_path)
        single_codes = face_recognition.face_encodings(face_img)
        if len(single_codes) != 0:
            person_codes.append(single_codes[0])

    if not os.path.exists('./Face lib/facedata.pkl'):
        faces_codes = []
    else:
        with open('./Face lib/facedata.pkl', 'rb') as f:
            faces_codes = pickle.load(f)

    faces_codes.append(person_codes)

    with open('./Face lib/facedata.pkl', 'wb') as f:
        pickle.dump(faces_codes, f)


def createPickleForAll():

    if not os.path.exists('Face lib/map.txt'):
        print("map.txt文件不存在")
        return
    user_count = count_users()

    faces_codes = []

    for idx in range(user_count):
        # 图片文件夹路径
        file_dir = f"./Face lib//{idx}//"
        person_codes = []
        for img_name in os.listdir(file_dir):
            face_path = file_dir + img_name
            face_img = face_recognition.load_image_file(face_path)
            single_codes = face_recognition.face_encodings(face_img)
            if len(single_codes) != 0:
                person_codes.append(single_codes[0])
        faces_codes.append(person_codes)

    output = open('./Face lib/facedata.pkl', 'wb')
    pickle.dump(faces_codes, output)
    output.close()


if __name__ == "__main__":
    createPickleForAll()
