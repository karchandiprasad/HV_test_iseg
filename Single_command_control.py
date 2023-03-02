#Author "Aloke Kumar Das"
#email "das21aloke@gmail.com"
#!/usr/bin/python
import io
import serial, time
import sys
#initialization and open the port
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print (p)

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port = "COM6"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False    #disable software flow control
ser.rtscts =  False  #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
#ser.writeTimeout = 2    #timeout for write

try: 
    ser.open()
except (Exception):
    print("error open serial port: " )
    exit()

eol_char='\r\n'
sio=io.TextIOWrapper(io.BufferedReader(ser),newline=eol_char)
if ser.isOpen():
    print("opened successfully: " )
else:
    print("cannot open serial port ")


while True:
  sending = input("type:\n")
  ser.write((sending+eol_char).encode('utf-8'))
  time.sleep(0.2)
  ans=sio.read()
  sys.stdout.write('recieved:'+str(ans))
  print('\nsucessed try new command\n')
  #ser.close()

