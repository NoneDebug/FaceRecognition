from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QInputDialog
from PyQt5.QtCore import pyqtSignal, QThread
from utils.detect import *
from utils.register import *
from utils.delete import *
from utils.Interceptor import *
import sys
import multiprocessing
from multiprocessing import Queue


def worker_func(func, main_window, need, name=None):

    if need:
        func(main_window, name)
    else:
        func(main_window)


class Worker(QThread):
    text_update_signal = pyqtSignal(str)

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            if not self.queue.empty():
                text = self.queue.get()
                self.text_update_signal.emit(text)


class MainWindow(QWidget):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.output_queue = Queue()
        self.worker = Worker(self.output_queue)
        self.worker.text_update_signal.connect(self.updateText)
        self.worker.start()

    def initUI(self):
        self.setWindowTitle('人脸识别')

        vbox = QVBoxLayout()

        self.output_text = QTextEdit(self)
        vbox.addWidget(self.output_text)

        btn_register = QPushButton('注册', self)
        btn_register.clicked.connect(
            lambda: self.execute_strategy(registerFaceByGUI, True))
        vbox.addWidget(btn_register)

        btn_delete = QPushButton('删除姓名', self)
        btn_delete.clicked.connect(
            lambda: self.execute_strategy(deleteFaceByGUI, True))
        vbox.addWidget(btn_delete)

        btn_detect = QPushButton('检测', self)
        btn_detect.clicked.connect(
            lambda: self.execute_strategy(detectByGUI, False))
        vbox.addWidget(btn_detect)

        btn_exit = QPushButton('退出', self)
        btn_exit.clicked.connect(self.close)
        vbox.addWidget(btn_exit)

        self.setLayout(vbox)
        self.update_output_signal.connect(self.updateText)

    def updateText(self, text):
        self.output_text.setText(text)

    def execute_strategy(self, strategy, need):

        cv2.destroyAllWindows()

        if need:
            name, ok = QInputDialog.getText(self, '输入姓名', '请输入你的姓名:')
            if name == '':
                return
            elif ok:
                process = multiprocessing.Process(
                    target=strategy, args=(self.output_queue, name))
                process.start()

        else:
            process = multiprocessing.Process(
                target=strategy, args=(self.output_queue,))
            process.start()


if __name__ == "__main__":

    multiprocessing.set_start_method('spawn')
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
