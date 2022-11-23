# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget
import rc_logo_team

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1512, 960)
        MainWindow.setMinimumSize(QSize(1280, 960))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 100))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(1100, 100))
        self.label_3.setMaximumSize(QSize(1100, 100))
        self.label_3.setPixmap(QPixmap(u":/newPrefix/space-ac-png.png"))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 10000))
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setSpacing(24)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(16, 16, 16, 8)
        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(200, 700))
        self.frame_5.setMaximumSize(QSize(300, 800))
        self.frame_5.setStyleSheet(u"font: 87 12pt \"Segoe UI Black\";\n"
"color: rgb(34, 87, 126);\n"
"background-color: rgb(255, 255, 255);\n"
"\n"
"border-radius: 5px;\n"
"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_5)
        self.gridLayout_5.setSpacing(5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(8, 8, 8, 16)
        self.btn_start = QPushButton(self.frame_5)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setMinimumSize(QSize(100, 20))
        self.btn_start.setMaximumSize(QSize(150, 16777215))
        self.btn_start.setStyleSheet(u"font: 700 12pt \"Verdana\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(128, 128, 128);\n"
"border-radius: 5px;\n"
"")

        self.gridLayout_5.addWidget(self.btn_start, 6, 2, 1, 1)

        self.name_controller = QLabel(self.frame_5)
        self.name_controller.setObjectName(u"name_controller")
        self.name_controller.setMaximumSize(QSize(16777215, 100))
        self.name_controller.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.name_controller.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.name_controller, 2, 0, 1, 4)

        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 95))
        self.label_4.setMaximumSize(QSize(100, 80))
        self.label_4.setPixmap(QPixmap(u":/newPrefix/ac.png"))
        self.label_4.setScaledContents(True)

        self.gridLayout_5.addWidget(self.label_4, 0, 2, 1, 1)

        self.btn_clear = QPushButton(self.frame_5)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setMinimumSize(QSize(100, 20))
        self.btn_clear.setMaximumSize(QSize(150, 16777215))
        self.btn_clear.setStyleSheet(u"font: 700 12pt \"Verdana\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(128, 128, 128);\n"
"border-radius: 5px;\n"
"")

        self.gridLayout_5.addWidget(self.btn_clear, 7, 2, 1, 1)

        self.time = QLabel(self.frame_5)
        self.time.setObjectName(u"time")
        self.time.setMaximumSize(QSize(16777215, 100))
        self.time.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.time.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.time, 4, 0, 1, 4)

        self.elasped = QLabel(self.frame_5)
        self.elasped.setObjectName(u"elasped")
        self.elasped.setMaximumSize(QSize(16777215, 100))
        self.elasped.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.elasped.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.elasped, 3, 0, 1, 4)

        self.btn_refresh = QPushButton(self.frame_5)
        self.btn_refresh.setObjectName(u"btn_refresh")
        self.btn_refresh.setMinimumSize(QSize(100, 20))
        self.btn_refresh.setMaximumSize(QSize(150, 16777215))
        self.btn_refresh.setStyleSheet(u"font: 700 12pt \"Verdana\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(128, 128, 128);\n"
"border-radius: 5px;\n"
"")

        self.gridLayout_5.addWidget(self.btn_refresh, 7, 1, 1, 1)

        self.port_list = QComboBox(self.frame_5)
        self.port_list.setObjectName(u"port_list")
        self.port_list.setMinimumSize(QSize(100, 20))
        self.port_list.setMaximumSize(QSize(150, 16777215))
        self.port_list.setStyleSheet(u"font: 700 12pt \"Verdana\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(128, 128, 128);\n"
"border-radius: 5px;\n"
"")

        self.gridLayout_5.addWidget(self.port_list, 6, 1, 1, 1)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(130, 100))
        self.label_2.setMaximumSize(QSize(130, 80))
        self.label_2.setPixmap(QPixmap(u":/newPrefix/Suankularb_Wittayalai_School_logo.png"))
        self.label_2.setScaledContents(True)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 700))
        self.frame_6.setMaximumSize(QSize(16777215, 800))
        self.frame_6.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_6)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.c_hum_graph = PlotWidget(self.frame_6)
        self.c_hum_graph.setObjectName(u"c_hum_graph")
        self.c_hum_graph.setMinimumSize(QSize(300, 150))
        self.c_hum_graph.setMaximumSize(QSize(350, 150))
        self.c_hum_graph.setStyleSheet(u"font: 700 16pt \"Verdana\";")

        self.gridLayout_2.addWidget(self.c_hum_graph, 2, 2, 1, 1)

        self.c_alt = QLabel(self.frame_6)
        self.c_alt.setObjectName(u"c_alt")
        self.c_alt.setMinimumSize(QSize(0, 50))
        self.c_alt.setMaximumSize(QSize(16777215, 50))
        self.c_alt.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.c_alt.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.c_alt, 3, 0, 1, 1)

        self.c_alt_graph = PlotWidget(self.frame_6)
        self.c_alt_graph.setObjectName(u"c_alt_graph")
        self.c_alt_graph.setMinimumSize(QSize(300, 150))
        self.c_alt_graph.setMaximumSize(QSize(350, 200))
        self.c_alt_graph.setStyleSheet(u"font: 700 16pt \"Verdana\";")

        self.gridLayout_2.addWidget(self.c_alt_graph, 2, 0, 1, 1)

        self.c_hum = QLabel(self.frame_6)
        self.c_hum.setObjectName(u"c_hum")
        self.c_hum.setMinimumSize(QSize(0, 50))
        self.c_hum.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.c_hum.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.c_hum, 3, 2, 1, 1)

        self.c_temp_graph = PlotWidget(self.frame_6)
        self.c_temp_graph.setObjectName(u"c_temp_graph")
        self.c_temp_graph.setMinimumSize(QSize(300, 150))
        self.c_temp_graph.setMaximumSize(QSize(350, 150))
        self.c_temp_graph.setStyleSheet(u"font: 700 16pt \"Verdana\";")

        self.gridLayout_2.addWidget(self.c_temp_graph, 2, 1, 1, 1)

        self.frame_4 = QFrame(self.frame_6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 300))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pm_text = QLabel(self.frame_4)
        self.pm_text.setObjectName(u"pm_text")
        self.pm_text.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.pm_text.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.pm_text, 1, 1, 1, 1)

        self.c_press = QLabel(self.frame_4)
        self.c_press.setObjectName(u"c_press")
        self.c_press.setMinimumSize(QSize(0, 50))
        self.c_press.setMaximumSize(QSize(16777215, 50))
        self.c_press.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.c_press.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.c_press, 1, 0, 1, 1)

        self.galt_graph = PlotWidget(self.frame_4)
        self.galt_graph.setObjectName(u"galt_graph")
        self.galt_graph.setMaximumSize(QSize(350, 16777215))
        self.galt_graph.setStyleSheet(u"font: 700 16pt \"Verdana\";")

        self.gridLayout_4.addWidget(self.galt_graph, 0, 2, 1, 1)

        self.galt_text = QLabel(self.frame_4)
        self.galt_text.setObjectName(u"galt_text")
        self.galt_text.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.galt_text.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.galt_text, 1, 2, 1, 1)

        self.c_press_graph = PlotWidget(self.frame_4)
        self.c_press_graph.setObjectName(u"c_press_graph")
        self.c_press_graph.setMinimumSize(QSize(300, 150))
        self.c_press_graph.setMaximumSize(QSize(350, 150))
        self.c_press_graph.setStyleSheet(u"font: 700 16pt \"Verdana\";")

        self.gridLayout_4.addWidget(self.c_press_graph, 0, 0, 1, 1)

        self.pm_graph = PlotWidget(self.frame_4)
        self.pm_graph.setObjectName(u"pm_graph")
        self.pm_graph.setMaximumSize(QSize(350, 16777215))
        self.pm_graph.setStyleSheet(u"font: 700 16pt \"Verdana\";")

        self.gridLayout_4.addWidget(self.pm_graph, 0, 1, 1, 1)

        self.uv_graph = PlotWidget(self.frame_4)
        self.uv_graph.setObjectName(u"uv_graph")
        self.uv_graph.setStyleSheet(u"font: 700 16pt \"Verdana\";")

        self.gridLayout_4.addWidget(self.uv_graph, 0, 3, 1, 1)

        self.uv_label = QLabel(self.frame_4)
        self.uv_label.setObjectName(u"uv_label")
        self.uv_label.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.uv_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.uv_label, 1, 3, 1, 1)


        self.gridLayout_2.addWidget(self.frame_4, 4, 0, 1, 4)

        self.c_temp = QLabel(self.frame_6)
        self.c_temp.setObjectName(u"c_temp")
        self.c_temp.setMinimumSize(QSize(0, 50))
        self.c_temp.setMaximumSize(QSize(16777215, 50))
        self.c_temp.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.c_temp.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.c_temp, 3, 1, 1, 1)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_7)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.lat_text = QLabel(self.frame_7)
        self.lat_text.setObjectName(u"lat_text")
        self.lat_text.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")

        self.gridLayout_6.addWidget(self.lat_text, 0, 0, 1, 1)

        self.lng_text = QLabel(self.frame_7)
        self.lng_text.setObjectName(u"lng_text")
        self.lng_text.setStyleSheet(u"font: 700 16pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")

        self.gridLayout_6.addWidget(self.lng_text, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_7, 2, 3, 1, 1)

        self.label = QLabel(self.frame_6)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 100))
        self.label.setMaximumSize(QSize(16777215, 100))
        self.label.setStyleSheet(u"font: 700 36pt \"Verdana\";\n"
"color: rgb(0, 0, 0);")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)


        self.gridLayout.addWidget(self.frame_6, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText("")
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.name_controller.setText(QCoreApplication.translate("MainWindow", u"CONTROLLER", None))
        self.label_4.setText("")
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"CLEAR", None))
        self.time.setText(QCoreApplication.translate("MainWindow", u"TIME  :  00:00:00", None))
        self.elasped.setText(QCoreApplication.translate("MainWindow", u"ELAPSED  :  00:00:00", None))
        self.btn_refresh.setText(QCoreApplication.translate("MainWindow", u"REFRESH", None))
        self.label_2.setText("")
        self.c_alt.setText(QCoreApplication.translate("MainWindow", u"ALTITUDE : 0 m", None))
        self.c_hum.setText(QCoreApplication.translate("MainWindow", u"HUMIDITY : 0 kg^-1", None))
        self.pm_text.setText(QCoreApplication.translate("MainWindow", u"DUST : 0 \u03bcg/m\u00b3", None))
        self.c_press.setText(QCoreApplication.translate("MainWindow", u"PRESSURE : 0 m", None))
        self.galt_text.setText(QCoreApplication.translate("MainWindow", u"GPS ALTITUDE : 0 m", None))
        self.uv_label.setText(QCoreApplication.translate("MainWindow", u"UV : 0 mW/cm\u00b2", None))
        self.c_temp.setText(QCoreApplication.translate("MainWindow", u"TEMPERATURE : 0 \u00b0C", None))
        self.lat_text.setText(QCoreApplication.translate("MainWindow", u"LAT : 0", None))
        self.lng_text.setText(QCoreApplication.translate("MainWindow", u"LNG : 0", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"GROUND STATION", None))
    # retranslateUi

