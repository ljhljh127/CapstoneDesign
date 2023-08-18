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
        raise f"create ConfigMap failed: {e}"
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

