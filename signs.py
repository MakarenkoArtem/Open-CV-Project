import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from Add_sign import Ui_Dialog
import json
import cv2
import shutil
import os
from base_date import *


class Sign(QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.picture)
        self.pushButton_3.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.add_sign)
        self.setMouseTracking(True)
        self.label.setText("Место для знака")
        with open("config/base.json") as file:
            self.DATA = json.load(file)
        self.BASE_DATA = Base_date("config/signs.sqlite3")
        self.new_point = {"Синий": [], 'Красный': [], 'Белый': [], 'Чёрный': [], 'Жёлтый': []}
        self.new_points = {"Синий": [], 'Красный': [], 'Белый': [], 'Чёрный': [], 'Жёлтый': []}
        '''self.new_black_points, self.new_white_points = [], []
        self.new_yellow_points, self.new_red_points, self.new_blue_points = [], [], []
        self.new_black_point, self.new_white_point = [], []
        self.new_yellow_point, self.new_red_point, self.new_blue_point = [], [], []'''
        self.im, self.dop_color, self.color, self.img = None, 'Чёрный', 'Красный', None
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.radioButton_2.setEnabled(False)
        for i in self.buttonGroup_3.buttons():
            i.setEnabled(False)
        self.buttonGroup.buttonClicked.connect(self.paint)
        self.buttonGroup_2.buttonClicked.connect(self.frequency)
        self.buttonGroup_3.buttonClicked.connect(self.image_group)
        self.spinBox.valueChanged.connect(self.change)
        self.spinBox_2.valueChanged.connect(self.change)

    def change(self):
        self.new_point[self.dop_color] = [self.spinBox.value() - 1, self.spinBox_2.value() - 1]
        self.paint()

    def add_sign(self):
        if len(self.lineEdit.text()) and self.label.text() != "Место для знака":
            if self.color == "Синий":
                table = "blue_signs"
            elif self.color == "Красный":
                table = "red_signs"
            else:
                table = "white_signs"
            points = {}
            names = ["'name'", "'values'", "'black_points'", "'black_values'", "'white_points'", "'white_values'", "'yellow_points'", "'yellow_values'", "'red_points'", "'red_values'", "'blue_points'", "'blue_values'"]
            for i in range(-2, -7, -1):
                self.dop_color = self.buttonGroup_3.button(i).text()
                points[self.dop_color] = self.paint()
            znach = [self.lineEdit.text()]
            for i in ['Чёрный', 'Белый', 'Жёлтый', 'Красный', 'Синий']:
                if points[i][0] is not None:
                    znach.insert(1, ", ".join([str(k) for k in points[i][0]]))
                znach.append(", ".join([":".join([str(j) for j in k]) for k in self.new_points[i]]))
                znach.append(", ".join([str(k) for k in points[i][1]]))
            self.BASE_DATA.insert(table=table, res=", ".join(names), z=znach)
            self.lineEdit.clear()
            self.image_group()
            self.picture()

    def run(self):
        if self.new_point[self.dop_color] not in self.new_points[self.dop_color] and len(self.new_point[self.dop_color]):
            self.new_points[self.dop_color].append(self.new_point[self.dop_color])
            self.new_point[self.dop_color] = []
        self.paint()

    def image_group(self):
        self.dop_color = self.buttonGroup_3.checkedButton().text()
        self.paint()

    def frequency(self):  # метод выбора частоты события
        self.color = self.buttonGroup_2.checkedButton().text()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.radioButton.setEnabled(True)
        self.radioButton_2.setEnabled(True)
        for i in self.buttonGroup_3.buttons():
            i.setEnabled(True)
        self.paint()

    def paint(self):
        if self.pushButton.text() != "Удалить картинку":
            return
        radius = 5
        img = cv2.imread("input.png")
        img = cv2.resize(img, (128, 128))
        image = img.copy()
        points = []
        base = None
        if self.dop_color == "Красный":
            c = self.DATA['red']['range']
            if self.color == "Красный":
                points = self.DATA['red']['points']
                base = []
        elif self.dop_color == "Синий":
            c = self.DATA['blue']['range']
            if self.color == "Синий":
                points = self.DATA['blue']['points']
                base = []
        elif self.dop_color == 'Чёрный':
            c = [0] * 3 + [15] * 3
        elif self.dop_color == 'Жёлтый':
            c = self.DATA['yellow']['range']
        else:
            c = self.DATA['white']['range']
            if self.color == "Белый":
                points = self.DATA['white']['points']
                base = []
        img = cv2.inRange(img, (c[0], c[1], c[2]), (c[3], c[4], c[5]))
        if self.buttonGroup.checkedId() != -2:
            cv2.imwrite("input1.png", img)
            image = cv2.imread("input1.png")
        for x, y in points:
            t = False
            color = (255, 0, 150)
            if self.color == "Красный":
                color = (0, 0, 255)
            elif self.color == "Синий":
                color = (255, 0, 0)
            if img[y * 2][x * 2]:
                color = (0, 255, 0)
                t = True
            base.append(t)
            cv2.circle(image, (x * 2, y * 2), radius, color, -1)
        dop = []
        for x, y in self.new_points[self.dop_color]:
            t = False
            color = (255, 0, 150)
            if self.dop_color == "Красный":
                color = (0, 0, 255)
            elif self.dop_color == "Синий":
                color = (255, 0, 0)
            if img[y * 2][x * 2]:
                color = (0, 255, 0)
                t = True
            dop.append(t)
            cv2.circle(image, (x * 2, y * 2), radius, color, -1)
        if len(self.new_point[self.dop_color]):
            for x, y in [self.new_point[self.dop_color]]:
                color = (255, 0, 150)
                if self.dop_color == "Красный":
                    color = (0, 0, 255)
                elif self.dop_color == "Синий":
                    color = (255, 0, 0)
                if img[y * 2][x * 2]:
                    color = (0, 255, 0)
                cv2.circle(image, (x * 2, y * 2), radius, color, -1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        self.label.setPixmap(QPixmap(convertToQtFormat))
        return base, dop

    def mousePressEvent(self, event):
        x, y = (event.x() - self.label.x()) // 2 - 1, (event.y() - self.label.y()) // 2 - 1
        if 0 <= x < 64 and 0 <= y < 64 and self.pushButton.text() != "Добавить картинку":
            self.new_point[self.dop_color] = [x, y]
            self.spinBox.setValue(x + 1)
            self.spinBox_2.setValue(y + 1)
            self.paint()

    def keyPressEvent(self, event):  # метод удаления события
        if event.key() == 16777223:
            if len(self.new_point[self.dop_color]):
                self.new_point[self.dop_color] = []
            elif len(self.new_points[self.dop_color]):
                self.new_points[self.dop_color].pop(-1)
            self.paint()

    def picture(self):  # метод для добавления и удаления картинки при добавлении события
        if self.pushButton.text() == "Добавить картинку":
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            if len(self.fname):
                try:
                    if self.fname == os.path.abspath("input.png").replace("\\", "/") or self.fname.split(".")[-1] not in ['jpg', 'png', 'bmp']:
                        raise shutil.SameFileError
                    print(self.fname)
                    shutil.copy(self.fname, "input.png")
                    self.pushButton.setText("Удалить картинку")
                    self.paint()
                except shutil.SameFileError:
                    self.fname = None
                    self.label.setText(
                        "Данный файл не\nявляется изображением\nили его нельзя открыть")
        else:
            self.image = None
            self.label.clear()
            self.label.setText("Место для знака")
            self.pushButton.setText("Добавить картинку")
        self.paint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Sign()
    f.show()
    app.exec()
    try:
        os.remove("input.png")
        os.remove("input1.png")
    except FileNotFoundError:
        pass
    sys.exit()
