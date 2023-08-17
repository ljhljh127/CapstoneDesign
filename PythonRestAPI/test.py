import requests
import os
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PodResponse:
    kind: str
    apiVersion: str
    metadata: Dict
    items: List


def call_k8s_api(ENDPOINT, JWT_TOKEN):
    """kubernetes API 호출"""
    api = f"{ENDPOINT}/api/v1/namespaces/default/pods"
    headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Accept": "application/json"}

    try:
        response = requests.get(api, headers=headers, verify=False)
    except Exception as e:
        raise f"call k8s API is failed: {e}"
    if not response.ok:
        raise "status is not ok"

    return response


def get_pods_default_namespace():
    """default namespace에 있는 pod 조회"""
    ENDPOINT = os.getenv("ENDPOINT", "")
    JWT_TOKEN = os.getenv("JWT_TOKEN", "")

    if ENDPOINT == "":
        raise "Check ENDPOINT"

    if JWT_TOKEN == "":
        raise "Check JWT_TOKEN"

    response = call_k8s_api(ENDPOINT, JWT_TOKEN)
    pod_specs = PodResponse(**response.json())

    for pod_item in pod_specs.items:
        print(f'pod {pod_item["metadata"]["name"]}\t{pod_item["status"]["phase"]}')


if __name__ == "__main__":
    get_pods_default_namespace()