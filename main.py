
from datetime import datetime
from re import S
from tracemalloc import stop

from ui_main import Ui_MainWindow
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication
from SpaceAc_tools.Port import Port
from SpaceAc_tools.Clock import RTC
from pyqtgraph import PlotWidget
from PySide6.QtCore import QThread,Signal
# from lib import Log
# import lib as ilib
import threading
import time
import mqtt
import sys
import os
import numpy as np
import pyqtgraph as pg
import random


data_dict = {
    "C": [
        "PKG", "ALT", "TMP", "PRESS", "HUM","GLAT", "GLNG", "GAL", "DUST", "UV" ,

    ],
    'T': [
        "ID", "CLO", "PKG", "TYP", "ALT", "TMP",
        "BAT", "GYR", "GYP", "GYY", "ACR", "ACP",
        "ACY", "MGR", "MGP", "MGY", "P_ERROR", "STATE",
    ],
}


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.clearUi()

    def clearUi(self):

        self.ui.c_alt.setText("-00.00-")
        self.ui.c_temp.setText("-00.00-")
        self.ui.c_press.setText("-00.00-")
        self.ui.c_hum.setText("-00.00-")
        self.ui.uv_label.setText("-00.00-")
        self.ui.pm_text.setText("-00.00-")
        self.ui.galt_text.setText("-00.00-")
       


class SerialThread(QThread):
    global data_dict
    carrier1 = Signal(object)
    carrier2 = Signal(object)

    def __init__(self, com, parent=None):
        super(SerialThread, self).__init__(parent)
        self.dict = data_dict
        self.port = Port(com=com, baudrate=9600, end='\r',
                         file_name="Flight_Suankularb", file_name2="Flight_Suankularb_reserve", key=self.dict)
        self.port.connect()
        self.port.gearthlive()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.pkg = self.port.reading()
            print(f'hey this is pkg : {self.pkg}')
            if(self.pkg is None):
                continue
            if isinstance(self.pkg, dict):
                try:
                    if 1== 1:
                        print(f"[DATA]   {self.pkg}")
                        self.pkg1 = self.pkg
                        self.carrier1.emit(self.pkg)
                        print(type(self.pkg1['GAL']))
                        if self.pkg1['GLNG'] != ''or 0:
                            coord = f"{self.pkg1['GLNG']},{self.pkg1['GLAT']},{self.pkg1['ALT']}  "
                            self.port.gearthcoord(coord)


                    elif self.pkg['TYP'] == 'T':
                        # print(f"[TETHERDPAYLOAD]   {self.pkg}")
                        self.pkg2 = self.pkg
                        self.carrier2.emit(self.pkg)

                except Exception:
                    print('Index Error 123')
                    return

    def stop(self):
        self._isRunning = False


class TimerThread(QThread):

    carrier1 = Signal(object)
    carrier2 = Signal(object)

    def __init__(self, parent=None):
        super(TimerThread, self).__init__(parent)
        self.clock = RTC()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.carrier1.emit(self.clock.time_pc())
            self.carrier2.emit(self.clock.time_elapsed())
            time.sleep(0.001)

    def stop(self):
        self._isRunning = False


