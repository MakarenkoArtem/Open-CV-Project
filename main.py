from os import mkdir, listdir
import sys
from time import sleep
import pip

if int(pip.__version__.split(".")[0]) < 21:
    pip.main(['install', 'pip', '--upgrade', '--force-reinstall'])
"""------------------------------------------------------------------------------------------"""
import site
import shutil


def check():
    if "platforms" not in listdir(site.getsitepackages()[0]):
        shutil.move("\\".join([site.getsitepackages()[1], 'PyQt5', "Qt", 'plugins', 'platforms']),
                    site.getsitepackages()[0])


check()

try:
    from PyQt5 import *
except ModuleNotFoundError:
    pip.main(['install', 'PyQT5'])
    check()
    from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

"""------------------------------------------------------------------------------------------"""
try:
    from cv2 import *
except ModuleNotFoundError:
    print("ModuleNotFoundError: модуль opencv-python не найден.")
    pip.main(['install', 'opencv-python'])
    from cv2 import *
"""------------------------------------------------------------------------------------------"""

dirs = [int(i.split()[-1]) for i in listdir() if i.split()[0] == 'Way']
dirs.sort()
if not len(dirs):
    mkdir("Way 1")
    dirs = 'Way 1'
else:
    mkdir(f"Way {dirs[-1] + 1}")
    dirs = f"Way {dirs[-1] + 1}"
with open(f'{dirs}/read_video_file.py', "w") as file:
    text = ['import cv2\n', '\n', "#cap = cv2.VideoCapture('frame.mp4')\n",
            "blue = cv2.VideoCapture('frame.avi')\n", "#red = cv2.VideoCapture('red.avi')\n",
            'from time import sleep\n', 'while 1:\n', '    #ret, frame = cap.read()\n',
            '    #print(ret)\n', '    ret, frame = blue.read()\n',
            "    if cv2.waitKey(1) == ord('q') or not ret:\n", '        break\n',
            "    cv2.imshow('blue', frame)\n", "    #cv2.imshow('frame', frame)\n",
            '    #ret, frame = red.read()\n', "    #cv2.imshow('red', frame)\n", '    sleep(0.02)\n',
            '#cap.release()\n', '#red.release()\n', 'blue.release()\n', 'cv2.destroyAllWindows()\n']
    for i in text:
        file.write(i)
from Base import Ui_MainWindow
from Settings import Ui_Dialog


