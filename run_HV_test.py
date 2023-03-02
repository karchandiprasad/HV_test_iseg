####Authors:
####Aloke Kumar Das, Chandiprasad Kar ############
####email "das21aloke@gmail.com"

#!/usr/bin/python
import io
import serial, time
import sys
import csv
from optparse import OptionParser
import serial.tools.list_ports as port_list


usage = ("Usage: %prog --filename name --voltage_in Incre --start_volt IVolt --end_volt EVolt"
         "\nThe Code used to collect data for HV test"
         "\nUse -h for help")

parser = OptionParser(usage=usage)

parser.add_option('-f', '--filename',
                  dest = 'filename',
                  default = 'filename.txt',
                  help = "Filename name to put all the values.Default: 'filename.txt'.",
                  metavar = 'FD')

parser.add_option('-v', '--voltage_in',
                  dest = 'voltage_in',
                  default = 5,
                  help = "Voltage increament, Default:5",
                  metavar = 'VIN')

parser.add_option('-s', '--start_volt',
                  dest = 'start_volt',
                  default = 10,
                  help = "Starting voltage is 10, CHange if you want to.",
                  metavar = 'VS')

parser.add_option('-e', '--end_volt',
                  dest = 'end_volt',
                  default = 100,
                  help = "Ending voltage is 100, CHange if you want to.",
                  metavar = 'VE')
parser.add_option('-p', '--step_volt',
                  dest = 'step_volt',
                  default = 10,
                  help = "Step size of voltage is 10, Change if you want to.",
                  metavar = 'Vst')

(options, arguments) = parser.parse_args()

print("filename,",options.filename)
print("Initial Volt,",options.voltage_in)
print("Volt StepSize,",options.voltage_in)
print("Start Volt,",options.step_volt)
print("End Volt,",options.end_volt)

V_b=int(options.start_volt)
V_e=int(options.end_volt)
V_step=int(options.step_volt)

finaloutput=[]
       
ports = list(port_list.comports())
for p in ports:
    print (p)


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

starting="D1=10"
ser.write((starting+eol_char).encode('utf-8'))
time.sleep(0.2)
starting_Cur='C1=0.5E-3'
ser.write((starting_Cur+eol_char).encode('utf-8'))
time.sleep(0.2)
starting_Kill='T1=1'
ser.write((starting_Kill+eol_char).encode('utf-8'))
time.sleep(0.2)

for incre in range(V_b, V_e+V_step, V_step):
    mindata=[]    
    print("Voltage:"+str(incre)+"\n")    
    sending = "D1="+str(incre)
    ser.write((sending+eol_char).encode('utf-8'))
    time.sleep(0.2)
    ans=sio.read()
    sys.stdout.write('recieved:'+str(ans))
    ## Measure voltage after setting
    ser.write(("U1"+eol_char).encode('utf-8'))
    time.sleep(0.2)
    ans_v=sio.read()
    sys.stdout.write('Measured Voltage:'+str(ans_v))
    ### Measure current after volatage setting
    ser.write(("I1"+eol_char).encode('utf-8'))
    time.sleep(0.2)
    ans_i=sio.read()
    sys.stdout.write('Measured Current:'+str(ans_i))

    #mindata.append(str(incre))
    #mindata.append(str(ans))
    mindata.append(str(ans_v))
    mindata.append(str(ans_i))
    
    finaloutput.append(mindata)
    

print('\nDone\n')

with open(options.filename, 'w') as f:
    csv.writer(f, delimiter=' ').writerows(finaloutput)

ser.close()  



