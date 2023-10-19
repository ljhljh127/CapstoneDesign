from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import k8sAPI
import kubernetes.client.exceptions
import json
from fastapi.responses import StreamingResponse
from video_streaming import stream_image
from fastapi.responses import JSONResponse
import os
import time



# FastAPI 애플리케이션 생성
app = FastAPI(title="CCTV_CRUD")
app.description = "쿠버네티스 환경에서 CCTV를 관리하기 위한 API"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진을 허용하려면 "*"를 사용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 에러 핸들링을 위한 함수
def Error_Handling(e):
    if e.__class__== kubernetes.client.exceptions.ApiException:
        error_info = json.loads(e.body)
        error_message = error_info.get('message')
        raise HTTPException(status_code=e.status, detail=error_message)
    else:
        raise HTTPException(status_code=500, detail="서버에 에러가 발생하였습니다.")



@app.post("/cctvs", status_code=201,tags=["CCTV CREATE"])
def Create_CCTV(cctv_name,rtsp_url):
    try:
        k8sAPI.Create_configmap(cctv_name,rtsp_url)
        k8sAPI.Create_deployment(cctv_name)
        return {"status": "success", "message": "CCTV 추가가 완료되었습니다."}
    except Exception as e:
        Error_Handling(e)


@app.put("/cctvs/{cctv_name}",tags=["CCTV UPDATE"])
def Update_CCTV(cctv_name,rtsp_url):
    try:
        k8sAPI.Update_configmap(cctv_name,rtsp_url)
        k8sAPI.Delete_deployment(cctv_name)
        k8sAPI.Create_deployment(cctv_name)
        return {"status": "success", "message": "CCTV RTSP 주소 변경이 완료되었습니다."}
    except Exception as e:
        Error_Handling(e)


@app.delete("/cctvs/{cctv_name}",tags=["CCTV DELETE"])
def Delete_CCTV(cctv_name):
    try:
        k8sAPI.Delete_deployment(cctv_name)
        k8sAPI.Delete_configmap(cctv_name)
        delete_cctv_files(cctv_name)
        return {"status": "success", "message": "CCTV 삭제가 완료되었습니다."}
    except Exception as e:
        Error_Handling(e)


@app.get("/cctvs", tags=["CCTV READ"])
def Read_CCTV():
    try:
        deployments = k8sAPI.READ_deployment()
        return CCTV_Info(deployments)

    except Exception as e:
        Error_Handling(e)


@app.get("/video/{cctv_name}", tags=["VIDEO GET"])
def GET_Video(cctv_name:str):
    # StringResponse함수를 return하고,
    # 인자로 OpenCV에서 가져온 "바이트"이미지와 type을 명시
    return StreamingResponse(video_streaming(f"/app/CCTV/{cctv_name}.jpg"), media_type="multipart/x-mixed-replace; boundary=frame")
    


@app.get("/Alert/{cctv_name}", tags=["Alert GET"])
def GET_Alert(cctv_name: str):
    file_path = f"/app/Alert/{cctv_name}.txt" 

    first_line = get_first_line_of_file(file_path)
    if first_line is not None:
        return JSONResponse(content={"Alert": first_line})
    else:
        return JSONResponse(content={"error": "파일을 열거나 읽을 수 없습니다."}, status_code=500)
    

# CCTV의 주소와, 현재 쿠버네티스에서의 상태를 return 하기 위한 함수
def CCTV_Info(deployments):
    deployment_info_dict = {}
    for deployment in deployments.items:
        rtsp_url = k8sAPI.READ_configmap(deployment.metadata.name)
        deployment_info_dict[deployment.metadata.name] = {
            "ready": f"{deployment.status.ready_replicas}/{deployment.status.replicas}",
            "rtsp_url": rtsp_url
        }
    return deployment_info_dict


# 비디오 스트리밍을 위한 함수(video_streming.py)
def video_streaming(image_path):
    return stream_image(image_path)


# 알람 여부 읽어오는 함수
def get_first_line_of_file(file_path):
    try:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            return first_line
    except Exception as e:
        return None  
    
# CCTV  파일 삭제
def delete_cctv_files(cctv_name):
    while True:
        # 이미지 파일 삭제
        image_path = f"/app/CCTV/{cctv_name}.jpg"
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Error deleting image file: {e}")
        
        # 알람 여부 파일 삭제
        alert_path = f"/app/Alert/{cctv_name}.txt"
        if os.path.exists(alert_path):
            try:
                os.remove(alert_path)
            except Exception as e:
                print(f"Error deleting alert file: {e}")
        time.sleep(5)
        if not os.path.exists(image_path) and not os.path.exists(alert_path):
            break