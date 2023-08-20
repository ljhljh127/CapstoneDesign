"""
CCTV 생성 시나리오
1. 서버에는 이미 ConfigMap이 생성 되어 올라가 있음(rtsp-config)
2. CCTV 추가를 누르면 rtsp-config에 데이터가 추가됨(업데이트) cctv1 : rtsp://~
3. 컨피그맵이 성공적으로 업데이트 되었다는 response를 받으면  cctv1으로 명명된 deployment 생성
"""
import requests
import os
import k8sAPI

# 전역적으로 사용할 URL,JWT_TOKEN 값 정의 나중에 k8sAPI 로 옮길거임
with open("../../token/Kub.txt", "r") as file:
    lines = file.readlines()
    URL = lines[0].strip().split("=")[1]
    JWT_TOKEN = lines[1].strip().split("=")[1]

# 1번 이미 완료


# 2번 컨피그맵 업데이트
def Update_configmap(cctv_name, rtsp_url):
    _resource_type="configmaps"
    _resource_name="rtsp-config"
    _resource_data={
        "data": {cctv_name: rtsp_url}
    }
    response = k8sAPI.call_k8s_api_put(URL, JWT_TOKEN, _resource_type, _resource_name,  _resource_data)

    return response


#3번 디플로이먼트 생성
def Create_deployment(cctv_name):
    _resource_type="deployments"
    _resource_data = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": cctv_name,
            "namespace": "cctv"
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "cctv"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "cctv"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "cctv-container",
                            "image": "nginx", # 테스트이미지
                            "env": [
                                {
                                    "name": "RTSP_URL",
                                    "valueFrom": {
                                        "configMapKeyRef": {
                                            "name": "rtsp-config",
                                            "key": cctv_name
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    response = k8sAPI.call_k8s_api_post(URL, JWT_TOKEN, _resource_type, _resource_data)

    return response


if __name__ == "__main__":
    cfu_result=Update_configmap("cctv1","rtsp://test1")
    if cfu_result.status_code == 200:
        dmc_result=Create_deployment("cctv1")
        if dmc_result.status_code == 200:
            print(dmc_result.status_code)
        
