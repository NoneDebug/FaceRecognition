import os
import shutil
import subprocess
import json
# 全局变量，用于存储要打包的脚本名称
script_name = "GUI.py"


def copy_folders(source_dir, target_dir):
    # 要复制的文件夹列表
    folders_to_copy = ["face_recognition_models"]

    # 创建目标文件夹
    script_name_without_extension = os.path.splitext(script_name)[0]
    target_path = os.path.join(target_dir, script_name_without_extension)
    os.makedirs(target_path, exist_ok=True)

    # 复制文件夹
    for folder in folders_to_copy:
        source_path = os.path.join(source_dir, folder)
        if os.path.exists(source_path):
            shutil.copytree(source_path, os.path.join(target_path, folder))
            print(f"Copied folder '{folder}' to '{target_path}'")
        else:
            print(f"Folder '{folder}' does not exist in '{source_dir}'")
    # 在 target_dir 中创建 Face lib 文件夹并写入 map.txt 文件
    face_lib_path = os.path.join(target_path, "Face lib")
    os.makedirs(face_lib_path, exist_ok=True)
    with open(os.path.join(face_lib_path, "map.txt"), "w") as map_file:
        empty_json = json.dumps({})
        map_file.write(empty_json)
        print(f"Created 'map.txt' in 'Face lib' folder at '{target_path}'")


def copy_project(source_dir, project_dir, version):

    target_dir = os.path.join(
        project_dir, f"Face_Recognition_v{version}"
    )

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        print(f"Removed existing directory '{target_dir}'")

    # 创建目标文件夹路径
    target_path = os.path.join(
        project_dir, f"Face_Recognition_v{version}", "project")

    os.makedirs(target_path, exist_ok=True)

    # 复制 dist/GUI 文件夹内容到目标路径
    dist_gui_path = os.path.join(source_dir, "dist", "GUI")
    if os.path.exists(dist_gui_path):
        shutil.copytree(dist_gui_path, os.path.join(target_path, "GUI"))
        print(f"Copied contents of 'dist/GUI' to '{target_path}'")

    # 复制 README.md 到上一级目录的指定位置
    readme_src_path = os.path.join(source_dir, "README.md")

    if os.path.exists(readme_src_path):
        readme_dst_path = os.path.join(
            project_dir, f"Face_Recognition_v{version}", "README.md")
        shutil.copy(readme_src_path, readme_dst_path)
        print(f"Copied 'README.md' to '{project_dir}'")
    else:
        print("README.md not found in source directory")


def extract_gui_files(project_dir, project_name, del_folder):
    project_project_dir = os.path.join(project_dir, project_name)
    gui_dir = os.path.join(project_project_dir, del_folder)

    # 检查 project 文件夹是否存在
    if os.path.exists(project_project_dir) and os.path.isdir(project_project_dir):
        # 检查 GUI 文件夹是否存在
        if os.path.exists(gui_dir) and os.path.isdir(gui_dir):
            project_dir_contents = os.listdir(gui_dir)

            # 移动 GUI 文件夹中的内容到 project 文件夹中
            for item in project_dir_contents:
                item_path = os.path.join(gui_dir, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, project_project_dir)
                elif os.path.isdir(item_path):
                    # 如果是文件夹，将文件夹中的内容移动到 project 文件夹中
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            shutil.move(os.path.join(root, file),
                                        project_project_dir)
                    # 删除空的 GUI 文件夹
                    shutil.rmtree(item_path)
            print("GUI folder contents extracted and folder removed successfully.")
        else:
            print("GUI folder not found.")
    else:
        print("Project folder not found.")


def main(script_name):
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 执行 PyInstaller 打包命令
    process = subprocess.Popen(
        ["pyinstaller", script_name, "-w", "-i", "pic.ico"], stdin=subprocess.PIPE)

    # 输入 'Y' 确认覆盖
    process.communicate(b"Y\n")

    # 复制指定文件夹到最终打包好的文件夹中
    copy_folders(current_dir, os.path.join(current_dir, "dist"))

    # 指定目标路径，版本号
    project_dir = os.path.abspath(os.path.join(
        current_dir, "..", "Face_Recognition_project"))
    version = "1.0"  # 这里替换为你想要的版本号

    # 将打包好的内容复制到项目目录中
    copy_project(current_dir, project_dir, version)

    deal_dir = os.path.abspath(os.path.join(
        current_dir, "..", "Face_Recognition_project", f"Face_Recognition_v{version}"))

    # extract_gui_files(deal_dir, "project", os.path.splitext(script_name)[0])


if __name__ == "__main__":
    main(script_name)
    print("Done!")
