import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageClassifierApp(QWidget):
    def __init__(self):
        super().__init__()

        self.image_folder = None
        self.current_image_index = 0
        self.good_folder = 'good_imgs'
        self.bad_folder = 'bad_imgs'

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Classifier')
        self.setFixedSize(1280, 800)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.load_image_button = QPushButton('Load Images', self)
        self.load_image_button.clicked.connect(self.loadImages)

        self.good_button = QPushButton('Good (Press "g")', self)
        self.good_button.clicked.connect(lambda: self.classifyImage('good'))

        self.bad_button = QPushButton('Bad (Press "b")', self)
        self.bad_button.clicked.connect(lambda: self.classifyImage('bad'))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.load_image_button)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.good_button)
        self.layout.addWidget(self.bad_button)

        self.setLayout(self.layout)

    def loadImages(self):
        self.image_folder = QFileDialog.getExistingDirectory(self, 'Select Image Folder')
        if self.image_folder:
            self.image_list = [file for file in os.listdir(self.image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.showNextImage()

    def showNextImage(self):
        if self.current_image_index < len(self.image_list):
            image_path = os.path.join(self.image_folder, self.image_list[self.current_image_index])
            pixmap = QPixmap(image_path)
            self.displayImage(pixmap)
        else:
            self.image_label.clear()
            self.current_image_index = 0
            self.image_folder = None

    def displayImage(self, pixmap):
        label_width = self.image_label.width()
        label_height = self.image_label.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def classifyImage(self, label):
        if self.image_folder:
            image_path = os.path.join(self.image_folder, self.image_list[self.current_image_index])
            if label == 'good':
                destination_folder = self.good_folder
            else:
                destination_folder = self.bad_folder

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            shutil.copy(image_path, os.path.join(destination_folder, self.image_list[self.current_image_index]))

            self.current_image_index += 1
            self.showNextImage()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_G:
            self.classifyImage('good')
        elif event.key() == Qt.Key_B:
            self.classifyImage('bad')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageClassifierApp()
    window.show()
    sys.exit(app.exec_())
