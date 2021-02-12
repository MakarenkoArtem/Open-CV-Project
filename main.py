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
    import cv2
except ModuleNotFoundError:
    print("ModuleNotFoundError: модуль opencv-python не найден.")
    pip.main(['install', 'opencv-python'])
    import cv2
"""------------------------------------------------------------------------------------------"""

dirs = [int(i.split()[-1]) for i in listdir() if i.split()[0] == 'Way']
dirs.sort()
if not len(dirs):
    mkdir("Way 1")
    dirs = 'Way 1'
else:
    mkdir(f"Way {dirs[-1] + 1}")
    dirs = f"Way {dirs[-1] + 1}"
# with open(f'Way 26/read_video_file.py', "r") as file:
#    print(file.readlines())
with open(f'{dirs}/read_video_file.py', "w") as file:
    text = ['import cv2\n', '\n', "cap = cv2.VideoCapture('frame.avi')\n",
            "blue = cv2.VideoCapture('blue.avi')\n", "red = cv2.VideoCapture('red.avi')\n",
            'time = 0.2\n', 'def click(event, x, y, flags, param):\n', '    global time\n',
            '    if event == cv2.EVENT_MOUSEWHEEL:\n', '        if flags > 0:\n',
            '            time += 0.05\n', '        elif flags < 0:\n', '            time -= 0.05\n',
            '    if time <= 0:\n', '        time = 0.01\n', 'from time import sleep\n', 'while 1:\n',
            '    k = [True, True, True]\n', '    ret, frame = cap.read()\n', '    print(1, ret)\n',
            "    if cv2.waitKey(1) == ord('q') or not ret:\n", '        k[0] = False\n',
            '    else:\n', "        cv2.imshow('frame', frame)\n", '    ret, frame = blue.read()\n',
            '    print(2, ret)\n', "    if cv2.waitKey(1) == ord('q') or not ret:\n",
            '        k[1] = False\n', '    else:\n', "        cv2.imshow('blue', frame)\n",
            "    cv2.setMouseCallback('blue', click)\n", '    ret, frame = red.read()\n',
            '    print(3, ret)\n', "    if cv2.waitKey(1) == ord('q') or not ret:\n",
            '        k[2] = False\n', '    else:\n', "        cv2.imshow('red', frame)\n",
            '    if k == [False, False, False]:\n', '        break\n', '    sleep(time)\n',
            'cap.release()\n', 'red.release()\n', 'blue.release()\n', 'cv2.destroyAllWindows()\n']
    for i in text:
        file.write(i)
from Base import Ui_MainWindow
from Settings import Ui_Dialog


class Settings(QWidget, Ui_Dialog):
    def __init__(self, number, color, colors):
        super().__init__()
        self.setupUi(self)
        try:
            self.cap = cv2.VideoCapture(number, cv2.CAP_DSHOW)
        except Warning:
            self.cap = cv2.VideoCapture(number)
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
                frame = cv2.imread('config/Colors.jpg')
            imgHLS = cv2.cvtColor(frame, self.color)
            print((self.z[0].value(), self.z[1].value(), self.z[2].value()),
                  (self.z[3].value(), self.z[4].value(), self.z[5].value()))
            mask = cv2.inRange(imgHLS, (self.z[0].value(), self.z[1].value(), self.z[2].value()),
                               (self.z[3].value(), self.z[4].value(), self.z[5].value()))
            mask = cv2.bitwise_and(frame, frame, mask=mask)
            pic = cv2.resize(mask, (632, 312), interpolation=cv2.INTER_AREA)
            pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(pic.data, 632, 312, QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            self.label_7.setPixmap(QPixmap(convertToQtFormat))
            self.show()
            # self.out.write(frame)
            if cv2.waitKey(1) == ord("q"):
                pass
            # sleep(0)


class Vision(QWidget, Ui_MainWindow):
    def __init__(self, number):
        super().__init__()
        self.setupUi(self)
        try:
            self.cap = cv2.VideoCapture(number, cv2.CAP_DSHOW)
        except Warning:
            self.cap = cv2.VideoCapture(number)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(f'{dirs}/frame.avi', fourcc, 24.0, (640, 480))
        self.blue_f = cv2.VideoWriter(f'{dirs}/blue.avi', fourcc, 20.0, (64, 64))
        self.red_f = cv2.VideoWriter(f'{dirs}/red.avi', fourcc, 20.0, (64, 64))  # запись
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
            self.cap = cv2.VideoCapture(self.number, cv2.CAP_DSHOW)
        except Warning:
            self.cap = cv2.VideoCapture(self.number)

    def release(self):
        self.out.release()
        self.blue_f.release()
        self.red_f.release()
        if self.play or 1:
            self.play = False
            self.cap.release()
            print("Надеюсь мы не разбились, жду встречи ;)")
            cv2.destroyAllWindows()
            self.close()

    def sign(self, occasion=1, time=0.3):
        def color(frame, asd):
            c = self.blue
            color = (0, 0, 255)
            if asd == "red":
                color = (255, 0, 0)
                c = self.red
            pic = cv2.blur(frame, (4, 4))
            pic = cv2.GaussianBlur(pic, (3, 3), 0)
            pic = cv2.erode(pic, (5, 5), iterations=3)
            pic = cv2.dilate(pic, (4, 4), iterations=2)
            pic = cv2.inRange(pic, (c[0], c[1], c[2]), (c[3], c[4], c[5]))
            contours = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = contours[0]  # or [1] в линуксе на ноуте не знаю почему
            contour = self.frame[0:64, 0:64]
            return pic, contour

        for _ in range(occasion):
            def insert(pic, widget):
                pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(pic.data, pic.shape[1], pic.shape[0],
                                           QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                widget.setPixmap(QPixmap(convertToQtFormat))

            if not self.play:
                break
            ret, self.frame = self.cap.read()
            print(ret, self.frame.shape)
            if not ret:
                self.frame = cv2.imread('Colors.jpg')
            # try:
            if 1:
                self.out.write(self.frame)
                self.frame = cv2.resize(self.frame, (352, 300))
                insert(self.frame, self.label)
                blue, contours = color(self.frame, 'blue')
                insert(contours, self.label_2)
                self.blue_f.write(contours)
                red, contours = color(self.frame, 'red')
                insert(contours, self.label_4)
                self.red_f.write(contours)
                pic = blue + red
                pic = cv2.bitwise_and(self.frame, self.frame, mask=pic)
                insert(pic, self.label_3)
                self.show()
            # except Exception as e:
            #    print(e.__class__.__name__)
            # imshow("Frame", self.frame)
            if cv2.waitKey(1) == ord("q"):
                pass
            sleep(time)
        self.func = None
        self.i = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Vision(0)
    f.show()
    f.sign(1000)
    f.release()
    sys.exit(app.exec())
