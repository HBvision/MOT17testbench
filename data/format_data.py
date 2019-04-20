import cv2
import numpy as np

# root = './' + input('Input the dataset folder: ')
# filename = root + input("Please input the filename: ")
# directory = root + input("Please input the desired directory name: ") + "/"
filename = "./vid2.mp4"
directory = "./HB/HB09/"
cap = cv2.VideoCapture(filename)

if cap.isOpened() is not True:
    print("Error with opening the provided file")

current_frame = 1
track = 1
while cap.isOpened():
    # Capture frame-by-frame
    if track < 150:
        ret, frame = cap.read()
        track += 1
    else:
        ret, frame = cap.read()
        if ret:

            # Display the resulting frame
            cv2.imshow('Frame', frame)
            current_filename = directory + "%06d.jpg" % current_frame
            cv2.imwrite(current_filename, frame)
            current_frame += 1

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
