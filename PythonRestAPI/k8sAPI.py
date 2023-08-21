import requests
import os

# 전역적으로 사용할 URL,JWT_TOKEN 값 정의 
with open("../../token/Kub.txt", "r") as file:
    lines = file.readlines()
    URL = lines[0].strip().split("=")[1]
    JWT_TOKEN = lines[1].strip().split("=")[1]


def call_k8s_api_post(resource_type, resource_data):
    api = f"{URL}/apis/apps/v1/namespaces/cctv/{resource_type}"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Content-Type": "application/json"}
    try:
        response = requests.post(api, json=resource_data, headers=headers, verify=False)
        print(response)
    except Exception as e:
        raise Exception(f"Create {resource_type} failed: {e}")
    if not response.ok:
        raise Exception("Status is not ok")

    return response


def call_k8s_api_put(resource_type, resource_name, resource_data):
    api = f"{URL}/api/v1/namespaces/cctv/{resource_type}/{resource_name}"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}",  "Content-Type": "application/merge-patch+json"}
    try:
        response = requests.patch(api, json=resource_data, headers=headers, verify=False)
    except Exception as e:
       raise Exception(f"Update {resource_type} failed: {e}")
    if not response.ok:
        raise Exception("Status is not ok")

    return response


def call_k8s_api_get(resource_type):
    api = f"{URL}/api/v1/namespaces/cctv/{resource_type}"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Accept": "application/json"}

    try:
        response = requests.get(api, headers=headers, verify=False)
    except Exception as e:
       raise Exception(f"Get {resource_type} failed: {e}")
    if not response.ok:
        raise Exception("Status is not ok")

    return response


# deployment apps/v1 대상 api
def call_k8s_api_put_apps_v1(resource_type, resource_name, resource_data):
    api = f"{URL}/apis/apps/v1/namespaces/cctv/{resource_type}/{resource_name}"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}",  "Content-Type": "application/merge-patch+json"}
    try:
        response = requests.patch(api, json=resource_data, headers=headers, verify=False)

    except Exception as e:
       raise Exception(f"Update {resource_type} failed: {e}")
    if not response.ok:
        raise Exception("Status is not ok")

    return response


def call_k8s_api_delete_apps_v1(resource_type,resource_name):
    api = f"{URL}/apis/apps/v1/namespaces/cctv/{resource_type}/{resource_name}"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Accept": "application/json"}


    try:
        response = requests.delete(api, headers=headers, verify=False)

    except Exception as e:
       raise Exception(f"Update {resource_type} failed: {e}")
    if not response.ok:
        raise Exception("Status is not ok")

    return response