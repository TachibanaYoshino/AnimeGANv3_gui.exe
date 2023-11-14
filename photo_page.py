import sys, os, time, traceback

import numpy as np
from PyQt5.QtGui import QPainter, QImage, QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QRadioButton, QWidget, QButtonGroup, QPlainTextEdit, \
    QHBoxLayout, QStyleOption, QStyle, QLabel
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QProgressBar
from PIL import Image
import face_det
import onnxruntime

ort_sess_options = onnxruntime.SessionOptions()
ort_sess_options.intra_op_num_threads = int(os.environ.get('ort_intra_op_num_threads', 0))


class Thread_01(QThread):  # Thread 1
    updated_text = pyqtSignal(str)
    pb_signal = pyqtSignal(int)  ###define a signal variable
    def __init__(self, imgs, input_dir, output_dir, ort_session, det, process_image, save_images):
        super().__init__()
        self.imgs =imgs
        self.input_dir =input_dir
        self.output_dir =output_dir
        self.ort_session =ort_session
        self.process_image =process_image
        self.save_images =save_images
        self.det = det
        self.running = True

    def accept(self, running):  ###Used to accept the code passed from the main interface
        self.running = running

    def run(self):
        try:
            begin = time.time()
            num = len(self.imgs)
            for i, f in enumerate(self.imgs):
                st = time.time()
                if self.running == False:
                    break
                img = Image.open(os.path.join(self.input_dir, f)).convert("RGB")
                scale = np.array(img).shape[:2][::-1]
                max_edge = max(scale[0], scale[1])
                if max_edge > 1280:  # Limit the maximum size of the image to prevent face detection errors
                    scale_factor = 1280 / max_edge
                    height = int(round(scale[1] * scale_factor))
                    width = int(round(scale[0] * scale_factor))
                    img = img.resize((width, height), Image.ANTIALIAS)
                if self.det == True:
                    bboxes, points = face_det.detect_face(np.array(img))
                    if self.running == False:
                        break
                    if bboxes is None:
                        self.updated_text.emit(f"> {f} has no face.")  # Send log value signal
                        continue
                    else:
                        margin_box = face_det.margin_face(bboxes[0], np.array(img).shape[:2])
                        img = np.array(img)[margin_box[1]:margin_box[3], margin_box[0]:margin_box[2]]
                        img = Image.fromarray(img)
                img = self.process_image(img)
                if self.running == False:
                    break
                ort_inputs = {self.ort_session.get_inputs()[0].name: img}
                ort_outs = self.ort_session.run(None, ort_inputs)[0]
                self.save_images(ort_outs, os.path.join(self.output_dir, f), scale)
                self.updated_text.emit(f"> running {i+1}/{num} : {f}, time: {time.time() - st:.3f}s")
                self.pb_signal.emit(int((i+1) / num * 100))  # Send a progress bar value signal
            self.updated_text.emit(f"> total time: {time.time() - begin:.3f}s")
            self.updated_text.emit(f"> {'-' * 3} End running. {'-' * 3} \n")
        except:
            self.updated_text.emit(f"> {traceback.format_exc()} ")
            print(traceback.format_exc())

