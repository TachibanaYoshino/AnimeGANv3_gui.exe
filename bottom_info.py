from PyQt5.QtGui import QBrush, QColor, QIcon, QPixmap, QPainter, QImage, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QApplication, QWidget, QDesktopWidget, QPlainTextEdit, \
    QHBoxLayout,  QStyleOption, QStyle, QLabel, QListWidgetItem
from PyQt5.QtWidgets import QMessageBox, QFrame, QFormLayout, QLineEdit, QGridLayout, QFileDialog


class bottom_weight(QWidget):
    def __init__(self,  parent=None):
        super(bottom_weight, self).__init__(parent)
        self.setObjectName("bw")
        self.setStyleSheet("QWidget#bw{border-radius:12px; background-color:rgba(0,0,0,128); }")

        self.welcome_t = QLabel('Welcome to use AnimeGANv3', self)  # static tags
        self.copyrihgt_t = QLabel('Copyright © 2019-2023 Asher Chan. All Rights Reserved.', self)  # static tags
        self.email_t = QLabel('asher_chan@foxmail.com', self)  # static tags
        self.url_t = QLabel('https://github.com/TachibanaYoshino/AnimeGANv3', self)  # static tags
        self.version_t = QLabel('V1.1', self)  # static tags

        self.h1,self.h2,self.h3,self.h4,self.h5 = QHBoxLayout(),QHBoxLayout(),QHBoxLayout(),QHBoxLayout(),QHBoxLayout()
        self.h1.addWidget(self.welcome_t)
        self.h2.addWidget(self.copyrihgt_t)
        self.h3.addWidget(self.email_t)
        self.h4.addWidget(self.url_t)
        self.h5.addWidget(self.version_t)
        [i.setAlignment(Qt.AlignCenter) for i in [self.h1, self.h2, self.h3, self.h4, self.h5]]

        self.VL = QVBoxLayout()
        [self.VL.addLayout(i) for i in [self.h1, self.h2, self.h3, self.h4, self.h5]]
        self.VL.setAlignment(Qt.AlignCenter)
        self.VL.setSpacing(6)
        self.VL.setContentsMargins(10, 10, 10, 10)

        self.setLayout(self.VL)
        for t in [ self.copyrihgt_t, self.email_t, self.url_t, self.version_t]:
            t.setStyleSheet("color:white; font-size:12px; font-weight:normal;font-family:Microsoft YaHei;")
        self.welcome_t.setStyleSheet("color:white; font-size:18px; font-weight:bold;font-family:Microsoft YaHei;")

    # Rewrite paintEvent, otherwise you cannot use a style sheet to define the appearance
    def paintEvent(self, evt):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        # anti-aliasing
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


    def enterEvent(self, e):  # Move the mouse into label
        for t in [self.copyrihgt_t, self.email_t, self.url_t, self.version_t]:
            t.setStyleSheet("color:white; font-size:12px; font-weight:normal;font-family:Microsoft YaHei;")
        self.welcome_t.setStyleSheet("color:white; font-size:18px; font-weight:bold;font-family:Microsoft YaHei;")
        self.setStyleSheet("QWidget#bw{border-radius:12px; background-color:rgba(0,0,0,128); }")
        self.show()  # When the mouse slides into the QLabel, emit a custom enterQLabel signal and pass in the current SelectQLabel object in the signal
        self.wh = self.size()

    # leaveEvent is a built-in method of QLabel. Override the leaveEvent method here.
    def leaveEvent(self, e):  # Mouse leaves label
        self.setStyleSheet("QWidget#bw{background-color:rgba(0,0,0,0);}")
        for t in [ self.copyrihgt_t, self.email_t, self.url_t, self.version_t]:
            t.setStyleSheet("font-size:12px; color:rgba(0,0,0,0);")
        self.welcome_t.setStyleSheet(" font-size:18px; color:rgba(0,0,0,0);")
        self.setFixedSize(self.wh)

