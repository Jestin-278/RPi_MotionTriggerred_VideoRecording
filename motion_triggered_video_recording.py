''' Purpose: Records the video using Raspberry Pi for specified time upon detecting motion by PIR Sensor '''

## Import the required libraries
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import datetime
from datetime import datetime as dt
import sys
import os

## Specify the path to the hard disk
path = "/media/pi/External_Hard_Disk/"

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

def video_record(output_file, seconds, frame_rate = 25, resolution = (640, 480)):
''' Function to record the video fo specified amount of time'''
    try:
        camera=PiCamera()
    except:
        print "Recording failed!"
        print "Camera absent"
        sys.exit()
    camera.resolution=resolution
    camera.framerate=frame_rate    
    camera.start_preview(fullscreen=False, window=(100,20,640,480))
    camera.start_recording(output_file)
    camera.wait_recording(seconds)
    camera.stop_preview()
    camera.stop_recording()
    conversion_return_value = os.system("MP4Box -fps "+str(frame_rate)+" -add "+str(output_file)+\
              " "+output_file[:output_file.index(".h264")])
    #print conversion_return_value
    if conversion_return_value == 0:
        os.system("rm "+str(output_file))
        
if __name__== "__main__":
    while True:
		## Check if the hard drive is mounted as External
        external_drive = int(os.popen('sudo mount | grep "External" | wc -l').read())
        if external_drive > 0 and GPIO.input(PIR_PIN):
            print "Motion Detected!"
			## If it is done, create a log file in it
            with open(path+"log_file.txt","a+") as log_file:
				## Get the system time
                start_time=dt.now()
				## If the user has specified the duration, then record till that time
				## else use the default time
                if len(sys.argv)==1:
                    mnts=0.1
                elif len(sys.argv)==2:
                    mnts=int(sys.argv[1])
                else:
                    print "More than required number of arguments"
				## Calculate the end time
                end_time=start_time+datetime.timedelta(minutes=mnts)
				## Calculate the number of lines in the log file
                file_length=sum([1 for line in log_file])
				## Create a name for the output file
                output_file=("sample_video"+str(file_length))
				## Call the video record function
                video_record(path+output_file+".h264",mnts*60) # Start recodring the video
				## Update the log file with the attributes of the video
                log_file.write("\n"+output_file+".mp4"+"\t"+str(end_time-start_time)+\
                               "\t\t"+str(start_time)+"\t"+str(end_time))
                break

