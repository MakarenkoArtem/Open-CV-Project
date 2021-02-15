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


class Sign(QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.picture)
        self.pushButton_3.clicked.connect(self.run)
        self.setMouseTracking(True)
        self.img = None
        with open("config/base.json") as file:
            self.DATA = json.load(file)
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
        print(self.red)
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
        k = self.points + self.new_points
        if len(self.point):
            k += [self.point]
            print(k)
        for x, y in k:
            color = (0, 0, 255)
            if not self.red:
                color = (255, 0, 0)
            if img[y * 2][x * 2]:
                color = (0, 255, 0)
            cv2.circle(image, (x * 2, y * 2), radius, color, -1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        self.label.setPixmap(QPixmap(convertToQtFormat))

    def mousePressEvent(self, event):
        x, y = (event.x() - self.label.x()) // 2, (event.y() - self.label.y()) // 2
        if 0 <= x < 64 and 0 <= y < 64 and self.pushButton.text() != "Добавить картинку":
            self.point = [x, y]
            self.spinBox.setValue(x)
            self.spinBox_2.setValue(y)
            self.paint()
        '''if (event.button() == Qt.LeftButton):
            print("Левая")
        elif (event.button() == Qt.RightButton):
            print("Правая")'''

    def keyPressEvent(self, event):  # метод удаления события
        print(event.key())

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
            self.pushButton.setText("Добавить картинку")
        self.paint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Sign()
    f.show()
    try:
        os.remove("input.png")
        os.remove("input1.png")
    except FileNotFoundError:
        pass
    sys.exit(app.exec())
