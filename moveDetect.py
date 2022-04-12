from datetime import datetime
import cv2, pandas, time

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#first frame set up
first_frame = None
check, first_frame = video.read ()
first_frame = cv2.cvtColor(first_frame,cv2.COLOR_BGR2GRAY)
first_frame = cv2.GaussianBlur(first_frame, (21,21),0)
status = 0 #variable to store motion det. status
single_event = []
events = []
df = pandas.DataFrame(columns=["Start","End"])


while True:
    check, frame = video.read ()
    grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # change frame to grayscale
    blured_frame = cv2.GaussianBlur (grey_frame, (21,21),0) # blur frame
    delta_frame = cv2.absdiff (first_frame,blured_frame)
    tresh_frame = cv2.threshold (delta_frame, 30, 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    tresh_frame = cv2.dilate (tresh_frame, None, iterations=2)

    (cnts,__) = cv2.findContours(tresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    number_of_contours = 0
    for contour in cnts:
        if cv2.contourArea(contour) > 100:
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            number_of_contours = number_of_contours + 1
    if number_of_contours > 0:
        if status == 0:
            single_event = [datetime.now(), None]
        status = 1
    else:
        if status == 1:
            single_event[1] = datetime.now()
            events.append (single_event)
        status = 0

    cv2.namedWindow("Tytul");
    cv2.moveWindow("Tytul", 50,50);    
    cv2.imshow("Tytul",frame)

    first_frame = blured_frame

    key = cv2.waitKey(1)
    if key == ord ('q'):
        if single_event[0] != None and single_event[1] == None:
            single_event[1] = datetime.now()
            events.append (single_event)           
        break
video.release()
cv2.destroyAllWindows()

df = pandas.DataFrame(events, columns = ['Start','End'])
df.to_csv("motion.csv")
