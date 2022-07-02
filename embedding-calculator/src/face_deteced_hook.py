#!python3
import serial
import serial.tools.list_ports as list_ports
import threading

lock = threading.Lock()

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1
def find_comport(pid, vid, baud):
  """ return a serial port """
  ser_port = serial.Serial(timeout=TIMEOUT)
  ser_port.baudrate = baud
  ports = list(list_ports.comports())
  print(f'scanning {len(ports)} ports')
  for p in ports:
    print('port: {}'.format(p))
    try:
      print('pid: {} vid: {}'.format(p.pid, p.vid))
    except AttributeError:
      continue
    if (p.pid == pid) and (p.vid == vid):
      print('found target device pid: {} vid: {} port: {}'.format(
        p.pid, p.vid, p.device))
      ser_port.port = str(p.device)
      return ser_port
  print('Did not found microbit!')
  return None

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]


class MicrobitClicker(metaclass=Singleton):
  def __init__(self):
    self.ser_port = None

  def click(self):
    if not self.ser_port:
      with lock:
        if not self.ser_port:
          self.ser_port = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
          self.ser_port.open()

    self.ser_port.write(b'#')

def handle_faces(faces):
  print(faces)
  MicrobitClicker().click()


def main():
  print('looking for microbit')
  clicker = MicrobitClicker()
  # ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
  # if not ser_micro:
  #   print('microbit not found')
  #   return
  # print('opening and monitoring microbit port')
  # ser_micro.open()
  while True:
    to_send = input()
    clicker.click()
    #ser_micro.write(to_send.encode('utf8'))

    #line = ser_micro.readline().decode('utf-8')
    #if line:  # If it isn't a blank line
    #  print(line)
  #ser_micro.close()

if '__main__' == __name__:
  main()
