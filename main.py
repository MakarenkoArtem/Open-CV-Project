from os import mkdir, listdir, remove
import sys
import time
import pip
import timeit
import json

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
try:
    from fuzzywuzzy import fuzz
except ModuleNotFoundError:
    print("ModuleNotFoundError: модуль fuzzywuzzy не найден.")
    pip.main(['install', 'fuzzywuzzy'])
    from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
            '    if time < 0:\n', '        time = 0\n', 'from time import sleep\n', 'while 1:\n',
            '    k = [True, True, True]\n', '    ret, frame = cap.read()\n', '    print(1, ret)\n',
            "    if cv2.waitKey(1) == ord('q') or not ret:\n", '        k[0] = False\n',
            '    else:\n', "        cv2.imshow('frame', frame)\n",
            "    cv2.setMouseCallback('frame', click)\n", '    ret, frame = blue.read()\n',
            '    print(2, ret)\n', "    if cv2.waitKey(1) == ord('q') or not ret:\n",
            '        k[1] = False\n', '    else:\n', "        cv2.imshow('blue', frame)\n",
            "    cv2.setMouseCallback('blue', click)\n", '    ret, frame = red.read()\n',
            '    print(3, ret)\n', "    if cv2.waitKey(1) == ord('q') or not ret:\n",
            '        k[2] = False\n', '    else:\n', "        cv2.imshow('red', frame)\n",
            "    cv2.setMouseCallback('frame', click)\n", '    if k == [False, False, False]:\n',
            '        break\n', '    sleep(time)\n',
            'cap.release()\n', 'red.release()\n', 'blue.release()\n', 'cv2.destroyAllWindows()\n']
    for i in text:
        file.write(i)
from Base import Ui_MainWindow
from Settings import Ui_Dialog
from base_date import *


