import cv2
import base64
import numpy as np

# RTSP URL
url = 'rtsp://192.168.0.7:8555/unicast'

# 해상도
width = 1280
height = 720

# OpenCV 윈도우 생성
cv2.namedWindow("RTSP Stream", cv2.WINDOW_NORMAL)

# RTSP 스트림 열기
cap = cv2.VideoCapture(url)

# 해상도 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')
    
    # base64 디코딩 및 이미지 생성
    img_data = base64.b64decode(img_base64)
    img_array = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    cv2.imshow("RTSP Stream", img)

    # ESC 키 입력 시 종료
    if cv2.waitKey(1) == 27:
        break

# 자원 해제 및 윈도우 종료
cap.release()
cv2.destroyAllWindows()
