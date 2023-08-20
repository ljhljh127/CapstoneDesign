# 환경 변수로 사용되는 컨피그맵은 자동으로 업데이트되지 않으며 파드를 다시 시작해야 한다.(쿠버네티스 공식문서)
# 나중에 만약 CCTV 주소를 변경하는 과정을 수행 할 때에는 파드를 재시작하거나 파드 내리고 다시 올려야할듯 이부분 나중에 고려사항
import requests
import os

def call_k8s_api(ENDPOINT, JWT_TOKEN):
    api = f"{ENDPOINT}/api/v1/namespaces/cctv/configmaps/rtsp-config"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}",  "Content-Type": "application/merge-patch+json"}
    configmap_data = {
        "data": {"RTSP_URL": "rtsp://Happycat"}
    }

    try:
        response = requests.patch(api, json=configmap_data, headers=headers, verify=False)
    except Exception as e:
        raise f"update ConfigMap failed: {e}"
    if not response.ok:
        print(response)
        raise "status is not ok"

    return response

def create_configmap():
    ENDPOINT = ""
    JWT_TOKEN = ""
    if ENDPOINT == "":
        raise ValueError("Check ENDPOINT")

    if JWT_TOKEN == "":
        raise ValueError("Check JWT_TOKEN")

    response = call_k8s_api(ENDPOINT, JWT_TOKEN)
    print("ConfigMap update successfully.")


if __name__ == "__main__":
    create_configmap()

