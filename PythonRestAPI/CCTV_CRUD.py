"""
CCTV 생성 시나리오
1. 서버에는 이미 ConfigMap이 생성 되어 올라가 있음(rtsp-config)
2. CCTV 추가를 누르면 rtsp-config에 데이터가 추가됨(업데이트) cctv1 : rtsp://~
3. 컨피그맵이 성공적으로 업데이트 되었다는 response를 받으면  cctv1으로 명명된 deployment 생성

CCTV 수정 시나리오
생성과 동일하게 진행 가능 다만 Deployment를 post가아닌 patch로 쏘면됨
but patch 시 api가 다르니 유의 apis/apps/v1, api/v1

CCTV 삭제 시나리오
CCTV 이름과 매핑된 디플로이먼트와 컨피그맵 수정 필요
디플로이먼트는 삭제, ConfigMap의 해당 cctv키와 연결된 키값 None으로 만들어 제거

CCTV 조회 시나리오
현재 노드상에 있는 모든 CCTV의 상태와 목록을 조회 가능해야함
API로 긁어와서 양식맞춰 디코딩 해야할듯 
"""

import k8sAPI
import CCTV_Class
from datetime import datetime
import json





# 환경 변수로 사용되는 컨피그맵은 자동으로 업데이트되지 않으며 파드를 다시 시작해야 한다.(쿠버네티스 공식문서)
# ConfigMap Update시 deployment Update 전략을 위해서 현재시간을 어노테이션으로 넣어줌
current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


# deployment_resource_data
def Setting_deployment_resource(cctv_name):
    deployment_resource_data = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": cctv_name,
            "namespace": "cctv",
            "annotations": {
                "deployment.update_at": current_time  # 어노테이션에 현재 시간 추가
            }
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
    return deployment_resource_data



# 컨피그맵 업데이트
def Update_configmap(cctv_name, rtsp_url):
    _resource_type="configmaps"
    _resource_name="rtsp-config"
    _resource_data={
        "data": {cctv_name: rtsp_url}
    }
    response = k8sAPI.call_k8s_api_put(_resource_type, _resource_name,  _resource_data)

    return response


# 디플로이먼트 생성
def Create_deployment(cctv_name):
    _resource_type="deployments"
    _resource_data=Setting_deployment_resource(cctv_name)
    response = k8sAPI.call_k8s_api_post(_resource_type, _resource_data)

    return response

# 디플로이먼트 업데이트
def Update_deployment(cctv_name):
    _resource_type="deployments"
    _resource_data=Setting_deployment_resource(cctv_name)
    response = k8sAPI.call_k8s_api_put_apps_v1(_resource_type, cctv_name, _resource_data)
    
    return response

# 디플로이먼트 삭제
def Delete_deployment(cctv_name):
    _resource_type="deployments"
    response=k8sAPI.call_k8s_api_delete_apps_v1(_resource_type, cctv_name)

    return response

# 디플로이먼트 조회
def GET_deployment():
    _resource_type="deployments"
    response=k8sAPI.call_k8s_api_get_v1(_resource_type)

    return response





# CCTV 생성
def CCTV_CREATE(cctv_name, rtsp_url):
    cfu_result=Update_configmap(f"{cctv_name}",f"rtsp://{rtsp_url}")
    if cfu_result.status_code == 200:
        dmc_result=Create_deployment(cctv_name)
        print(dmc_result)

# CCTV 업데이트
def CCTV_UPDATE(cctv_name, rtsp_url):
    cfu_result=Update_configmap(f"{cctv_name}", rtsp_url)
    if cfu_result.status_code == 200:
        dmu_result=Update_deployment(cctv_name)
        print(dmu_result)

# CCTV 삭제
def CCTV_DELETE(cctv_name):
    dfd_result=Delete_deployment(cctv_name)
    if dfd_result.status_code == 200:
        cfu_result=Update_configmap(f"{cctv_name}",None)
        print(cfu_result)

# CCTV 목록 조회
def CCTV_GET():
    dmg_result=GET_deployment()
    deployment_List = CCTV_Class.DeploymentResponse(**dmg_result.json())

    print(len(deployment_List.items))
    for cctv in deployment_List.items:
        print(f'{cctv["metadata"]["name"]} 상태: {cctv["status"]["readyReplicas"]}')
    


# 나중에 fastapi와 연동해서 아래 함수 호출 인자전달
if __name__ == "__main__":
    print("")
    # CCTV_UPDATE("cctv1","rtsp://test1")
    # CCTV_DELETE("cctv1")
    # CCTV_DELETE("cctv2")
    # CCTV_DELETE("cctv3")
    # CCTV_GET()
    