class Settings(QWidget, Ui_Dialog):
    def __init__(self, number, color, colors):
        super().__init__()
        self.setupUi(self)
        try:
            self.cap = VideoCapture(number, CAP_DSHOW)
        except Warning:
            self.cap = VideoCapture(number)
        self.color = 38
        if color == 'Blue':
            self.color = 51
        self.play = True
        self.setWindowTitle(color)
        self.pushButton_2.clicked.connect(self.ret)
        self.pushButton.clicked.connect(self.ret)
        self.s = [self.spinBox, self.spinBox_2, self.spinBox_3, self.spinBox_4, self.spinBox_5,
                  self.spinBox_6]
        self.z = [self.horizontalSlider, self.horizontalSlider_2, self.horizontalSlider_3,
                  self.horizontalSlider_4, self.horizontalSlider_5, self.horizontalSlider_6]
        for i in range(6):
            self.z[i].setValue(colors[i])
            self.z[i].valueChanged.connect(self.valuechange)
            self.s[i].setValue(colors[i])
            self.s[i].valueChanged.connect(self.valuechangespin)
        self.run()

    def valuechangespin(self):
        self.z[self.s.index(self.sender())].setValue(self.sender().value())

    def valuechange(self):
        self.s[self.z.index(self.sender())].setValue(self.sender().value())

    def ret(self):
        self.play = False
        self.cap.release()
        self.output = [i.value() for i in self.z]
        if self.sender() == self.pushButton_2:
            self.output = None
        self.close()

    def run(self):
        while self.play:
            ret, frame = self.cap.read()
            if not ret:
                frame = imread('config/Colors.jpg')
            imgHLS = cvtColor(frame, self.color)
            print((self.z[0].value(), self.z[1].value(), self.z[2].value()),
                  (self.z[3].value(), self.z[4].value(), self.z[5].value()))
            mask = inRange(imgHLS, (self.z[0].value(), self.z[1].value(), self.z[2].value()),
                           (self.z[3].value(), self.z[4].value(), self.z[5].value()))
            mask = bitwise_and(frame, frame, mask=mask)
            pic = resize(mask, (632, 312), interpolation=INTER_AREA)
            pic = cvtColor(pic, COLOR_BGR2RGB)
            convertToQtFormat = QImage(pic.data, 632, 312, QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            self.label_7.setPixmap(QPixmap(convertToQtFormat))
            self.show()
            # self.out.write(frame)
            if waitKey(1) == ord("q"):
                pass
            # sleep(0)
        destroyAllWindows()


class Vision(QWidget, Ui_MainWindow):
    def __init__(self, number):
        super().__init__()
        self.setupUi(self)
        try:
            self.cap = VideoCapture(number, CAP_DSHOW)
        except Warning:
            self.cap = VideoCapture(number)
        fourcc = VideoWriter_fourcc(*"XVID")
        self.out = VideoWriter(f'{dirs}/frame.avi', fourcc, 20.0, (640, 480))
        '''self.blue = VideoWriter(f'{di}/blue.avi', fourcc, 20.0, (64, 64))
        self.red = VideoWriter(f'{di}/red.avi', fourcc, 20.0, (64, 64))'''  # запись
        self.number = number
        self.pushButton_3.clicked.connect(self.release)
        self.pushButton.clicked.connect(self.settings)
        self.pushButton_2.clicked.connect(self.settings)
        self.i = 0
        self.red, self.blue = [50, 15, 10, 130, 70, 70], [0, 10, 175, 20, 140, 255]
        self.func = None
        self.play = True

    def settings(self):
        self.cap.release()
        c, cl = 'Red', self.red
        if self.sender() == self.pushButton_2:
            c, cl = 'Blue', self.blue
        f = Settings(self.number, c, cl)  # .exec_()
        if self.sender() == self.pushButton_2 and f.output is not None:
            self.blue = f.output
        elif f.output is not None:
            self.red = f.output
        try:
            self.cap = VideoCapture(self.number, CAP_DSHOW)
        except Warning:
            self.cap = VideoCapture(self.number)

    def release(self):
        self.out.release()
        # self.blue.release()
        # self.red.release()
        if self.play or 1:
            self.play = False
            self.cap.release()
            print("Надеюсь мы не разбились, жду встречи ;)")
            destroyAllWindows()
            self.close()

    def sign(self, occasion=1, time=0.3):
        def color(frame, asd):
            c = self.blue
            color = (0, 0, 255)
            if asd == "red":
                color = (255, 0, 0)
                c = self.red
            pic = blur(frame, (4, 4))
            pic = GaussianBlur(pic, (3, 3), 0)
            pic = erode(pic, (5, 5), iterations=3)
            pic = dilate(pic, (4, 4), iterations=2)
            pic = inRange(pic, (c[0], c[1], c[2]), (c[3], c[4], c[5]))
            contours = findContours(pic, RETR_TREE, CHAIN_APPROX_NONE)
            contours = contours[0]  # or [1] в линуксе на ноуте не знаю почему
            contour = self.frame[0:64, 0:64]
            return pic, contour

        for _ in range(occasion):
            def insert(pic, widget):
                pic = cvtColor(pic, COLOR_BGR2RGB)
                convertToQtFormat = QImage(pic.data, pic.shape[1], pic.shape[0],
                                                 QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                widget.setPixmap(QPixmap(convertToQtFormat))
            if not self.play:
                break
            ret, self.frame = self.cap.read()
            print(ret, self.frame.shape)
            if not ret:
                self.frame = imread('Colors.jpg')
            try:
                self.out.write(self.frame)
                self.frame = resize(self.frame, (352, 300))
                insert(self.frame, self.label)
                blue, contours = color(self.frame, 'blue')
                insert(contours, self.label_2)
                red, contours = color(self.frame, 'red')
                insert(contours, self.label_4)
                pic = blue + red
                pic = bitwise_and(self.frame, self.frame, mask=pic)
                insert(pic, self.label_3)
                self.show()
            except Exception as e:
                print(e.__class__.__name__)
            # imshow("Frame", self.frame)
            if waitKey(1) == ord("q"):
                pass
            sleep(time)
        destroyAllWindows()
        self.func = None
        self.i = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Vision(0)
    print(1)
    f.show()
    f.sign(1000)
    #f.release()
    sys.exit(app.exec())
