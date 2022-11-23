try:
    from _global import *
except:
    from ._global import *
from distutils.log import ERROR
from email.errors import FirstHeaderLineIsContinuationDefect
from re import L
import string
import glob

from matplotlib.pyplot import connect


class Port:
    def __init__(self, com: str, end: str, start=None, baudrate=9600, file_name='', file_name2='', earth_name='Location', key: dict = None):
        self.com = com
        self.baudrate = baudrate
        self.end = end
        self.key = key
        self.start = start
        self.device = None
        self.pathC = self.path(file_name)
        self.pathT = self.path2(file_name2)
        self.coord = ""
        self.googlename = self.earthpath(earth_name)

    @staticmethod
    def list_port():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def write(self, text: str):
        if self.device is not None:
            self.device.write(text.encode('utf-8'))
        else:
            print(f"Cannot write to {self.device}")

    def connect(self):
        try:
            self.device = serial.Serial(
                self.com, baudrate=self.baudrate, timeout=60)
            print(self.device)
        except:
            print(f"Cannot connect to {self.device}")

    def read(self):
        try:
            inp = self.device.read().decode('utf-8')
        except UnicodeDecodeError as e:
            print(f'Error decoding input from serial: {e}')
            return
        pkg = ''
        while inp != self.end:
            # print(inp, end='')
            if self.start is not None and inp == self.start:
                pkg = ''
            if inp in string.printable:
                pkg += inp
            try:
                inp = self.device.read().decode('utf-8')
            except Exception:
                print('Error decoding')
                return
        pkg = pkg.replace('\r', '').replace('\n', '')
        return pkg

    @staticmethod
    def path(file_name):
        if not os.path.exists('Data_log'):
            os.mkdir('Data_log')
        clock = datetime.now().time()
        index = "_".join(list((date.today().strftime("%b-%d-%Y"),
                         str(clock.hour).zfill(2), str(clock.minute).zfill(2))))
        return os.path.join(os.path.abspath(os.getcwd()),
                            'Data_log', f"{file_name}_{index}.csv")

    @staticmethod
    def path2(file_name2):
        if not os.path.exists('Data_log'):
            os.mkdir('Data_log')
        clock = datetime.now().time()
        index = "_".join(list((date.today().strftime("%b-%d-%Y"),
                         str(clock.hour).zfill(2), str(clock.minute).zfill(2))))
        return os.path.join(os.path.abspath(os.getcwd()),
                            'Data_log', f"{file_name2}_{index}.csv")

    @staticmethod
    def earthpath(earth_name):
        if not os.path.exists('earth_log'):
            os.mkdir('earth_log')
        clock = datetime.now().time()
        index = "_".join(list((date.today().strftime("%b-%d-%Y"),
                         str(clock.hour).zfill(2), str(clock.minute).zfill(2))))
        return os.path.join(os.path.abspath(os.getcwd()),
                            'earth_log', f"{earth_name}_{index}.kml")

    def reading(self):
        if self.device is None:
            print("No Serial device found! Try .connect to start device")
            return
        if self.key is not None:
            return self.reading_key()
        else:
            return self.reading_split()

    def reading_split(self):
        try:
            received = self.read().split(",")  
        except Exception:
            print('Error no attribute')
            return
        self.check_path()
        if len(received) == 0:
            return
        if len(received) == 8:
            with open(self.pathC, "at") as file:
                file.write(','.join(received))
                file.write('\n')
        else:
            with open(self.pathT, "at") as file:
                file.write(','.join(received))
                file.write('\n')

        return received

    def reading_key(self):
        try:
            received = self.read()[:-1].split(",") 
            # received = self.read().split(",")  # recieved from read
            if received == '':
                print('There is none')
                return
        except Exception as e:
            if self.device.is_open:
                pass
            else:
                self.device = serial.Serial(
                    self.com, baudrate=self.baudrate, timeout=60)
                print(self.device)

        self.check_path()


        if received == '':
            return

        if len(received) == 0:
            return

        if len(received) < 4:
            return

        if len(received) == 10:
            with open(self.pathC, 'at') as file:  # save file
                file.write(','.join(received))
                file.write('\n')
        else:
            with open(self.pathT, "at") as file:
                file.write(','.join(received))
                file.write('\n')
        try:
            tolist = self.key['C']
            print(f'this is : {received}')
            if len(received) == 10 :  # check length
                dic = {tolist[i]: received[i] for i in range(len(tolist))}
                return dic
        except Exception as e:
            pass  # map tolist to dict keys set

    def check_path(self):
        with open(self.pathC, 'a+') as file:
            file.seek(0)
            readc = file.read()
            if readc == '':
                file.write(','.join(self.key['C']))
                file.write('\n')
        with open(self.pathT, 'a+') as file:
            file.seek(0)
            readt = file.read()
            if readt == '':
                file.write(','.join(self.key['T']))
                file.write('\n')

    def gearthlive(self):
        file = open('gearthlive.kml', 'w')
        file.writelines('<?xml version="1.0" encoding="UTF-8"?>'
                        '<kml xmlns="http://www.opengis.net/kml/2.2" '
                        'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                        '<NetworkLink><Link><href>'+'\n')
        file.writelines(self.googlename)
        file.writelines('</href><refreshMode>onInterval</refreshMode>'
                        '<refreshInterval>0.1</refreshInterval></Link>'
                        '<refreshInterval>0.1</refreshInterval><refreshMode>onInterval</refreshMode>'
                        '</NetworkLink></kml>')

    def gearthcoord(self, info: str):
        self.coord += info
        with open(self.googlename, 'w') as file:
            file.writelines('<kml xmlns="http://www.opengis.net/kml/2.2" '
                            'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                            '<Folder><name>Log</name><Placemark><name>GRAVITY1072</name>'
                            '<styleUrl>#yellowLineGreenPoly</styleUrl><Style>'
                            '<LineStyle><color>ff00ffff</color><colorMode>normal</colorMode><width>4</width></LineStyle>'
                            '</Style><LineString><extrude>1</extrude><altitudeMode>absolute</altitudeMode><coordinates>'+'\n')
            file.writelines("")
            file.writelines(self.coord+"")
            file.writelines(
                '\n' + '</coordinates></LineString></Placemark></Folder></kml>')


if __name__ == "__main__":
    Allport = Port.list_port()
    for index, port in enumerate(Allport):
        print(f'{index+1}:{port}')
    com = int(input("Choose port :"))-1
    print(Allport[com])
    COM = Port(Allport[com], '$', file_name='ALIEN')
    COM.connect()
    GNSS = int(input("gearth? 0(no) or 1(yes): "))
    if GNSS == 1:
        COM.gearthlive()
        LAT_index = int(input("index of latitude: "))
        LNG_index = int(input("index of longitude: "))
    print(f'saving file to {COM.path}')
    while True:
        PKG = COM.reading()
        print(','.join(PKG))
        if GNSS == 1:
            try:
                LAT = PKG[LAT_index]
                LNG = PKG[LNG_index]
                coord = f"{LAT},{LNG}"
                COM.gearthcoord(coord)
            except Exception:
                print("WRONG INDEX FOR LAT AND LON")
