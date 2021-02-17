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
        self.img = None
        with open("config/base.json") as file:
            self.DATA = json.load(file)
        self.i = 0
        self.BASE_DATA = Base_date("config/signs.sqlite3")
        self.new_points = []
        self.point = []
        self.bool = False
        self.im = None
        self.red = True
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.radioButton_2.setEnabled(False)
        self.buttonGroup.buttonClicked.connect(self.frequency)
        self.buttonGroup_2.buttonClicked.connect(self.image_group)
        self.spinBox.valueChanged.connect(self.change)
        self.spinBox_2.valueChanged.connect(self.change)

    def change(self):
        if self.sender() == self.spinBox:
            print(self.spinBox.value())
            self.point[0] = self.spinBox.value() - 1
        else:
            self.point[1] = self.spinBox_2.value() - 1
        self.paint()

    def add_sign(self):
        if len(self.lineEdit.text()) and self.label.text() != "Место для знака":
            a = "blue_signs"
            if self.red:
                a = "red_signs"
            base, dop = self.paint()
            self.BASE_DATA.insert(table=a, res=", ".join(
                ["'name'", "'values'", "'dop_points'", "'dop_values'"]),
                                  z=[self.lineEdit.text(), ", ".join([str(i) for i in base]),
                                     ", ".join([f"{x}:{y}" for x, y in self.new_points]),
                                     ", ".join([str(i) for i in dop])])
            self.lineEdit.clear()
            self.picture()

    def run(self):
        if self.point not in self.new_points:
            self.new_points.append(self.point)
            self.paint()

    def image_group(self):
        self.im = self.buttonGroup_2.checkedId() == -3
        self.paint()

    def frequency(self):  # метод выбора частоты события
        self.bool = True
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.radioButton.setEnabled(True)
        self.radioButton_2.setEnabled(True)
        self.red = self.buttonGroup.checkedId() == -3
        self.paint()

    def paint(self):
        if self.pushButton.text() != "Удалить картинку":
            return
        radius = 5
        img = cv2.imread("input.png")
        img = cv2.resize(img, (128, 128))
        image = img.copy()
        c = self.DATA['blue']['range']
        self.points = self.DATA['blue']['points']
        if self.red:
            c = self.DATA['red']['range']
            self.points = self.DATA['red']['points']
        img = cv2.inRange(img, (c[0], c[1], c[2]), (c[3], c[4], c[5]))
        if self.im:
            cv2.imwrite("input1.png", img)
            image = cv2.imread("input1.png")
        base = []
        for x, y in self.points:
            t = False
            color = (255, 0, 0)
            if self.red:
                color = (0, 0, 255)
            if img[y * 2][x * 2]:
                color = (0, 255, 0)
                t = True
            base.append(t)
            cv2.circle(image, (x * 2, y * 2), radius, color, -1)
        dop = []
        for x, y in self.new_points:
            t = False
            color = (255, 0, 0)
            if self.red:
                color = (0, 0, 255)
            if img[y * 2][x * 2]:
                color = (0, 255, 0)
                t = True
            dop.append(t)
            cv2.circle(image, (x * 2, y * 2), radius, color, -1)
        k = []
        if len(self.point):
            k = [self.point]
        for x, y in k:
            color = (255, 0, 0)
            if self.red:
                color = (0, 0, 255)
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
            self.point = [x, y]
            self.spinBox.setValue(x)
            self.spinBox_2.setValue(y)
            self.paint()

    def keyPressEvent(self, event):  # метод удаления события
        if event.key() == 16777223:
            if len(self.point):
                self.point = []
            elif len(self.new_points):
                self.new_points.pop(-1)
            self.paint()

    def picture(self):  # метод для добавления и удаления картинки при добавлении события
        if self.pushButton.text() == "Добавить картинку":
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            if len(self.fname):
                try:
                    if self.fname == os.path.abspath("input.png").replace("\\", "/"):
                        raise shutil.SameFileError
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