class Settings(QWidget, Ui_Dialog):
    def __init__(self, number, color, colors):
        super().__init__()
        self.setupUi(self)
        try:
            self.cap = cv2.VideoCapture(number, cv2.CAP_DSHOW)
        except Warning:
            self.cap = cv2.VideoCapture(number)
        self.color = 'Red'
        if color == 'Blue':
            self.color = 'Blue'
        self.play = True
        self.setWindowTitle(color)
        self.pushButton_2.clicked.connect(self.ret)
        self.pushButton.clicked.connect(self.ret)
        self.s = [self.spinBox_3, self.spinBox_2, self.spinBox, self.spinBox_6, self.spinBox_5,
                  self.spinBox_4]
        self.z = [self.horizontalSlider_3, self.horizontalSlider_2, self.horizontalSlider,
                  self.horizontalSlider_6, self.horizontalSlider_5, self.horizontalSlider_4]
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
            # imgHLS = cv2.cvtColor(frame, self.color)
            print((self.z[0].value(), self.z[1].value(), self.z[2].value()),
                  (self.z[3].value(), self.z[4].value(), self.z[5].value()))
            mask = cv2.inRange(frame, (self.z[0].value(), self.z[1].value(), self.z[2].value()),
                               (self.z[3].value(), self.z[4].value(), self.z[5].value()))
            mask = cv2.bitwise_and(frame, frame, mask=mask)
            pic = cv2.resize(mask, (572, 312), interpolation=cv2.INTER_AREA)
            pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(pic.data, 572, 312, QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            self.label_7.setPixmap(QPixmap(convertToQtFormat))
            self.show()
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
        self.frame_video = cv2.VideoWriter(f'{dirs}/frame.avi', fourcc, 24.0, (640, 480))
        self.blue_video = cv2.VideoWriter(f'{dirs}/blue.avi', fourcc, 20.0, (64, 64))
        self.red_video = cv2.VideoWriter(f'{dirs}/red.avi', fourcc, 20.0, (64, 64))  # запись
        self.number = number
        self.pushButton_3.clicked.connect(self.release)
        self.pushButton.clicked.connect(self.settings)
        self.pushButton_2.clicked.connect(self.settings)
        base = Base_date("config/signs.sqlite3").select(['*'], "White_signs", 'and', [])
        self.WHITE_SIGNS = []
        for f in base:
            r = []
            for i in range(len(f)):
                k = []
                if i == 0:
                    k = f[i]
                elif i % 2 and f[i] != '':
                    k = [j.strip() == "True" for j in f[i].split(",")]
                elif f[i] != '':
                    k = [[int(m) for m in j.split(":")] for j in f[i].split(",")]
                r.append(k)
            self.WHITE_SIGNS.append(r)
        print(self.WHITE_SIGNS)
        base = Base_date("config/signs.sqlite3").select(['*'], "Red_signs", 'and', [])
        self.RED_SIGNS = []
        for f in base:
            r = []
            for i in range(len(f)):
                k = []
                if i == 0:
                    k = f[i]
                elif i % 2 and f[i] != '':
                    k = [j.strip() == "True" for j in f[i].split(",")]
                elif f[i] != '':
                    k = [[int(m) for m in j.split(":")] for j in f[i].split(",")]
                r.append(k)
            self.RED_SIGNS.append(r)
        print(self.RED_SIGNS)
        base = Base_date("config/signs.sqlite3").select(['*'], "Blue_signs", 'and', [])
        self.BLUE_SIGNS = []
        for f in base:
            r = []
            for i in range(len(f)):
                k = []
                if i == 0:
                    k = f[i]
                elif i % 2 and f[i] != '':
                    k = [j.strip() == "True" for j in f[i].split(",")]
                elif f[i] != '':
                    k = [[int(m) for m in j.split(":")] for j in f[i].split(",")]
                r.append(k)
            self.BLUE_SIGNS.append(r)
        print(self.BLUE_SIGNS)
        try:
            with open("config/base.json") as file:
                self.DATA = json.load(file)
                self.red, self.blue = self.DATA['red']['range'], self.DATA['blue']['range']
        except FileNotFoundError:
            print("Нет json файла")
            self.release()
        self.play = True

    def settings(self):
        self.cap.release()
        c, cl = 'Red', self.red
        if self.sender() == self.pushButton_2:
            c, cl = 'Blue', self.blue
        f = Settings(self.number, color=c, colors=cl)  # .exec_()
        if self.sender() == self.pushButton_2 and f.output is not None:
            self.blue = f.output
            self.DATA['blue']['range'] = self.blue
        elif f.output is not None:
            self.red = f.output
            self.DATA['red']['range'] = self.red
        try:
            self.cap = cv2.VideoCapture(self.number, cv2.CAP_DSHOW)
        except Warning:
            self.cap = cv2.VideoCapture(self.number)

    def release(self):
        self.frame_video.release()
        self.blue_video.release()
        self.red_video.release()
        if self.play:
            print("Надеюсь мы не разбились, жду встречи ;)")
        self.play = False
        self.cap.release()
        cv2.destroyAllWindows()
        try:
            remove("bw.png")
        except FileNotFoundError:
            pass
        try:
            with open("config/base.json", 'w') as file:
                json.dump(self.DATA, file)
        except FileNotFoundError:
            pass
        finally:
            self.close()

    def sign(self, occasion=2147483647, delay=0.09):
        if occasion < 0:
            occasion = 2147483647

        def insert(pic, widget):  # вывод картинки на label
            pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
            pic = cv2.resize(pic, (
                widget.size().width(),
                widget.size().height()))  # размер картинки должен быть кратным 4
            convertToQtFormat = QImage(pic.data, pic.shape[1], pic.shape[0], QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            widget.setPixmap(QPixmap(convertToQtFormat))

        def color(frame, draw_frame, asd="white"):
            c = self.DATA[asd]['range']
            if asd == "red":
                color = (0, 0, 255)
                list_points = self.RED_SIGNS
            elif asd == "blue":
                color = (255, 0, 0)
                list_points = self.BLUE_SIGNS
            else:
                color = (255, 0, 150)
                list_points = self.WHITE_SIGNS
            points = self.DATA[asd]['points']
            pic = cv2.blur(frame, (4, 4))
            pic = cv2.GaussianBlur(pic, (3, 3), 0)
            pic = cv2.erode(pic, (5, 5), iterations=3)
            pic = cv2.dilate(pic, (4, 4), iterations=2)
            pic = cv2.inRange(pic, (c[0], c[1], c[2]), (c[3], c[4], c[5]))
            contours = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = contours[0]  # or [1] в линуксе на ноуте не знаю почему
            frame_n = frame[0:64, 0:64]
            k = pic[0:64, 0:64]
            if contours:
                contours = sorted(contours, key=cv2.contourArea, reverse=True)
                x, y, w, h = cv2.boundingRect(contours[0])
                if (w > 60 or h > 60) and h * w >= 3800:
                    k = pic[y:y + h, x:x + w]
                    k = cv2.resize(k, (64, 64))
                    frame_n = frame[y:y + h, x:x + w]
                    frame_n = cv2.resize(frame_n, (64, 64))
                    # cv2.drawContours(draw_frame, contours[0], -1, color, 0) # контуры
                    cv2.rectangle(draw_frame, (x, y), (x + w, y + h), color, 2)
            contour = k.copy()
            cv2.imwrite('bw.png', k)
            k = cv2.imread('bw.png')
            point = []
            for x, y in points:
                c = color
                point.append(contour[y][x].all())
                if contour[y][x].all():
                    c = (0, 255, 0)
                cv2.circle(k, (x, y), 3, c, -1)
            list_points = [i for i in list_points if
                           fuzz.ratio(i[1], point) >= 85]  # нечёткое сравнение контуров знаков
            if asd == "white":
                print(list_points)
            z = []
            for sign in list_points:
                num = []
                for i in range(2, (2 + len(sign[2:])) // 2):
                    print(i)
                    num.append(fuzz.ratio([contour[y][x] for x, y in sign[i* 2]], sign[i*2 + 1]))
                z.append([sum(num) / len(num), sign[0]])
            z.sort()
            if asd == "white":
                print(z)
            if len(z) and (z[0][0] > 70 or (asd == "white" and z[0][0] > 60)):
                cv2.putText(draw_frame, z[0][1].replace("_", " ").capitalize(), (30, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                insert(frame_n, self.label_5)
                self.label_6.setText(z[0][1].replace("_", " ").capitalize())
            return k, frame, pic

        for _ in range(occasion):
            start = time.time()
            if not self.play:
                break
            ret, self.frame = self.cap.read()
            if not ret:
                self.frame = cv2.imread('config/Colors.jpg')
            # try:
            if 1:
                frame = self.frame.copy()
                blue, contours, blue_pic = color(self.frame, frame, 'blue')
                # contours = blue#cv2.bitwise_and(self.frame, self.frame, mask=blue)
                insert(blue, self.label_4)
                self.blue_video.write(blue)
                red, contours, red_pic = color(self.frame, frame, 'red')
                # contours = blue#contours = cv2.bitwise_and(self.frame, self.frame, mask=blredue)
                insert(red, self.label_2)
                white, contours, white_pic = color(self.frame, frame, 'white')
                insert(white, self.label_7)
                self.red_video.write(red)
                pic = blue_pic + red_pic + white_pic
                pic = cv2.bitwise_and(self.frame, self.frame, mask=pic)
                insert(pic, self.label_3)
                insert(frame, self.label)
                self.frame_video.write(frame)
                self.show()
            # except Exception as e:
            #    print(e.__class__.__name__)
            # imshow("Frame", self.frame)
            if cv2.waitKey(1) == ord("q"):
                pass
            t = delay - time.time() + start
            if t > 0:
                time.sleep(t)
        self.func = None


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


"""self.output - переменная во всех класса для передачи информации после завершения работы класса"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    f = Vision(0)
    f.sign(1000)
    f.release()
    sys.exit(app.exec())
