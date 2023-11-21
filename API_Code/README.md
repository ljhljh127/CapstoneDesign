
# API_Pod_Code
### k8sAPI.py
- Python을 이용하여 쿠버네티스 API에 CRUD 요청을 보내기 위한 핵심코드
- 토큰 정보는 해당 네임스페이스에 연결된 서비스어카운트의 시크릿으로 부터 받아옴
(네임스페이스에 이 API 파드가 떠있으므로 가능)

---
### main.py
- fastAPI 기반의 쿠버네티스 API를 호출하기 위한 외부 요청에 대한 코드
- 실시간으로 이미지를 긁어오기 위한 코드

---

### gRPCserver.py
- API 파드내에 함께 실행되는 gRPC 서버 코드
- 이미지 처리 파드로부터 지속적으로 처리된 사진을 전송받음
---
### image_transfer_pb2,_gtrpc2
- proto 빌드시 자동적으로 생성되는 코드(grpc를 위함)
---
### video_streming.py
- 비디오 스트리밍을 위한 코드 사진을 토대로 지속적 스트림 생성