class photo_window(QWidget):
    def __init__(self, parent=None):
        super(photo_window, self).__init__(parent)
        # self.setWindowTitle("Photo Conversion")
        self.setObjectName("winn")
        self.setStyleSheet("QWidget#winn{border-radius:12px; background-color:rgba(245, 245, 245,66); margin:30px;}")
        # left
        self.label = QLabel('Input Folder:', self)  # static tags
        self.label.setStyleSheet(" color:white; font-size:14px; font-weight:normal;font-family:Microsoft YaHei;")
        self.line_edit = QLineEdit(self)  # Single line edit box
        self.line_edit.setPlaceholderText('')
        self.line_edit.setText(r'')
        self.line_edit.setStyleSheet(
            "border-radius:4px; border:1px solid DeepSkyBlue; height:24px; color: white; background-color:rgba(245,245,245,0); font-size:14px; font-weight:normal;font-family:Roman times;")
        self.btn_img = QPushButton("Broswer", self)
        self.btn_img.setFixedWidth(80)

        self.input1_lay = QHBoxLayout()
        self.input1_lay.addWidget(self.label)
        self.input1_lay.addWidget(self.line_edit)
        self.input1_lay.addWidget(self.btn_img)
        self.input1_lay.setAlignment(Qt.AlignCenter)
        self.input1_lay.setStretch(0, 1)
        self.input1_lay.setStretch(1, 3)
        self.input1_lay.setStretch(2, 1)
        self.input1_lay.setContentsMargins(0, 0, 0, 0)
        self.input1_lay.setSpacing(15)

        self.label2 = QLabel('onnx File:   ', self)
        self.label2.setStyleSheet(" color:white; font-size:14px;font-weight:normal;font-family:Microsoft YaHei;")
        self.line_edit2 = QLineEdit(self)
        self.line_edit2.setPlaceholderText('')
        self.line_edit2.setText(r'')
        self.line_edit2.setStyleSheet(
            "border-radius:4px; border:1px solid DeepSkyBlue; height: 24px; color: white; background-color:rgba(245,245,245,0); font-size:14px;font-weight:normal;font-family:Roman times;")
        self.btn_img2 = QPushButton("Broswer", self)
        self.btn_img2.setFixedWidth(80)

        self.input2_lay = QHBoxLayout()
        self.input2_lay.addWidget(self.label2)
        self.input2_lay.addWidget(self.line_edit2)
        self.input2_lay.addWidget(self.btn_img2)
        self.input2_lay.setAlignment(Qt.AlignCenter)
        self.input2_lay.setStretch(0, 1)
        self.input2_lay.setStretch(1, 3)
        self.input2_lay.setStretch(2, 1)
        self.input2_lay.setContentsMargins(0, 0, 0, 0)
        self.input2_lay.setSpacing(15)

        self.label3 = QLabel('Extract face:   ', self)
        self.label3.setStyleSheet(" color:white; font-size:14px;font-weight:normal;font-family:Microsoft YaHei;")
        self.rb11 = QRadioButton('Yes', self)
        self.rb12 = QRadioButton('No', self)
        self.rb11.setChecked(True)
        [i.setStyleSheet(" color:white; font-size:14px;font-weight:bold;font-family:Microsoft YaHei;") for i in
         (self.rb11, self.rb12)]
        self.bg1 = QButtonGroup(self)
        self.bg1.addButton(self.rb11, 11)
        self.bg1.addButton(self.rb12, 12)
        self.input3_lay = QHBoxLayout()
        self.input3_lay.addWidget(self.label3)
        self.input3_lay.addWidget(self.rb11)
        self.input3_lay.addWidget(self.rb12)
        self.input3_lay.setAlignment(Qt.AlignCenter)
        self.input3_lay.setStretch(0, 1)
        self.input3_lay.setStretch(1, 1)
        self.input3_lay.setStretch(2, 1)
        self.input3_lay.setContentsMargins(0, 0, 0, 0)
        self.input3_lay.setSpacing(15)

        self.btn_start = QPushButton("Start", self)
        self.btn_stop = QPushButton("Stop", self)
        self.input4_lay = QHBoxLayout()
        self.input4_lay.addWidget(self.btn_start)
        self.input4_lay.addWidget(self.btn_stop)
        self.input4_lay.setAlignment(Qt.AlignCenter)
        self.input4_lay.setStretch(0, 1)
        self.input4_lay.setStretch(1, 1)
        self.input4_lay.setContentsMargins(0, 0, 0, 0)
        self.input4_lay.setSpacing(15)

        self.pb = QProgressBar(self)
        self.pb.setStyleSheet(
            "QProgressBar{ height: 14px; padding: 2px; border: 1px solid Yellow; border-radius: 8px; background-color: rgba(245,245,245,0); text-align:center; color:white; font-size:12px; font-weight:bold;font-family:Microsoft YaHei;}"
            # "QProgressBar::chunk{background-color: rgba(255,255,255,128); height: 10px; width: 10px; margin: 0.5px; border-radius: 5px; border: 1px normal;}")
            "QProgressBar::chunk{background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2: 0.523, stop:0 rgba(254,121,199,255), stop:1 rgba(170,85,255,255)); border-radius: 5px; border: 1px normal;}")
        self.pb.setRange(0, 100)
        self.pb.hide()
        self.input5_lay = QHBoxLayout()
        self.input5_lay.addWidget(self.pb)
        self.input5_lay.setContentsMargins(0, 5, 0, 0)
        self.input5_lay.setSpacing(15)

        self.left_V = QVBoxLayout()
        self.left_V.addLayout(self.input1_lay)
        self.left_V.addLayout(self.input2_lay)
        self.left_V.addLayout(self.input3_lay)
        self.left_V.addLayout(self.input4_lay)
        self.left_V.addLayout(self.input5_lay)
        self.left_V.addStretch(3)
        self.left_V.setAlignment(Qt.AlignCenter)
        self.left_V.setSpacing(10)
        self.left_V.setStretch(0, 1)
        self.left_V.setStretch(1, 1)
        self.left_V.setStretch(2, 1)
        self.left_V.setStretch(3, 1)
        self.left_V.setStretch(4, 1)
        # self.left_V.setStretch(3,3)
        self.left_V.setContentsMargins(20, 20, 0, 20)

        # right
        self.tet = QPlainTextEdit(self)
        self.tet.setReadOnly(True)
        self.cursor = self.tet.textCursor()
        self.tet.setLineWrapMode(QPlainTextEdit.NoWrap)  # Turn off soft line wrapping, that is, characters will wrap directly after they exceed the width of the control.
        self.tet.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tet.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tet.setMaximumBlockCount(3000)  # Set the maximum number of blocks, which is the number of paragraphs in the text box. The default value is 0, which means no limit. When a limit value is given, the top paragraph will be hidden if the limit value is exceeded.
        self.tet.setPlaceholderText("log.")
        self.tet.setStyleSheet(
            "border-radius:4px; border:1px solid DeepSkyBlue; color:white; font-size:14px; font-weight:bold;font-family:Roman times; background-color:rgba(245,245,245,0)")
        self.btn_Clear = QPushButton("Clear", self)

        self.right_V = QVBoxLayout()
        self.right_h1, self.right_h2 = QHBoxLayout(), QHBoxLayout()
        self.right_h1.addWidget(self.tet)
        self.right_h2.addWidget(self.btn_Clear)

        self.right_V.addLayout(self.right_h1)
        self.right_V.addLayout(self.right_h2)
        # self.right_V.addStretch(0.5)
        self.right_V.setStretch(0, 7)
        self.right_V.setStretch(1, 1)
        # self.right_V.setStretch(2,1)
        self.right_V.setContentsMargins(0, 20, 20, 20)
        self.right_V.setSpacing(10)

        self.top_Hl = QHBoxLayout(self)
        self.top_Hl.addLayout(self.left_V)
        self.top_Hl.addStretch(1)
        self.top_Hl.addLayout(self.right_V)
        self.top_Hl.setStretch(0, 2)
        self.top_Hl.setStretch(1, 1)
        self.top_Hl.setStretch(2, 2)
        self.top_Hl.setAlignment(Qt.AlignCenter)
        self.top_Hl.setContentsMargins(30, 30, 30, 30)
        self.top_Hl.setSpacing(0)  # Remove gaps between controls
        self.setLayout(self.top_Hl)

        for b in [self.btn_img, self.btn_img2, self.btn_start, self.btn_stop, self.btn_Clear]:
            # Set a unified style for each button
            # b.setFixedWidth(100) if b is not self.btn_Clear else b
            b.setStyleSheet("QPushButton{ background:None; }"
                            "QPushButton:hover{background:Pink; border:3px solid rgb(189,252,201); }"
                            "QPushButton{border:1px solid;}"
                            "QPushButton{border-radius:4px}"
                            "QPushButton{border-color:rgb(189,252,201)}"
                            "QPushButton{font-family: Microsoft YaHei}"
                            "QPushButton{font-weight: bold}"
                            "QPushButton{color: white}"
                            "QPushButton{font-size: 13px}"
                            "QPushButton{height: 20px;}"
                            "QPushButton{padding: 4px }"
                            )
        # event
        self.running = False
        self.thread_01 = None
        self.det = True
        self.ort_session = None
        self.btn_img.clicked.connect(self.open_dir)
        self.btn_img2.clicked.connect(self.onnx_path)
        self.btn_start.clicked.connect(self.run)
        self.btn_stop.clicked.connect(self.stop_run)
        self.btn_Clear.clicked.connect(self.clear_log)
        self.bg1.buttonClicked.connect(self.rbclicked)

    def open_dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self, "Open dir", "")
        if dir_choose == "":
            return
        else:
            self.line_edit.setText(dir_choose)

    def onnx_path(self):
        files, filetype = QFileDialog.getOpenFileName(None, "Open onnx file", "", "(*.onnx)")
        if "" == files:
            return
        if not files.endswith(".onnx"):
            self.write("> Please select the correct onnx file.")
            return
        else:
            self.line_edit2.setText(files)

    def rbclicked(self):
        if self.bg1.checkedId() == 11:
            self.det = True
        else:
            self.det = False

    def run(self):
        if self.thread_01 is not None or self.running == True:
            self.write(f"> It is running now. ")
            return

        input_dir = self.line_edit.text()
        if input_dir == "":
            self.write("> Please select the correct image directory.")
            self.running = False
            return
        if self.line_edit2.text() == "":
            self.write("> Please select the correct onnx file.")
            self.running = False
            return
        try:
            self.ort_session = onnxruntime.InferenceSession(self.line_edit2.text(), sess_options=ort_sess_options)
            self.write(f"> Loaded {self.line_edit2.text()}.")
        except:
            print(traceback.format_exc())
            self.write("> Failed to load onnx file.")
            self.running = False
            return

        try:
            imgs = [x for x in os.listdir(input_dir) if x.split('.')[-1].lower() in ['jpg', 'jpeg','png','tiff', 'bmp']]
            output_dir = os.path.join(input_dir, "results")
            os.makedirs(output_dir, exist_ok=True)
            self.write(f"> {'-' * 3} Start running. {'-' * 3}")

            self.pb.setValue(0)
            self.thread_01 = Thread_01( imgs, input_dir, output_dir, self.ort_session, self.det, self.process_image, self.save_images)  # Create thread
            self.thread_01.finished.connect(self.handle_done) # Gives a completion signal when the thread completes
            self.thread_01.pb_signal.connect(self.th_callback) # Thread gives progress bar signal
            self.thread_01.updated_text.connect(self.th_log) # Thread gives log printing signal
            self.thread_01.start()  # Start thread
            self.running=True
            self.pb.show()

        except:
            self.write(f"> Error: {traceback.format_exc()}")
            self.running = False
            if self.thread_01 is not None:
                self.thread_01=None
            print(traceback.format_exc())

    def stop_run(self):
        if self.thread_01 is not None and self.running==True:
            self.thread_01.accept(False)
            self.running=False
            self.write("> Conversion has stopped.")
        else:
            self.write("> Conversion has not started yet.")

    def handle_done(self):
        self.running = False
        self.thread_01 = None

    # Return progress bar parameters
    def th_callback(self, i):
        self.pb.setValue(i)

    def th_log(self, log):
        self.write(log)

    def clear_log(self):
        self.tet.setPlainText("")

    def write(self, log):
        """"""
        self.cursor.movePosition(QTextCursor.End)
        self.cursor.insertText(log + '\n')
        self.tet.setTextCursor(self.cursor)
        self.tet.ensureCursorVisible()

    def process_image(self, img, x8=True):
        if self.det == True:
            img = img.resize((512, 512), Image.ANTIALIAS)
        else:
            h, w = np.array(img).shape[:2]
            if x8:
                def to_8s(x):
                    return 256 if x < 256 else x - x % 8
                def to_16s(x):
                    return 256 if x < 256 else x - x % 16
                if '_tiny_' in self.line_edit2.text():
                    img = img.resize((to_16s(w), to_16s(h)), Image.ANTIALIAS)
                else:
                    img = img.resize((to_8s(w), to_8s(h)), Image.ANTIALIAS)
        img = np.array(img).astype(np.float32) / 127.5 - 1.0
        # img = img.transpose(2, 0, 1)
        img = np.expand_dims(img, axis=0)
        return img

    def save_images(self, images, image_path, scale):

        # images = np.concatenate( [x for x in images], axis=1)
        images = (images + 1.) / 2 * 255
        images = np.clip(images, 0, 255).astype(np.uint8)
        output = []
        if self.det == False:
            for x in images:
                img = Image.fromarray(x)
                img = img.resize(scale, Image.ANTIALIAS)
                output.append(np.array(img))
            images = np.concatenate([x for x in output], axis=1)
        else:
            images = np.concatenate([x for x in images], axis=1)
        Image.fromarray(images).save(image_path, quality=98)

    # Rewrite paintEvent, otherwise you cannot use a style sheet to define the appearance
    def paintEvent(self, evt):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        # anti-aliasing
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
