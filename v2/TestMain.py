from utils.detect import *
from utils.register import *
from utils.delete import *
from utils.Interceptor import *

if __name__ == "__main__":

    strategies = {
        "注册": register_face,
        "删除姓名": delete,
        "检测": detect,
        "退出": exit
    }

    while True:
        option = input("请输入您的选择（注册/删除姓名/检测/退出）")
        strategy = strategies.get(option)
        if strategy:
            strategy()
        else:
            print("无效的选项。")
