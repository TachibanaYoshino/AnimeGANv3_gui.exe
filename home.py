# -*- coding: utf-8 -*-
import sys, base64
from io import  BytesIO
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush,QImage,QIcon,QPixmap, QPalette
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QDesktopWidget,QStatusBar,QHBoxLayout,QVBoxLayout, QLabel
from PyQt5.QtWidgets import QMessageBox
from  PIL import  Image
from photo_page import photo_window
from bottom_info import bottom_weight
import assets_bin

bg_img = Image.open(BytesIO(base64.b64decode(assets_bin.bg)))
ico_img = Image.open(BytesIO(base64.b64decode(assets_bin.ico)))
# bg_img.show()

app_name='AnimeGANv3-photo'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.available_geometry = QDesktopWidget().availableGeometry()
        init_width = int(self.available_geometry.width() * 0.5)
        init_height = int(self.available_geometry.height() * 0.5)
        self.setWindowTitle(app_name)
        self.resize(init_width, init_height)
        self.setMinimumSize(init_width, init_height)
        self.setWindowFlags(Qt.Window)
        # Instantiate the status bar and set the status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.ico_img = np.array(ico_img)
        self.setWindowIcon(QIcon(QPixmap.fromImage(QImage(self.ico_img, self.ico_img.shape[1], self.ico_img.shape[0], self.ico_img.strides[0], QImage.Format_RGBA8888))))
        self.setObjectName("MainWindow")
        self.bg = bg_img
        bg = self.bg.resize((init_width, init_height), Image.ANTIALIAS)
        frame = np.array(bg)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap.fromImage(QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888))))
        self.setPalette(palette)
        ###### Create interface ######
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.mainLayout = QVBoxLayout(self.centralwidget)#global landscape
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)  # Remove gaps between controls

        ###################
        photo_win = photo_window()
        bottom = bottom_weight()
        self.HL1, self.HL2 = QHBoxLayout(), QHBoxLayout()
        self.bHL1, self.bHL2, self.bHL3 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout()

        self.bHL1.addWidget(QLabel())
        self.bHL2.addWidget(bottom)
        self.bHL3.addWidget(QLabel())

        self.HL1.addWidget(photo_win)
        self.HL2.addLayout(self.bHL1)
        self.HL2.addLayout(self.bHL2)
        self.HL2.addLayout(self.bHL3)
        self.HL2.setStretch(0,2)
        self.HL2.setStretch(1,1)
        self.HL2.setStretch(2,2)
        self.mainLayout.addLayout(self.HL1)
        self.mainLayout.addStretch(2)
        self.mainLayout.addLayout(self.HL2)
        self.mainLayout.setStretch(0,9)
        self.mainLayout.setStretch(1,2)
        self.mainLayout.setStretch(2,1)
        self.mainLayout.setSpacing(0)

    def resizeEvent(self, event):
        w, h = event.size().width(), event.size().height()
        bg = self.bg.resize((w, h), Image.ANTIALIAS)
        frame = np.array(bg)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(
            QPixmap.fromImage(QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888))))
        self.setPalette(palette)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'Do you want to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
