from os import mkdir, listdir
import sys
from time import sleep
import pip

if int(pip.__version__.split(".")[0]) < 21:
    pip.main(['install', 'pip', '--upgrade', '--force-reinstall'])
"""------------------------------------------------------------------------------------------"""
try:
    from PyQt5 import *
except ModuleNotFoundError:
    pip.main(['install', 'PyQT5'])
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


class Vision(QWidget, Ui_MainWindow):
    def __init__(self, number):
        super().__init__()
        self.setupUi(self)
        try:
            self.cap = cv2.VideoCapture(number, cv2.CAP_DSHOW)
        except Warning:
            self.cap = VideoCapture(number)
        fourcc = VideoWriter_fourcc(*'XVID')
        '''self.out = VideoWriter(f'{di}/frame.mp4', fourcc, 20.0, (640, 480))
        self.blue = VideoWriter(f'{di}/blue.avi', fourcc, 20.0, (64, 64))
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
        # self.out.release()
        # self.blue.release()
        # self.red.release()
        if self.play:
            self.play = False
            self.close()
            self.cap.release()
            print("Надеюсь мы не разбились, жду встречи ;)")
            self.close()

    def sign(self, occasion=1, time=0):
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
            '''if contours:
                contours = sorted(contours, key=contourArea, reverse=True)
                #drawContours(frame, contours[0], -1, (0, 255, 0), 3)
                x, y, w, h = boundingRect(contours[0])
                rectangle(frame, (x, y), (x + w, y + h), color, 1)
                contours = pic[y:y + h, x:x + w]
                contour = (contours, (64, 64))'''
            return pic, contour

        '''
            r = ["minb", "ming", "minr", "maxb", "maxg", "maxr"]

            def nothing(x):
                pass

            f = asd + f"result"
            namedWindow(f)
            for i in range(6):
                createTrackbar(r[i], f, c[i], 255, nothing)
            self.frame = imread('Colors.jpg')
            while True:
                # ret, self.frame = self.cap.read()
                hsv = cvtColor(self.frame, COLOR_BGR2HSV)
                hsv = blur(hsv, (5, 5))
                c = []
                for i in range(6):
                    c.append(getTrackbarPos(r[i], f))
                mask = inRange(self.frame, (c[0], c[1], c[2]), (c[3], c[4], c[5]))
                maskEr = erode(mask, (3, 3), iterations=2)
                maskDi = dilate(maskEr, (3, 3), iterations=2)
                imshow("Dilate", maskDi)
                result = bitwise_and(self.frame, self.frame, mask=mask)
                imshow(f, result)
                if waitKey(1) == ord("q"):
                    break
            destroyAllWindows()
            return [minb, ming, minr, maxb, maxg, maxr]

        inp = input(
            "Если вы хотите сами написать границы, то напишите 'w', если вы хотите готовые границы, то напишите 'r', если хотите подобрать границы, то напишите любую другую букву или не пишите ничего, ввод: ")
        if inp == "w":
            r = list(int(i) for i in input("Red: ").split(", "))
            b = list(int(i) for i in input("Blue: ").split(", "))
        elif inp == "r":
            r = [0, 10, 175, 20, 140, 255]
            b = [200, 10, 10, 255, 200, 110]
        else:
            r = color("red_")
            b = color("blue_")
        rn = [(2, 32), (62, 32), (32, 62), (32, 2), (6, 60), (60, 60), (19, 20),
              (44, 44), (19, 44), (44, 19), (20, 31), (44, 33)]
        no_entry = [True, True, True, True, False, False, True, True, True, True, True,
                    True]
        stop_is_prohibited = [True, True, True, True, False, False, True, True, True,
                              True, False, False]
        no_parking = [True, True, True, True, False, False, True, True, False, False,
                      False, False]
        speed = [True, True, True, True, False, False, False, False, False, False,
                 False, False]
        bn = [(3, 3), (3, 60), (60, 3), (60, 60), (28, 3), (38, 3), (31, 25), (42, 13), (22, 13)]
        pedestrian_crossing = [True, True, True, True, True, True, False, True, True]
        park = [True, True, True, True, True, True, True, False, False]
        m = ''
        ma = '''
        # self.func = self.sign
        for i in range(occasion):
            print(self.play)
            if not self.play:
                break
            '''if not ret:
                continue
            print(i)

            def e(ca):
                colo = (0, 0, 255)
                c = r
                rnt = rn
                if ca == "Blue":
                    c = b
                    rnt = bn
                    colo = (255, 0, 0)
                # imshow(ca, ra)
                contours = findContours(ra, RETR_TREE, CHAIN_APPROX_NONE)
                contours = contours[0]  # or [1] в линуксе на ноуте не знаю почему
                pic = self.frame[0:64, 0:64]
                pic = inRange(pic, (0, 0, 0), (100, 100, 100))
                if contours:
                    contours = sorted(contours, key=contourArea, reverse=True)
                    drawContours(self.frame, contours[0], -1, (0, 255, 0), 3)
                    x, y, w, h = boundingRect(contours[0])
                    rectangle(self.frame, (x, y), (x + w, y + h), colo, 2)
                    pic = ra[y:y + h, x:x + w]
                    pic = resize(pic, (64, 64))
                imwrite('bw.png', pic)
                rt = imread('bw.png')
                rq = []
                for x, y in rnt:
                    if pic[y][x]:  # pic
                        circle(rt, (x, y), 3, (0, 250, 0), -1)  # rt
                        rq.append(True)
                    else:
                        circle(rt, (x, y), 3, colo, -1)  # rt
                        rq.append(False)
                imshow(ca, rt)  # rt
                if ca == "Blue":
                    self.blue.write(rt)
                else:
                    self.red.write(rt)
                return rq

            rrb = e("Red")

            # putText(self.frame, m, (50, 40), FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)'''

            # self.func = self.sign
            def insert(pic, widget):
                pic = cvtColor(pic, COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(pic.data, pic.shape[1], pic.shape[0],
                                                 QtGui.QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
                widget.setPixmap(QPixmap(convertToQtFormat))

            ret, self.frame = self.cap.read()
            print(ret)
            if not ret:
                self.frame = imread('Colors.jpg')
            try:
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
            except Exception:
                pass
            # imshow("Frame", self.frame)
            # self.out.write(self.frame)
            if waitKey(1) == ord("q"):
                pass
            sleep(time)
        destroyAllWindows()
        self.func = None
        self.i = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Vision(0)
    f.sign(1000)
    f.release()
    sys.exit(app.exec())
