# 나중에 CCTV1-config의 형태로 변경 늘어날 때마다 1,2,....fstring으로 받아서 처리함 될듯..
# metadata 부분에서
import requests
import os

def call_k8s_api(ENDPOINT, JWT_TOKEN):
    api = f"{ENDPOINT}/api/v1/namespaces/cctv/configmaps"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Content-Type": "application/json"}
    configmap_data = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": "rtsp-config"},
        "data": {"RTSP_URL": "rtsp://test56785678"}
    }

    try:
        response = requests.post(api, json=configmap_data, headers=headers, verify=False)
        print(response)
    except Exception as e:
        raise f"create ConfigMap failed: {e}"
    if not response.ok:
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
    print("ConfigMap created successfully.")


if __name__ == "__main__":
    create_configmap()