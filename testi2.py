import serial
import time
import MySQLdb

#establish connection to MySQL. You'll have to change this for your database.
dbConn = MySQLdb.connect("localhost","root","root","saaasema") or die ("could not connect to database")
#open a cursor to the database
cursor = dbConn.cursor()

def read_serial(ser):
    while True:
        if ser.inWaiting() > 0:
            break;
        time.sleep(0.5)
    return ser.readline()

#device = "/dev/ttyACM0"
buadrate = 9600
ser = serial.Serial("/dev/ttyACM0", buadrate, timeout=1)
time.sleep(2) #wait for the Arduino to init

while True:
    ser.write("Hello\n") #On the Arduino I'm reading with: Serial.readStringUntil('\n');

    data = read_serial(ser)
    print "read: %s" % data
    


    pieces = data.split("\t")
    #print "read: %s" % pieces[1]

    try:
        cursor.execute("INSERT INTO data (kosteus,lampotila) VALUES (%s,%s)", (pieces[0],pieces[1].rstrip()))
        dbConn.commit() #commit the insert
        print "d"
        #cursor.close()  #close the cursor
        
    except MySQLdb.IntegrityError:
        print "failed to insert data"
    #finally:
       # cursor.close()  #close just incase it failed
    time.sleep(1)
