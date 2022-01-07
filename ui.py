from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from torchvision.models import resnet18
from torch.nn import Softmax, Linear
from torch import load as torch_load
from PIL import Image
from numpy import argmax
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtChart
from PyQt5.QtChart import QChart, QPieSeries

resnet18 = resnet18(pretrained=True)
resnet18.fc = Linear(in_features=512, out_features=3)
resnet18.load_state_dict(torch_load('model.pt'))
resnet18.eval()


class Result(object):
        def __init__(self, text, color) -> None:
                super().__init__()
                self.color = color
                self.text = text

class Ui_MainWindow(object):

        def __init__(self) -> None:
                super().__init__()
                self.p1 = 0
                self.p2 = 0
                self.p3 = 0
                self.unknownResult = Result("Unknown", "gray")
                self.normalResult = Result("Normal", "green")
                self.viralResult = Result("Viral", "orange")
                self.covidResult = Result("Covid", "red")

        def process_image(self):
                try:
                        image_transform = Compose([
                        Resize(size=(224, 224)),
                        ToTensor(),
                        Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                        ])
                        image = Image.open(self.file_name).convert('RGB')
                        image = image_transform(image)
                        image = image.unsqueeze(0)
                        output = resnet18(image)[0]
                        probabilities = Softmax(dim=0)(output)
                        probabilities = probabilities.cpu().detach().numpy()
                        self.p1 = probabilities[0] * 100
                        self.p2 = probabilities[1] * 100
                        self.p3 = probabilities[2] * 100
                except:
                        self.clearViewAction()

        def OpenFileAction(self):
                self.file_name, _ = QFileDialog.getOpenFileName(
                        None, 
                        "Select Png Image", 
                        "", 
                        "Png Files (*.png)")
                if not self.file_name:
                        self.clearViewAction()
                        return
                self.process_image()
                self.setResultToChart(self.getMax())
                self.update_chart()
                self.setCharttoView()

        def getMax(self):
                if self.p1 > self.p2 \
                        and self.p1 > self.p3:
                        return self.normalResult
                elif self.p2 > self.p3:
                        return self.viralResult
                else:
                        return self.covidResult

        def update_chart(self):
                self.pieChart = QPieSeries()
                self.pieChart.append("Normal", self.p1)
                self.pieChart.append("Viral", self.p2)
                self.pieChart.append("Covid", self.p3)

                self.pieChart.slices()[0].setBrush(QColor("green"))
                self.pieChart.slices()[1].setBrush(QColor("blue"))
                self.pieChart.slices()[2].setBrush(QColor("red"))
                self.pieChart.setLabelsVisible(True)
                self.pieChart.setLabelsPosition(
                QtChart.QPieSlice.LabelOutside
                )

        def setCharttoView(self):
                mainChart = QChart()
                mainChart.legend()
                mainChart.addSeries(self.pieChart)
                mainChart.createDefaultAxes()
                mainChart.setAnimationOptions(QChart.SeriesAnimations)
                mainChart.legend().setVisible(True)
                mainChart.legend().setAlignment(Qt.AlignBottom)
                self.chartView.setRenderHint(QPainter.Antialiasing)
                self.chartView.setChart(mainChart)

        def clearViewAction(self):
                self.pieChart = QPieSeries()
                self.pieChart.append("Unknown", 1)
                self.pieChart.setLabelsVisible(True)
                self.setResultToChart(self.unknownResult)
                self.pieChart.setLabelsPosition(QtChart.QPieSlice.LabelOutside)
                self.setCharttoView()

        def setResultToChart(self, obj):
                _translate = QtCore.QCoreApplication.translate
                self.resultLabel.setText(_translate("MainWindow", """
                <html>
                <head/>
                <body>
                        <p align=\"center\">
                                <span style=\" font-size:16pt; 
                                color:""" + obj.color + """;\">
                                [ """+ obj.text +""" ]
                                </span>
                        </p>
                </body>
                </html>"""))

        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(762, 555)
                MainWindow.setMinimumSize(QtCore.QSize(762, 555))
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setMinimumSize(QtCore.QSize(762, 555))
                self.centralwidget.setObjectName("centralwidget")
                self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
                self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
                self.horizontalLayout.setSpacing(0)
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.lFrame = QtWidgets.QFrame(self.centralwidget)
                self.lFrame.setStyleSheet("""
                background-color: rgb(0, 0, 255);
                color: rgb(246, 245, 244);""")
                self.lFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.lFrame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.lFrame.setObjectName("lFrame")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.lFrame)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.Title = QtWidgets.QLabel(self.lFrame)
                self.Title.setObjectName("Title")
                self.verticalLayout_2.addWidget(self.Title)
                self.classes = QtWidgets.QLabel(self.lFrame)
                self.classes.setObjectName("classes")
                self.verticalLayout_2.addWidget(self.classes)
                self.version = QtWidgets.QLabel(self.lFrame)
                self.version.setObjectName("version")
                self.verticalLayout_2.addWidget(self.version)
                self.horizontalLayout.addWidget(self.lFrame)
                self.rFrame = QtWidgets.QFrame(self.centralwidget)
                self.rFrame.setStyleSheet("background-color: white;")
                self.rFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.rFrame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.rFrame.setObjectName("rFrame")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.rFrame)
                self.verticalLayout.setObjectName("verticalLayout")
                self.resultLabel = QtWidgets.QLabel(self.rFrame)
                self.resultLabel.setMinimumSize(QtCore.QSize(361, 31))
                self.resultLabel.setObjectName("resultLabel")
                self.verticalLayout.addWidget(self.resultLabel)
                self.chartView = QtChart.QChartView(self.rFrame)
                self.chartView.setMinimumSize(QtCore.QSize(368, 411))
                self.chartView.setObjectName("chartView")
                self.verticalLayout.addWidget(self.chartView)
                self.frame_3 = QtWidgets.QFrame(self.rFrame)
                self.frame_3.setMinimumSize(QtCore.QSize(371, 51))
                self.frame_3.setStyleSheet("border: 0;")
                self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_3.setObjectName("frame_3")
                self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.openImageButton = QtWidgets.QPushButton(self.frame_3)
                self.openImageButton.setMinimumSize(QtCore.QSize(101, 31))
                self.openImageButton.setStyleSheet("""
                color: rgb(239, 239, 239);
                background-color: rgb(0, 0, 255);
                border-radius: 12px;""")
                self.openImageButton.setObjectName("openImageButton")
                self.horizontalLayout_2.addWidget(self.openImageButton)
                self.clearViewButton = QtWidgets.QPushButton(self.frame_3)
                self.clearViewButton.setMinimumSize(QtCore.QSize(101, 31))
                self.clearViewButton.setStyleSheet("""
                color: rgb(239, 239, 239);
                background-color: rgb(0, 0, 255);
                border-radius: 12px;""")
                self.clearViewButton.setObjectName("clearViewButton")
                self.horizontalLayout_2.addWidget(self.clearViewButton)
                self.exitButton = QtWidgets.QPushButton(self.frame_3)
                self.exitButton.setMinimumSize(QtCore.QSize(101, 31))
                self.exitButton.setStyleSheet("""
                color: rgb(239, 239, 239);
                background-color: rgb(0, 0, 255);
                border-radius: 12px;""")
                self.exitButton.setObjectName("exitButton")
                self.horizontalLayout_2.addWidget(self.exitButton)
                self.verticalLayout.addWidget(self.frame_3)
                self.horizontalLayout.addWidget(self.rFrame)
                self.horizontalLayout.setStretch(0, 4)
                self.horizontalLayout.setStretch(1, 6)
                MainWindow.setCentralWidget(self.centralwidget)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)
                self.clearViewAction()

                self.exitButton.clicked.connect(MainWindow.close)
                self.clearViewButton.clicked.connect(self.clearViewAction)
                self.openImageButton.clicked.connect(self.OpenFileAction)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                self.Title.setText(_translate("MainWindow", """
                <html>
                <head/>
                <body>
                        <p align=\"center\"><span style=\" font-size:16pt;\">
                                Lung Anomaly Detector
                                </span>
                        </p>
                        <p align=\"center\"><span style=\" font-size:14pt;\">
                                [Algotithm - ResNet18]
                                </span>
                        </p>
                </body>
                </html>"""))
                self.classes.setText(_translate("MainWindow", """
                <html>
                <head/>
                <body>
                        <p align=\"center\"><span style=\" font-size:14pt;\">
                                [Available Classes]
                                </span>
                        </p>
                        <p align=\"center\"><span style=\" font-size:12pt; 
                                font-style:italic; 
                                color:#00ff18;\">
                                (normal)
                                </span>
                        </p>
                        <p align=\"center\">
                        <span style=\" font-size:12pt; 
                                font-style:italic; 
                                color:#ff5800;\">
                                (viral)
                        </span>
                        </p>
                        <p align=\"center\">
                        <span style=\" font-size:12pt; 
                                font-style:italic; 
                                color:#ff0000;\">
                                        (covid)
                        </span>
                        </p>
                </body>
                </html>"""))
                self.version.setText(_translate("MainWindow", """
                <html>
                <head/>
                <body>
                        <p align=\"center\">
                                v1.0
                        </p>
                </body>
                </html>"""))
                self.resultLabel.setText(_translate("MainWindow", """
                <html>
                <head/>
                <body>
                        <p align=\"center\">
                        <span style=\" font-size:14pt; color:#5e5c64;\">
                                [ Unknown ]
                        </span>
                </p>
                </body>
                </html>"""))
                self.openImageButton.setText(_translate("MainWindow", "Open CXR Image"))
                self.clearViewButton.setText(_translate("MainWindow", "Clear View"))
                self.exitButton.setText(_translate("MainWindow", "Exit Application"))

if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec())
