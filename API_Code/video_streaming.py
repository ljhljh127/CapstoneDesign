import cv2

def stream_image(image_path):
    while True:
        frame = cv2.imread(image_path)

        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       bytearray(frame) + b'\r\n')
        else:
            break
