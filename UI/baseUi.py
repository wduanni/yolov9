import sys
import cv2
import torch
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtCore import QTimer

from test_ui import Ui_MainWindow  # main_windows是刚才生成的ui对用的Python文件名
ROOT=r"C:\Users\WDN\Desktop\file\code\PY\yolov5\\"

def convert2QImage(img):
    height, width, channel = img.shape
    return QImage(img, width, height, width * channel, QImage.Format_RGB888)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # self.model = torch.hub.load("./", "custom", path=ROOT+"runs/train/exp6/weights/best.pt", source="local")
        self.model = torch.hub.load("./", "custom", path=r"C:\Users\WDN\Desktop\file\code\PY\github\yolov9\weights\best.pt", source="local")
        
        self.video = None
        self.timer = QTimer()
        self.timer.setInterval(1)
        self.bind_slots()  # 绑定槽函数

    def image_pred(self, file_path): # 图片检测
        # img = cv2.imread(file_path)
        results = self.model(file_path)
        # results = self.model(img)
        image = results.render()[0]
        return convert2QImage(image)

    def open_image(self): # 打开图片
        print("点击了检测图片按钮")
        self.timer.stop()  # 停止视频检测
        file_path = QFileDialog.getOpenFileName(self, dir=ROOT+"data/industry/val/images/train", filter="*.jpg;*.png;*.jpeg")
        if file_path[0]:
            file_path = file_path[0]
            qimage = self.image_pred(file_path)
            self.input.setPixmap(QPixmap(file_path))
            self.output.setPixmap(QPixmap.fromImage(qimage))

    # def video_pred(self):  # 视频检测
    #     ret, frame = self.video.read()
    #     if not ret:
    #         self.timer.stop()
    #     else:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         self.input.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
    #         results = self.model(frame)
    #         image = results.render()[0]
    #         self.output.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    def open_video(self):  # 打开视频
        print("点击了检测视频！")
        file_path = QFileDialog.getOpenFileName(self, dir="./data02", filter="*.mp4")
        if file_path[0]:
            file_path = file_path[0]
            self.video = cv2.VideoCapture(file_path)
            self.timer.start()

    def bind_slots(self):  # 绑定槽函数
        self.detect.clicked.connect(self.open_image)
        # self.det_video.clicked.connect(self.open_video)
        # self.timer.timeout.connect(self.video_pred)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

