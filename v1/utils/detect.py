import face_recognition
import cv2
import numpy as np
import pickle
import json
import os
import dlib
from imutils import face_utils

# 初始眨眼次数
blink_total = 0
mouth_total = 0
pic_total = 0
blink_counter = 0
mouth_status_open = 0

# 眼长宽比例值
EAR_THRESH = 0.25
EAR_CONSEC_FRAMES_MIN = 1
EAR_CONSET_FRAMES_MAX = 9  # 当EAR小于阈值时，连接多少帧一定发生眨眼动作

# 嘴长宽比例值
MAR_THRESH = 0.15

# 人脸检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    "face_recognition_models/models/shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]


def detect():

    video_capture = cv2.VideoCapture(0)

    pkl_file = open('Face lib/facedata.pkl', 'rb')
    all_known_face_encodings = pickle.load(pkl_file)
    pkl_file.close()

    with open('Face lib/map.txt', 'r') as f:
        name_folder_map = json.load(f)

    names = list(name_folder_map.keys())

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:

        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                min_dis = 10000.0  # 初始化为最大值
                name = names[0]
                # See if the face is a match for the known face(s)
                name = "Unknown"
                idx = -1
                for i in range(len(all_known_face_encodings)):
                    # name = "Unknown"
                    face_dis = face_recognition.face_distance(
                        all_known_face_encodings[i], face_encoding)
                    # If a match was found in known_face_encodings, just use the first one.
                    # min_dis = min(np.mean(face_dis),min_dis)
                    if face_dis.shape[0] != 0:
                        face_mean = np.mean(face_dis)
                        if face_mean != 0 and face_mean < min_dis:
                            min_dis = face_mean
                            name = names[i]
                if min_dis > 0.5:  # 阈值可调
                    name = "Unknown"
                face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)

            font = cv2.FONT_HERSHEY_DUPLEX
            if name == "Unknown":
                cv2.putText(frame, 'Unknown', (left + 6, bottom - 6),
                            font, 1.0, (255, 255, 255), 1)
            else:
                if name == "唐钰渤":
                    cv2.putText(frame, 'Yubo Tang', (left + 6, bottom - 6),
                                font, 1.0, (255, 255, 255), 1)
                elif name == "高梦圆":
                    cv2.putText(frame, 'MenYuan Gao', (left + 6, bottom - 6),
                                font, 1.0, (255, 255, 255), 1)
                # cv2.putText(frame, 'User', (left + 6, bottom - 6),
                #             font, 1.0, (255, 255, 255), 1)
                face_names.append('User')

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Release handle to the webcam
            video_capture.release()
            cv2.destroyAllWindows()
            break

    if "User" in face_names:
        return True

    return False

# 眼长宽比例


def eye_aspect_ratio(eye):
    # (|e1-e5|+|e2-e4|) / (2|e0-e3|)
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# 嘴长宽比例
def mouth_aspect_ratio(mouth):
    A = np.linalg.norm(mouth[1] - mouth[7])  # 61, 67
    B = np.linalg.norm(mouth[3] - mouth[5])  # 63, 65
    C = np.linalg.norm(mouth[0] - mouth[4])  # 60, 64
    mar = (A + B) / (2.0 * C)
    return mar


def detectByGUI(queue):

    def update_output(text):
        while not queue.empty():
            queue.get()
        queue.put(text)

    global blink_total
    global mouth_total
    global pic_total
    global blink_counter
    global mouth_status_open

    try:
        map_file_path = 'Face lib/map.txt'

        if not os.path.exists(map_file_path):
            os.makedirs('Face lib', exist_ok=True)
            with open(map_file_path, 'w') as f:
                json.dump({}, f)  # 写入一个空的字典

        with open(map_file_path, 'r') as f:
            name_folder_map = json.load(f)
        names = name_folder_map.keys()
        if (len(names) == 0):
            update_output("还没有注册，请先注册！")
            return False

        update_output("检测模块, 按住Q即可退出检测")
        video_capture = cv2.VideoCapture(0)

        pkl_file = open('Face lib/facedata.pkl', 'rb')
        all_known_face_encodings = pickle.load(pkl_file)
        pkl_file.close()

        names = list(name_folder_map.keys())

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        frame_count = 0

        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            if frame_count % 1 == 0:  # 每帧处理一次
                process_this_frame = True
            else:
                process_this_frame = False

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            name = 'Unknown'
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    min_dis = 10000.0  # 初始化为最大值
                    name = names[0]
                    # See if the face is a match for the known face(s)
                    name = "Unknown"
                    idx = -1
                    for i in range(len(all_known_face_encodings)):
                        face_dis = face_recognition.face_distance(
                            all_known_face_encodings[i], face_encoding)
                        if face_dis.shape[0] != 0:
                            face_mean = np.mean(face_dis)
                            if face_mean != 0 and face_mean < min_dis:
                                min_dis = face_mean
                                name = names[i]
                    if min_dis > 0.5:  # 阈值可调
                        name = "Unknown"
                    face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)

                font = cv2.FONT_HERSHEY_DUPLEX
                if name == "Unknown":
                    cv2.putText(frame, 'Unknown', (left + 6, bottom - 6),
                                font, 1.0, (255, 255, 255), 1)
                else:
                    cv2.putText(frame, 'User', (left + 6, bottom - 6),
                                font, 1.0, (255, 255, 255), 1)
                    face_names.append('User')
                    update_output(f"检测出来了，你是{name}，但是我不确定你是不是真人！")

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            rects = detector(gray, 0)

            if len(rects) == 1:

                shape = predictor(gray, rects[0])
                shape = face_utils.shape_to_np(shape)
                left_eye = shape[lStart:lEnd]
                right_eye = shape[rStart:rEnd]
                left_ear = eye_aspect_ratio(left_eye)   # 计算左眼对应特征点
                right_ear = eye_aspect_ratio(right_eye)  # 计算右眼对应特征点
                ear = (left_ear + right_ear) / 2.0

                inner_mouth = shape[mStart:mEnd]
                mar = mouth_aspect_ratio(inner_mouth)

                print(blink_counter)

                # EAR低于阈值，有可能发生眨眼，眨眼连续帧加一次
                # 低于说明眨眼了
                if ear < EAR_THRESH:
                    blink_counter += 1
                # 否则，说明睁眼了
                else:
                    # 如果在 EAR_CONSEC_FRAMES_MIN 和 EAR_CONSET_FRAMS_MAX 个帧之间发生了 一次 睁眼 和 眨眼
                    if EAR_CONSEC_FRAMES_MIN <= blink_counter <= EAR_CONSET_FRAMES_MAX:
                        # if EAR_CONSET_FRAMES_MAX <= blink_counter:
                        blink_total += 1

                    blink_counter = 0

                if mar > MAR_THRESH:
                    mouth_status_open = 1

                else:
                    if mouth_status_open:
                        mouth_total += 1
                    mouth_status_open = 0

            if blink_total >= 1 and name != "Unknown":
                blink_total = 0
                mouth_total = 0
                update_output(f"检测出来了，你是{name}，我确定你是真人！")
                return True

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Release handle to the webcam
                video_capture.release()
                cv2.destroyAllWindows()
                break

        if 'User' not in face_names:
            update_output("没检测出来，你不是用户!")
        else:
            update_output("检测出来了，但我不确定你是人还是照片！")

        return False

    finally:
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detect()
