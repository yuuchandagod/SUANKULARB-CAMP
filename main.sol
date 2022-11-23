from datetime import datetime
from logging import exception
from re import S
from tkinter import ON
from tracemalloc import stop

from sklearn.utils import check_X_y
from ui_main import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from SpaceAc_tools.Port import Port
from SpaceAc_tools.Clock import RTC
from SpaceAc_tools.GNSS import GNSS
from pyqtgraph import PlotWidget
from PyQt5.QtCore import QThread
import threading
import serial
import cmd
import time
import mqtt
import sys
import os
import numpy as np
import pyqtgraph as pg
import random


data_dict = {
    "C": [
        "ID", "CLO", "PKG", "TYP", "MODE", "TP_R",
        "ALT", "TMP", "BAT", "GPS_TIME", "GLAT",
        "GLNG", "GAL", "SATS", "STATE", "C_ECHO",
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
        self.ui.c_pkg.setText("-00.00-")
        self.ui.tp_pkg.setText("-00.00-")
        self.ui.mode.setText("NONE")
        self.ui.c_bat.setText("-00.00-")
        self.ui.c_alt.setText("-00.00-")
        self.ui.tp_alt.setText("-00.00-")
        self.ui.c_temp.setText("-00.00-")
        self.ui.tp_temp.setText("-00.00-")
        self.ui.c_galt.setText("-00.00-")
        self.ui.c_glat.setText("-00.00-")
        self.ui.c_glng.setText("-00.00-")

        self.ui.c_state.setProperty('value', 0)
        self.ui.tp_state.setProperty('value', 0)
        self.ui.tp_r.setProperty('value', 0)


class SerialThread(QThread):
    global data_dict
    carrier1 = QtCore.pyqtSignal(object)
    carrier2 = QtCore.pyqtSignal(object)

    def __init__(self, com, parent=None):
        super(SerialThread, self).__init__(parent)

        self.dict = data_dict
        self.port = Port(com=com, baudrate=9600, end='\r',
                         file_name="Project", key=self.dict)
        self.port.connect()
        self.port.gearthlive()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.pkg = self.port.reading()
            if(self.pkg is None):
                continue
            # print(f'got: {self.pkg}')
            if isinstance(self.pkg, dict):
                try:
                    if self.pkg['TYP'] == 'C':
                        print(f"[CONTAINER]   {self.pkg}")
                        self.pkg1 = self.pkg
                        self.carrier1.emit(self.pkg)
                        coord = f"{self.pkg1['GLAT']},{self.pkg1['GLNG']}"
                        self.port.gearthcoord(coord)

                    elif self.pkg['TYP'] == 'T':
                        print(f"[T]   {self.pkg}")
                        self.pkg2 = self.pkg
                        self.carrier2.emit(self.pkg)

                except Exception:
                    print('Index Error')
                    return

    def stop(self):
        self._isRunning = False


class TimerThread(QThread):
    carrier1 = QtCore.pyqtSignal(object)
    carrier2 = QtCore.pyqtSignal(object)

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

    def __init__(self, com: str):
        self.ui_main = MainWindow()
        self.s_thread = SerialThread(com)
        self.send_mqtt = False
        self.dict = data_dict
        self.serial_state = False

        self.all_state_cansat = [
            'PRELAUNCH', 'LAUNCH', 'ROCKET_SEPARATION',
            'DESCENT', 'TP_RELEASE', 'LANDED',
        ]
        self.all_state_payload = [
            'STANDBY', 'RELEASED', 'ACQUIRING_TARGET',
            'TARGET_POINTING',
        ]

        self.list_cansat_append = [
            'PKG', 'CLO', 'ALT', 'GAL', 'TMP', 'BAT',
            'STATE', 'C_ECHO', 'SATS',
        ]
        self.list_cansat_type = [
            int, str, float, float, float, float,
            str, str, float,
        ]
        self.list_payload_append = [
            'PKG', 'ALT', 'TMP', 'ACR', 'ACP', 'ACY',
            'GYR', 'GYP', 'GYY', 'MGR', 'MGP', 'MGY',
        ]

        self.ui_main.ui.cmd_send.clicked.connect(self.sendcmd)
        self.ui_main.ui.btn_clear.clicked.connect(self.clear)
        self.ui_main.ui.btn_refresh.clicked.connect(self.refresh)
        self.ui_main.ui.btn_start.clicked.connect(
            self.startSerial), (self.update_cmdecho)
        self.ui_main.ui.cmd_list.currentTextChanged.connect(
            lambda x: self.cmdselect(x))
        self.ui_main.ui.mqtt_on.clicked.connect(self.mqttOn)
        self.ui_main.ui.mqtt_off.clicked.connect(self.mqttOff)
        self.setDefaultLabel()
        self.ui_main.show()
        self.refresh()

    def setDefaultLabel(self):
        self.ui_main.ui.c_alt_graph.setLabel(
            'left', 'Metres(m)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.c_temp_graph.setLabel(
            'left', 'Celcius(°C)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.c_galt_graph.setLabel(
            'left', 'Metres(m)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.tp_alt_graph.setLabel(
            'left', 'Metres(m)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.tp_temp_graph.setLabel(
            'left', 'Celcius(°C)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.tp_point_graph.setLabel(
            'left', 'Degree(°)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.mag_graph.setLabel(
            'left', 'Microteslas(μT)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.gyro_graph.setLabel(
            'left', 'Degree/Seconds²(deg/sec²)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.ui_main.ui.ac_graph.setLabel(
            'left', 'Metres/Seconds²(m/s²)', **{'color': '#EEF3D2', 'front-size': '8 pt '})
        self.clear()

    def clear(self):
        self.cansat = {v: [] for v in self.dict['C']}
        self.rocket = {v: [] for v in self.dict['T']}

        self.ui_main.ui.c_alt_graph.clear()
        self.ui_main.ui.c_temp_graph.clear()
        self.ui_main.ui.c_galt_graph.clear()

    def startThread(self, com: str):
        print('Starting and connecting')
        self.clock = TimerThread()
        self.clock.carrier1.connect(self.updateClock)
        self.clock.carrier2.connect(self.updateElapsed)

        self.serial = SerialThread(com)
        self.serial.carrier1.connect(self.updateCanSat)
        self.serial.carrier2.connect(self.updatePayload)

        try:
            self.serial.terminate()
        except Exception:
            pass

        self.serial.start()

        try:
            self.clock.terminate()
        except Exception:
            pass

        self.clock.start()

    def updateClock(self, time):
        self.ui_main.ui.time.setText(time)

    def updateElapsed(self, time):
        self.ui_main.ui.elasped.setText(time)

    def updateCanSat(self, data: dict):
        print('Updating CanSat')

        data['CLO'] = RTC.time_pc()
        data['TP_R'] = 0
        print("[UPDATE_CONTAINER]", end=" ")

        self.ui_main.ui.time.setText(data['CLO'])
        self.ui_main.ui.c_pkg.setText(f'Packet Count: {data["PKG"].zfill(3)}')
        self.ui_main.ui.c_alt.setText(f'Altitude: {data["ALT"]}m')
        self.ui_main.ui.c_temp.setText(f'Temperature: {data["TMP"]}c')
        self.ui_main.ui.c_glat.setText(f'Latitude: {data["GLAT"]}m')
        self.ui_main.ui.c_glng.setText(f'Longtitude: {data["GLNG"]}m')
        self.ui_main.ui.c_galt.setText(f'GPS Altitude: {data["GAL"]}m')
        self.ui_main.ui.c_bat.setText(f'Voltage: {data["BAT"]}v')
        self.ui_main.ui.cmd_echo.setText(f'COMMAND ECHO: {data["C_ECHO"]}')
        self.ui_main.ui.mode.setText(f'Mode: {data["MODE"]}')
        self.ui_main.ui.c_alt_graph.setLabel('bottom', 'packet count')

        for dat, typ in zip(self.list_cansat_append, self.list_cansat_type):
            if data[dat]:
                self.cansat[dat].append(typ(data[dat]))
            else:
                self.cansat[dat].append(data[dat][-1])

        temp_state = data['STATE']

        if temp_state in self.all_state_cansat:
            self.ui_main.ui.c_state.setProperty(
                'value', self.all_state_cansat.index(temp_state))

        self.ui_main.ui.tp_r.setProperty('value', int(data['TP_R'] == "R"))

        # Convert every value in 'data' to string (some of them later modified to int)
        data_str_packed = ','.join([str(v) for v in data.values()])

        if self.send_mqtt:
            print('SENT:', data_str_packed)
            mqtt.sendserver(self.MQTT, data_str_packed)

        self.plot(self.ui_main.ui.c_alt_graph,
                  self.cansat["PKG"], self.cansat["ALT"])
        self.plot(self.ui_main.ui.c_temp_graph,
                  self.cansat["PKG"], self.cansat["TMP"])
        self.plot(self.ui_main.ui.c_galt_graph,
                  self.cansat["PKG"], self.cansat["GAL"])

    def updatePayload(self, data: dict):
        self.ui_main.ui.tp_pkg.setText(f'Packet count: {data["PKG"].zfill(3)}')
        self.ui_main.ui.tp_alt.setText(f'Altitude: {data["ALT"]}m')
        self.ui_main.ui.tp_temp.setText(f'Temperature: {data["TMP"]}c')
        self.ui_main.ui.tp_v.setText(f'Voltage: {data["BAT"]}v')
        self.ui_main.ui.tp_acr.setText(f'ACCR: {data["ACR"]}m/s²')
        self.ui_main.ui.tp_acp.setText(f'ACCP: {data["ACP"]}m/s²')
        self.ui_main.ui.tp_acy.setText(f'ACCY: {data["ACY"]}m/s²')
        self.ui_main.ui.tp_gyr.setText(f'GYRR: {data["GYR"]}deg/s²')
        self.ui_main.ui.tp_gyp.setText(f'GYRP: {data["GYP"]}deg/s²')
        self.ui_main.ui.tp_gyy.setText(f'GYRY: {data["GYY"]}deg/s²')
        self.ui_main.ui.tp_mgr.setText(f'MGR: {data["MGR"]}μT')
        self.ui_main.ui.tp_mgp.setText(f'MGP:{data["MGP"]}μT')
        self.ui_main.ui.tp_mgy.setText(f'MGY:{data["MGY"]}μT')
        self.ui_main.ui.tp_error.setText(f'Pointing error: {data["P_ERROR"]}°')

        if data['PKG']:
            self.rocket["PKG"].append(int(data['PKG']))
        else:
            self.rocket["PKG"].append(self.rocket["PKG"][-1])
        for dat in self.list_payload_append:
            if data[dat]:
                self.rocket[dat].append(float(data[dat]))
            else:
                self.rocket[dat].append(self.rocket[dat][-1])

        temp_state = data['STATE']
        if temp_state in self.all_state_payload:
            self.ui_main.ui.tp_state.setProperty(
                'value', self.all_state_payload.index(temp_state))

        # Convert every value in 'data' to string (some of them later modified to int)
        data_str_packed = ','.join([str(v) for v in data.values()])

        if self.send_mqtt:
            print('SENT:', data_str_packed)
            mqtt.sendserver(self.MQTT, data_str_packed)

        self.plot(self.ui_main.ui.tp_alt_graph,
                  self.rocket["PKG"], self.rocket["ALT"])
        self.plot(self.ui_main.ui.tp_temp_graph,
                  self.rocket["PKG"], self.rocket["TMP"])
        self.plot(self.ui_main.ui.tp_point_graph,
                  self.rocket["PKG"], self.rocket["P_ERROR"])
        self.plot(self.ui_main.ui.mag_graph,
                  self.rocket["PKG"], self.rocket["MGR"])
        self.plot(self.ui_main.ui.mag_graph,
                  self.rocket["PKG"], self.rocket["MGP"])

        self.plot(self.ui_main.ui.gyro_graph,
                  self.rocket["PKG"], self.rocket["GYR"] + self.rocket["GYP"] + self.rocket["GYY"])
        self.plot(self.ui_main.ui.ac_graph,
                  self.rocket["PKG"], self.rocket["ACR"] + self.rocket["ACP"] + self.rocket["ACY"])

    def refresh(self):
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

    def cmdselect(self, command: str):
        pres = random.uniform(50, 100)

        if command == 'CX ON':
            self.cmdtype = 'CX'
            self.cmd = 'ON'
            self.s_thread.port.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
            print(f"CMD,1072,{self.cmdtype},{self.cmd}$")
        elif command == 'CX OFF':
            self.cmdtype = 'CX'
            self.cmd = 'OFF'
            self.s_thread.port.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
            print(f"CMD,1072,{self.cmdtype},{self.cmd}$")
        elif command == 'ST':
            self.cmdtype = 'ST'
            # self.cmd = ':'.join(RTC.time_UTC()).split(':')[:-1]
            self.cmd = datetime.utcnow().strftime('%H:%M:%S')
            self.s_thread.port.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
            print(f"CMD,1072,{self.cmdtype},{self.cmd}$")
        elif command == 'SIM ACTIVATE':
            self.cmdtype = 'SIM'
            self.cmd = 'ACTIVATE'
            print(f"CMD,1072,{self.cmdtype},{self.cmd}$")
            self.ui_main.ui.cmd_sim.setText(f"SIM : {self.cmd} ")
            self.s_thread.port.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
        elif command == 'SIM ENABLE':
            self.cmdtype = 'SIM'
            self.cmd = 'ENABLE'
            self.s_thread.port.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
            self.ui_main.ui.cmd_sim.setText(f"SIM : {self.cmd} ")
            print(f"CMD,1072,{self.cmdtype},{self.cmd}$")
        elif command == 'SIM DISABLE':
            self.cmdtype = 'SIM'
            self.cmd = 'DISABLE'
            self.s_thread.port.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
            self.ui_main.ui.cmd_sim.setText(f"SIM : {self.cmd} ")
            print(f"CMD,1072,{self.cmdtype},{self.cmd}$")
        elif command == 'SIMP':
            self.cmdtype = 'SIMP'
            self.cmd = pres
            self.s_thread.port.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
            print(f"CMD,1072,{self.cmdtype},{self.cmd}$")

            # self.simpfunction = threading.Thread(target=self.simp)
            # self.simpfunction.start()
            # # self.device.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")

    def simp(self):
        with open("filename", "r") as file:
            simdata = file.readlines()
        for i, data in enumerate(simdata):
            simdata[i] = data.replace("$", "1072")
        for i in simdata:
            self.device.write(i)
            time.sleep(1)

    def sendcmd(self):
        self.device.write(f"CMD,1072,{self.cmdtype},{self.cmd}$")
        print(f"CMD,1072,{self.cmdtype},{self.cmd}$")

    def update_cmdecho(self):
        self.ui_main.ui.cmd_echo.setText(
            self.ui_main.ui.cmd_list.currentText())

    def sim(self):
        file = 'Cansat_2022_sim_file_B.txt'
        self.ui_main.ui.sim_file.setText(file)
        print(f"simulating : {file}")
        if os.path.exists(f"SIM/{file}"):
            with open(f'SIM/{file}', 'r') as f:
                simdata = f.readlines()
            for data in simdata:
                x = data.find("C_ECHO")
                if x == 0:
                    data = data.replace('$', '1072')
                    data = data.replace('\n', '')
                    self.device.write((data + "$").encode())
                    time.sleep(0.99)
                    print(data + "$")
        else:
            print("ERROR NO FILE!")

    def connectSerial(self):
        self.A = self.ui_main.ui.port_list.currentText()
        try:
            self.device = serial.Serial(self.A, baudrate=9600, timeout=60)
        except Exception:
            print("[Cannot connect port]")

        self.refresh()

    def plot(self, graph: PlotWidget, pkg, data):
        print('plotting')
        graph.clear()
        size_min = min(len(pkg), len(data))

        if size_min > 50:
            graph.plot(pkg[-50:-1], data[-50:-1])
        else:
            graph.plot(pkg[-size_min:], data[-size_min:])

    def mqttOn(self):
        try:
            self.MQTT = mqtt.initClient("1072", "Cyygkiqi171")
            self.send_mqtt = True
            print('Client connected!')
        except TimeoutError:
            self.send_mqtt = False
            print("***************[MQTT ERROR]***************")

    def mqttOff(self):
        try:
            mqtt.disconnectClient(self.MQTT)
            self.send_mqtt = False
            print('Client disconnected!')
        except Exception:
            pass


if __name__ == "__main__":
    pg.setConfigOption('background', (255, 255, 255, 0))
    pg.setConfigOption('foreground', (255, 255, 255, 255))
    app = QApplication(sys.argv)
    Window = Controller(com=str)
    sys.exit(app.exec())
