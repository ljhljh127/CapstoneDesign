import cv2
import numpy as np
import grpc
import image_transfer_pb2
from concurrent import futures
import image_transfer_pb2_grpc

class ImageTransferService(image_transfer_pb2_grpc.ImageTransferServiceServicer):
    def PostImage(self, request, context):
        
        image = self.decode_image(request.image_data)
        # CCTV ID
        cctv_id =request.cctv_id

        # 이미지 저장
        self.save_image(image,cctv_id)

        # 압사 위험 여부
        alert_text = request.alert
        self.save_alert_to_file(cctv_id, alert_text)

        response = image_transfer_pb2.ImageResponse(message="success")
        return response

    # 이미지 저장함수
    def decode_image(self, image_data):

        # 데이터를 numpy 배열로 변환
        shape = (1080, 1920, 3) 
        image = np.frombuffer(image_data, dtype=np.uint8)
        # 형식 변환
        image = image.reshape(shape)
        return image

    def save_image(self, image, cctv_id):
        # 이미지를 파일로 저장
        cv2.imwrite(f'/app/CCTV/{cctv_id}.jpg', image)

    def save_alert_to_file(self, cctv_id, alert_text):
        # alert 정보를 파일로 저장
        file_path = f'/app/Alert/{cctv_id}.txt'
        with open(file_path, 'w') as alert_file:
            alert_file.write(str(alert_text))

def serve():
    server_option = (
        ('grpc.max_send_message_length', 8 * 1024 * 1024),
        ('grpc.max_receive_message_length', 8 * 1024 * 1024),
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=server_option)
    image_transfer_pb2_grpc.add_ImageTransferServiceServicer_to_server(ImageTransferService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
