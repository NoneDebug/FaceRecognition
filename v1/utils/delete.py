from utils.Interceptor import get_name
import os
import json
import shutil
from utils.createPickle import *


def delete():
    name = get_name()

    if os.path.exists('Face lib/map.txt') and os.path.getsize('Face lib/map.txt') > 0:
        with open('Face lib/map.txt', 'r') as f:
            name_folder_map = json.load(f)

            if name in name_folder_map:

                deleted_folder_number = name_folder_map[name]

                del name_folder_map[name]
                shutil.rmtree(f'Face lib/{deleted_folder_number}')

                for key in list(name_folder_map.keys()):
                    if name_folder_map[key] > deleted_folder_number:
                        os.rename(
                            f'Face lib/{name_folder_map[key]}', f'Face lib/{name_folder_map[key] - 1}')
                    # 更新字典
                        name_folder_map[key] -= 1

                with open('Face lib/map.txt', 'w') as f:
                    json.dump(name_folder_map, f)
                print('名字已删除！')
                createPickleForAll()
                return
            else:
                print("名字不存在！")
                return
    else:
        print("文件不存在或者文件为空！")
        return


def deleteFaceByGUI(queue, name):

    def update_output(text):
        while not queue.empty():
            queue.get()
        queue.put(text)

    if os.path.exists('Face lib/map.txt') and os.path.getsize('Face lib/map.txt') > 0:
        with open('Face lib/map.txt', 'r') as f:
            name_folder_map = json.load(f)

            if name in name_folder_map:
                # TODO: 处理逻辑
                deleted_folder_number = name_folder_map[name]

                del name_folder_map[name]
                shutil.rmtree(f'Face lib/{deleted_folder_number}')

                for key in list(name_folder_map.keys()):
                    if name_folder_map[key] > deleted_folder_number:
                        os.rename(
                            f'Face lib/{name_folder_map[key]}', f'Face lib/{name_folder_map[key] - 1}')
                    # 更新字典
                        name_folder_map[key] -= 1

                with open('Face lib/map.txt', 'w') as f:
                    json.dump(name_folder_map, f)

                update_output('请等候，不要操作！')
                createPickleForAll()
                update_output('名字已删除！')
                return
            else:
                update_output("名字不存在！")
                return
    else:
        update_output("文件不存在或者文件为空！")
        return


if __name__ == "__main__":
    delete()
