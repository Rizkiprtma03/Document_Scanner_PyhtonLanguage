# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design_Sample.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog,QMessageBox
from PyQt5.QtCore import *
from PyQt5 import QtCore
from skimage.filters import threshold_local
import imutils
from PIL import Image
from PyQt5.QtGui import QPixmap
import cv2
from pypower.transform import four_point_transform


class Ui_MainWindow(object):
    def Browser(self):
        widget = QWidget()
        if self.pushButton.isChecked():
            self.pushButton_2.setDisabled(1)
        else:
            self.pushButton_2.setDisabled(0)
        self.fname = QFileDialog.getOpenFileName(widget, "Unggah Gambar", "", "Image Files(*.jpg *.gif *.bmp *.png *.jpeg)")
        self.pix = QPixmap(self.fname[0])
        print(self.fname[0])
        self.label_3.setPixmap(self.pix.scaledToWidth(250))
        self.lineEdit.setText(self.fname[0])

    def Scanner(self):
        # Input Gambar Original
        image = cv2.imread(self.fname[0])
        ratio = image.shape[0] / 500.0 #500 piksel
        print("\n",image)
        # resizing ukuran gambar.
        orig = image.copy()
        image = imutils.resize(image, height=500)
        # merubah gambar dari RGB ke GRAY SCALE
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # merubah citra GRAY SCALE menjadi Blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # (5,5) ukuran kernel dan 0 adalah sigma untuk menentukan jumlah blur
        # GRAY SCALE Blur di cari deteksi tepi menggunakan operator Canny
        edged = cv2.Canny(blurred, 55, 175)  # 55 untuk MinThreshold dan 175 untuk MaxThreshold
        # Menemukan titik untuk Contours nya #Mengambil contour dengan List dan Approx Simple.
        contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        byframe = image.copy()
        titik_kontur = cv2.drawContours(byframe, contours, -1, (255, 255, 0), 2)
        # contours = sorted( contours, key = cv2.contourArea, reverse= True )[:5]
        # the loop extracts the boundary contours of the page
        maxArea = 0
        biggest = []
        for c in contours:
            area = cv2.contourArea(c) #  digunakan untuk mengurutkan contours berdasarkan luas area (cv2.contourArea)
            # dimana contour dengan ukuran paling besar akan berada di depan dari variable list.
            if area > 1000:
                p = cv2.arcLength(c, True)
                edges = cv2.approxPolyDP(c, 0.01 *  p, True)
                if area > maxArea and len(edges) == 4:
                    biggest = edges
                    maxArea = area

        if len(biggest) != 0:
            drawcontours = cv2.drawContours(image, biggest, -1, (255, 255, 0), 18)
            #drawcontours2 = cv2.resize(drawcontours, (255, 255))

        # Merubah Dokumen yang sudah ditentukan titik konturnya, akan di crop perspective transform, menjadi bird eye view effect

        warped = four_point_transform(orig, biggest.reshape(4, 2) * ratio)
        warped1 = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        Threshold = threshold_local(warped1,15,offset=10, method="mean")
        warped_copy = (warped1 > Threshold).astype("uint8") * 255

        # Display
        cv2.imshow("Original", imutils.resize(orig, height=500))
        cv2.imshow("Gray", gray)
        cv2.imshow("Blur", blurred)
        self.messagebox("Step 1\n\n 1. Citra Original\n 2. Merubah Citra RGB ke Grayscale\n 3. Lalu citra tersebut dibuat menjadi blur")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow("Deteksi Tepi", edged)
        cv2.imshow("DrawContours", titik_kontur)
        cv2.imshow("BiggestContours", drawcontours)
        self.messagebox("Step 2\n\n 1. Dari citra Blur, Lalu dilakukan deteksi tepi \n 2. Citra yang sudah di deteksi tepi nya akan dicari garis/titik menggunakan Contour \n "
                        "3. Setelah garis sudah ditemuka dengan Contour, maka garis tersebut diubah menjadi empat titik Contour pada citra yang ingin di scan")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow("Scanned Without Shadow", imutils.resize(warped_copy,height=550))
        cv2.imshow("Scanned Orisinil", imutils.resize(warped,height=550))
        self.messagebox("Step 3\n\n 1. Dari citra yang sudah ditentukan 4 titik tersebut dengan Contour, selanjutnya akan di proses Transformation Prespective/ bird eye view effect \n "
                        "2. Citra yang sudah dilalukan Transformation Perspective lalu dilakukan Scanning\n ")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Save File PNG and PDF
        print("\n------ Saving the Scanned Image -------")
        cv2.imwrite("./Output_png/Threshold_.png", warped_copy)
        cv2.imwrite("./Output_png/Orisinil_.png", warped)
        path_1 = "./Output_png/Threshold_.png"
        path_2 = "./Output_png/Orisinil_.png"
        pdf1 = Image.open(path_1)
        pdf2 = Image.open(path_2)
        print("\n------ Saving the Scanned Pdf -------")
        pdf1.save("./Output_Pdf/Scan_Threshold.pdf")
        pdf2.save("./Output_Pdf/Scan_Orisinil.pdf")
        self.messagebox("Citra telah di Scan dan disimpan")

    def messagebox(self,message):
        mess = QMessageBox()
        mess.setText(message)
        mess.setWindowTitle("Tahap proses Dokumen Scan")
        mess.setStandardButtons(QMessageBox.Ok)
        mess.exec_()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(475, 368)
        MainWindow.setStyleSheet("background-color: rgb(160, 151, 162)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 310, 151, 31))
        self.pushButton.setStyleSheet("font: 9pt \"Copperplate Gothic Light\";\n"
"background-color: rgb(255, 255, 127);")
        self.pushButton.setIconSize(QtCore.QSize(20, 15))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.Browser)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 461, 41))
        self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(205, 130, 222, 255), stop:0.55 rgba(235, 178, 61, 85), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 310, 121, 31))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("font: 9pt \"Copperplate Gothic Light\";\n" "background-color: rgb(255, 255, 127);")
        self.pushButton_2.setDisabled(1)
        self.pushButton_2.clicked.connect(self.Scanner)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 280, 291, 21))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(340, 270, 33, 25))
        self.label_2.setStyleSheet("font: 20pt \"Segoe UI Symbol\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(-10, 60, 491, 211))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(330, 270, 113, 31))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.raise_()
        self.lineEdit_2.setReadOnly(True)
        self.pushButton.raise_()
        self.label.raise_()
        self.pushButton_2.raise_()
        self.lineEdit.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Welcome to My Application"))
        self.pushButton.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Unggah Gambar</span></p></body></html>"))
        self.pushButton.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Unggah Gambar</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Unggah Gambar"))
        self.label.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Document Scanner Application</span></p></body></html>"))
        self.label.setWhatsThis(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffff00;\">Document Scanner Application</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600; color:#ffffff;\">Document Scanner Application</span></p></body></html>"))
        self.pushButton_2.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Scan Now</span></p></body></html>"))
        self.pushButton_2.setWhatsThis(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Scan Now</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Scan Now"))
        self.label_2.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">File</span></p></body></html>"))
        self.label_2.setWhatsThis(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">File</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#00007f;\">File</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
