####Authors:
####Aloke Kumar Das, Chandiprasad Kar ############
####email "das21aloke@gmail.com"

#!/usr/bin/python
import io
#import serial, time
import sys
import csv
from optparse import OptionParser
#import serial.tools.list_ports as port_list


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

(options, arguments) = parser.parse_args()

print("filename,",options.filename)
print("filename,",options.voltage_in)
print("filename,",options.start_volt)
print("filename,",options.end_volt)


finaloutput=[]
       
ports = list(port_list.comports())
for p in ports:
    print (p)

# #possible timeout values:
# #    1. None: wait forever, block call
# #    2. 0: non-blocking mode, return immediately
# #    3. x, x is bigger than 0, float allowed, timeout block call

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

for incre in range(10, 100, 10):
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

    mindata.append(str(incre))
    mindata.append(str(ans))
    mindata.append(str(ans_v))
    mindata.append(str(ans_i))
    
    finaloutput.append(mindata)
    

print('\nDone\n')

with open(options.filename, 'w') as f:
    csv.writer(f, delimiter=' ').writerows(finaloutput)

ser.close()  






    

#    try:
#        ser.flushInput() #flush input buffer, discarding all its contents
#        ser.flushOutput()#flush output buffer, aborting current output 
                 #and discard all that is in buffer

#        #write data
#        ser.write("AT+CSQ")
#        print("write data: AT+CSQ")

#        time.sleep(0.5)  #give the serial port sometime to receive the data

#        numOfLines = 0

#        while True:
#          response = ser.readline()
#          print("read data: " + response)

#          numOfLines = numOfLines + 1

#          if(numOfLines >= 5):
#            break

#        ser.close()
#    #except (Exception, e1):
#    except (Exception):
#        #print("error communicating...: " + str(e1))
#        print("error communicating...: ")

#else:
#    print("cannot open serial port ")
