import sys

import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import LV3
import LV2

class PhotoLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
        }''')

    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)
        self.setStyleSheet('''
        QLabel {
            border: none;
        }''')


class Template(QWidget):
    def __init__(self):
        super().__init__()
        self.level = 3
        self.img_path = ""
        self.photo = PhotoLabel()

        btn1 = QPushButton('Browse')
        btn1.clicked.connect(self.open_image)

        btn2 = QPushButton('Current level: ')
        btn2.clicked.connect(self.change_level)

        self.label1 = QLabel('3')

        btn3 = QPushButton('Run')
        btn3.clicked.connect(self.process)

        btn4 = QPushButton('Reset')
        btn4.clicked.connect(self.reset)

        btn5 = QPushButton('Save')
        btn5.clicked.connect(self.save)

        grid = QGridLayout(self)
        grid.addWidget(btn2, 0, 0)
        grid.addWidget(self.label1, 0, 1)
        grid.addWidget(btn1, 0, 2)
        grid.addWidget(btn3, 0, 3)
        grid.addWidget(btn4, 0, 4)
        grid.addWidget(btn5, 0, 5)
        grid.addWidget(self.photo, 1, 0, 1, 6)
        self.setAcceptDrops(True)
        self.resize(300, 200)

    def change_level(self):
        if (self.level == 2):
            self.level = 3
            self.label1.setText('3')
        else:
            self.level = 2
            self.label1.setText('2')

    def reset(self):
        if self.level == 2:
            LV2.resetFunc()
        else:
            LV3.resetFunc()
        self.img = []
        self.open_image(self.img_path, action=2)

    def save(self):
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename, self.img)

    def process(self):
        if self.img_path:
            if self.level == 3:
                self.img = LV3.mainFunc(self.img_path)
            else:
                self.img = LV2.mainFunc(self.img_path)
            self.open_image(action=1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            filename = event.mimeData().urls()[0].toLocalFile()
            event.accept()
            self.open_image(filename, 0)
        else:
            event.ignore()

    def open_image(self, filename=None, action=0):
        if action==0:
            if not filename:
                filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
                if not filename:
                    return
            self.img_path = filename
            self.photo.setPixmap(QPixmap(filename))
        elif action == 1:
            cvImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            height, width, channel = cvImg.shape
            bytesPerLine = 3 * width
            qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.photo.setPixmap(QPixmap.fromImage(qImg))
        else:
            self.photo.setPixmap(QPixmap(filename))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())