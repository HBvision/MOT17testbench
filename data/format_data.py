import cv2
import numpy as np

root = './' + input('Input the dataset folder: ')
filename = root + input("Please input the filename: ")
directory = root + input("Please input the desired directory name: ") + "/"
cap = cv2.VideoCapture(filename)

if (cap.isOpened()== False):
	print("Error with opening the provided file")

current_frame = 0
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame',frame)
        current_filename = directory + "%06d.jpg" % current_frame
        cv2.imwrite(current_filename, frame)
        current_frame += 1

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()