class Controller:
    global data_dict

    def __init__(self):
        self.ui_main = MainWindow()
        self.dict = data_dict
        self.serial_state = False
        # self.logger = Log(target='GUI_STACK')
        self.header = None
        self.cansat = {v: [] for v in self.dict['C']}
        # self.rocket = {v: [] for v in self.dict['T']}
    

        self.all_state_cansat = [
            'PRELAUNCH', 'LAUNCH', 'ROCKET_SEPARATION',
            'DESCENT', 'TP_RELEASE', 'LANDED',
        ]
       

        self.list_cansat_append = [
            'PKG', 'ALT', 'TMP', 'PRESS', 'HUM','GLAT' , 'GLNG' , 'GAL', 'DUST',  'UV',
        ]
        self.list_cansat_type = [
            int, float, float, float, float, float , float , float, float, float
        ]
        


        self.ui_main.ui.btn_clear.clicked.connect(self.clear)
        self.ui_main.ui.btn_refresh.clicked.connect(self.refresh)
        self.ui_main.ui.btn_start.clicked.connect(
            self.startSerial)
        # self.ui_main.ui.cmd_list.currentTextChanged.connect(
        #     lambda x: self.cmdselect(x))
        self.setDefaultLabel()
        self.ui_main.show()
        self.refresh()

    def setDefaultLabel(self):
        self.ui_main.ui.c_alt_graph.setLabel(
            'left', 'Metres(m)', **{'color': '#100720', 'front-size': '8 pt '})
        self.ui_main.ui.c_temp_graph.setLabel(
            'left', 'Celcius(°C)', **{'color': '#100720', 'front-size': '8 pt '})
        self.ui_main.ui.c_press_graph.setLabel(
            'left', 'Metres(m)', **{'color': '#100720', 'front-size': '8 pt '})
        self.ui_main.ui.c_hum_graph.setLabel(
            'left', 'Kilogramm(kg^-1)', **{'color': '#100720', 'front-size': '8 pt '})
        self.ui_main.ui.galt_graph.setLabel(
            'left', 'Metres(m)', **{'color': '#100720', 'front-size': '8 pt '})
        self.ui_main.ui.pm_graph.setLabel(
            'left', 'μg/m³', **{'color': '#100720', 'front-size': '8 pt '})
        self.ui_main.ui.uv_graph.setLabel(
            'left', 'mW/cm²', **{'color': '#100720', 'front-size': '8 pt '})
      
     

    def clear(self):
        self.cansat = {v: [] for v in self.dict['C']}

        self.ui_main.ui.c_alt_graph.clear()
        self.ui_main.ui.c_temp_graph.clear()
        self.ui_main.ui.c_press_graph.clear()
        self.ui_main.ui.c_hum_graph.clear()
 

    def startThread(self, com: str):
        print('Starting and connecting')
        self.clock = TimerThread()
        self.clock.carrier1.connect(self.updateClock)
        self.clock.carrier2.connect(self.updateElapsed)

        self.serial = SerialThread(com)
        self.serial.carrier1.connect(self.updateCanSat)
        self.serial.start()
        self.clock.start()

    def updateClock(self, time):
        self.ui_main.ui.time.setText(time)

    def updateElapsed(self, time):
        self.ui_main.ui.elasped.setText(time)

    def updateCanSat(self, data: dict):
        print('Updating CanSat')

        self.ui_main.ui.c_hum.setText(f'HUMIDITY : {data["HUM"]}kg^-1')
        self.ui_main.ui.c_alt.setText(f'ALTITUDE : {data["ALT"]}m')
        self.ui_main.ui.c_temp.setText(f'TEMPERATURE: {data["TMP"]}°C')
        self.ui_main.ui.c_press.setText(f'PRESSURE: {data["PRESS"]}m')
        self.ui_main.ui.pm_text.setText(f'DUST: {data["DUST"]}μg/m³')
        self.ui_main.ui.galt_text.setText(f'GAL: {data["GAL"]}m')
        self.ui_main.ui.lat_text.setText(f'LAT: {data["GLAT"]}°')
        self.ui_main.ui.lng_text.setText(f'LNG: {data["GLNG"]}°')
        self.ui_main.ui.uv_label.setText(f'UV: {data["UV"]}mW/cm²')
       

        for dat, typ in zip(self.list_cansat_append, self.list_cansat_type):
            if not data[dat]:
                self.cansat[dat].append(0)

                continue
            try:
                self.cansat[dat].append(typ(data[dat]))
            except Exception as e:
                self.cansat[dat].append(data[dat])


      

        self.plot(self.ui_main.ui.c_alt_graph,
                  self.cansat["PKG"], self.cansat["ALT"], '', '')
        self.plot(self.ui_main.ui.c_temp_graph,
                  self.cansat["PKG"], self.cansat["TMP"], '', '')
        self.plot(self.ui_main.ui.c_hum_graph,
                  self.cansat["PKG"], self.cansat["HUM"], '', '')
        self.plot(self.ui_main.ui.c_press_graph,
                  self.cansat["PKG"], self.cansat["PRESS"], '', '')
        self.plot(self.ui_main.ui.galt_graph,
                  self.cansat["PKG"], self.cansat["GAL"], '', '')
        self.plot(self.ui_main.ui.pm_graph,
                  self.cansat["PKG"], self.cansat["DUST"], '', '')
        self.plot(self.ui_main.ui.uv_graph,
                  self.cansat["PKG"], self.cansat["UV"], '', '')
        
        

  

    def refresh(self):
        self.serial_state = False
        self.ui_main.ui.port_list.clear()
        for port in Port.list_port():
            self.ui_main.ui.port_list.addItem(port)

    def startSerial(self):
        if len(self.ui_main.ui.port_list.currentText()) == 0:
            print('No Serial device found! Try .connect to start device')
            return
        elif not self.serial_state:
            self.port = self.ui_main.ui.port_list.currentText()
            self.baudrate = 9600
            self.serial_state = True
            Window.startThread(self.port)


    def plot(self, graph: PlotWidget, pkg, x, y=None, z=None):
        graph.clear()
        size_x = min(len(pkg), len(x))if len(x) < 50 else 50
        # if isinstance(x,str):
        #     return

        if not y and not z:
            graph.plot(**{'x': pkg[-size_x:-1], 'y': x[-size_x:-1], 'symbol': 'o',
                       'symbolSize': 6, 'symbolPen': 'r', 'pen': 'r'})
        else:
            size_y = min(len(pkg), len(y))if len(y) < 50 else 50
            size_z = min(len(pkg), len(z)) if len(z) < 50 else 50
            graph.plot(**{'x': pkg[-size_x:-1], 'y': x[-size_x:-1],
                          'symbol': 'o', 'symbolSize': 6, 'symbolPen': 'c', 'pen': 'c'})
            graph.plot(**{'x': pkg[-size_y:-1], 'y': y[-size_y:-1],
                          'symbol': 'o', 'symbolSize': 6, 'symbolPen': 'y', 'pen': 'y'})
            graph.plot(**{'x': pkg[-size_z:-1], 'y': z[-size_z:-1],
                          'symbol': 'o', 'symbolSize': 6, 'symbolPen': 'k', 'pen': 'k'})


    def stop(self):
        self._isRunning = False


if __name__ == "__main__":
    # log = Log(target='GUI_PROG')
    # log.info('Start of Program')
    pg.setConfigOption('background', (255, 255, 255, 0))
    pg.setConfigOption('foreground', (255, 255, 255, 255))
    app = QApplication(sys.argv)
    Window = Controller()
    sys.exit(app.exec())
