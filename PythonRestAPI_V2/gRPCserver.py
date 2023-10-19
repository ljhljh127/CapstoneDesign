import cv2
import numpy as np
import grpc
import image_transfer_pb2
from concurrent import futures
import image_transfer_pb2_grpc

class ImageTransferService(image_transfer_pb2_grpc.ImageTransferServiceServicer):
    def PostImage(self, request, context):
        # 클라이언트에 성공 여부 전송
        shape = (1080, 1920, 3)  # 원하는 이미지 모양
        image = self.decode_image(request.image_data, shape)
        cctv_id =request.cctv_id
        self.save_image(image,cctv_id)  # 이미지를 파일로 저장
        response = image_transfer_pb2.ImageResponse(message="success")
        return response

    def decode_image(self, image_data, shape):
        # 이미지 데이터를 numpy 배열로 변환
        image = np.frombuffer(image_data, dtype=np.uint8)
        # 원하는 모양으로 변환
        image = image.reshape(shape)
        # print(image)
        return image

    def save_image(self, image, cctv_id):
        # 이미지를 파일로 저장
        cv2.imwrite(f'/app/CCTV/{cctv_id}.jpg', image)  # 이미지를 저장

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
