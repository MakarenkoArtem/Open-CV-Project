from os import mkdir, listdir
from time import sleep
import pip

if int(pip.__version__.split(".")[0]) < 20:
    pip.main(['install', 'pip', '--upgrade', '--force-reinstall'])
"""------------------------------------------------------------------------------------------"""
try:
    from PyQt5 import *
except ModuleNotFoundError:
    import pip

    pip.main(['install', 'PyQT5'])
    from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
"""------------------------------------------------------------------------------------------"""
try:
    from cv2 import *
except ModuleNotFoundError:
    print("ModuleNotFoundError: модуль opencv-python не найден.")
    import pip

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
            "blue = cv2.VideoCapture('output.avi')\n", "#red = cv2.VideoCapture('red.avi')\n",
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
            convertToQtFormat = QtGui.QImage(pic.data, 632, 312, QtGui.QImage.Format_RGB888)
            convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
            self.label_7.setPixmap(QPixmap(convertToQtFormat))
            self.show()
            # self.out.write(frame)
            if waitKey(1) == ord("q"):
                pass
            # sleep(0)
        destroyAllWindows()