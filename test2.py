# import pigpio
# pi = pigpio.pi('10.42.0.91')
# pi.write(17, 0)
# print(pi.connected)

######## TEST CAMERA BROADCAST FROM ROV ########

import cv2

# Initialize camera
cap = cv2.VideoCapture("rtsp://10.42.0.91:8554/unicast")  # hope and pray that this is the right port to listen on

while True:
    # Read frame
    ret, frame = cap.read()
    if not ret: break

    # Display frame
    cv2.imshow('Live Feed', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
