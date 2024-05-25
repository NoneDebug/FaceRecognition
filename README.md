# FaceRecognition
It's a trying to implements a faceRecognition through PC and Raspberry Pi.

## v0
初始构建在PC端的人脸检测

## v1
修复了一些bug

# 目前目录组织结构

```
.
├── GUI.py          # GUI界面，其中的函数均是最新版本
├── TestMain.py     # 测试主程序文件，并其中的函数并不是最新版本
├── py2Exe.py       # 打包脚本文件，根据自己需求可以进行修改
└── utils/          # 工具文件夹
    ├── Interceptor.py   # 拦截器文件，一个简单的AOP编程(静态代理)
    ├── createPickle.py  # 创建 pickle 文件脚本，保存当前注册用户的预测向量用于检测。
    ├── delete.py        # 删除文件脚本，删除对应名字，并处理pickle文件
    ├── detect.py        # 检测文件脚本，检测当前摄像头下有没有人脸
    ├── preProcess.py    # 预处理文件脚本，对注册用户
    └── register.py      # 注册文件脚本，用以注册目录用户（调用preProcess函数以及createPickle函数）
```

# 此项目已闲置

- 因为，本来的目标识别系统是用来设计门禁和开锁系统的，但是由于硬件电机和现场布置存在诸多问题，故放弃。
- 本项目依然可以实现一个基本的人脸识别功能，包括用户可交互的GUI界面，并包括打包程序。
