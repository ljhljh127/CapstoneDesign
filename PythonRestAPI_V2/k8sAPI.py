from kubernetes import client, config
import ssl

"""
CCTV 생성 시나리오
1. CCTV 생성시 해당 CCTV 이름과 동일한 ConfigMap을 생성함(RTSP_URL 포함)
2. 컨피그맵이 성공적으로 생성 되었다는 response를 받으면 cctv명으로 명명된 deployment 생성

CCTV 수정 시나리오
1. 해당 CCTV 이름과 동일한 Configmap 수정

CCTV 삭제 시나리오
CCTV 이름과 매핑된 디플로이먼트와 컨피그맵 삭제 필요
디플로이먼트, 해당 ConfigMap 삭제

CCTV 조회 시나리오
현재 클러스터내에 있는 모든 CCTV의 상태와 목록을 조회 가능해야함
API로 긁어와서 양식맞춰 디코딩 해야할듯 
"""


# 토큰과 인증관련 설정(배포 용)
config = client.Configuration()
config.api_key["authorization"] = open("/var/run/secrets/kubernetes.io/serviceaccount/token").read()
config.api_key_prefix["authorization"] = "Bearer"
config.host = "https://kubernetes.default"
config.ssl_ca_cert = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
config.verify_ssl=True

# k8s api
core_Api = client.CoreV1Api(client.ApiClient(config))
apps_v1_Api = client.AppsV1Api(client.ApiClient(config))


# # 토큰과 인증관련 설정(개발 용)
# config.load_kube_config()
# core_Api = client.CoreV1Api()
# apps_v1_Api=client.AppsV1Api()

# 대상 namespace 설정
namespace="cctv"


# 컨피그맵 생성
def Create_configmap(cctv_name,rtsp_url):
    configmap = client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata = client.V1ObjectMeta(
            name = cctv_name,
            namespace = namespace
        ),
        data ={"RTSP_URL":rtsp_url}
    )
    response = core_Api.create_namespaced_config_map(namespace,configmap)
   


# 컨피그맵 업데이트
def Update_configmap(cctv_name,rtsp_url):
    configmap = core_Api.read_namespaced_config_map(cctv_name, namespace)
    configmap.data["RTSP_URL"] = rtsp_url
    core_Api.patch_namespaced_config_map(
            name=cctv_name,
            namespace=namespace,
            body=configmap
        )


# 컨피그맵 삭제
def Delete_configmap(cctv_name):
    core_Api.delete_namespaced_config_map(cctv_name,namespace)


# 컨피그맵 조회
def READ_configmap(cctv_name):
    configmap = core_Api.read_namespaced_config_map(cctv_name,namespace)
    return configmap.data.get("RTSP_URL", "등록된 rtsp 주소가 없습니다.")   



# 디플로이먼트 리소스 설정
def Setting_deployment_resource(cctv_name):
    deployment_resource_data = {
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
                    "volumes": [
                        {
                            "name": "config-volume",
                            "configMap": {
                                "name": cctv_name, 
                            }
                        }
                    ],
                    "containers": [
                        {
                            "name": "cctv-container",
                            "image": "nginx",  # 테스트 이미지
                            "volumeMounts": [
                                {
                                    "name": "config-volume",
                                    "mountPath": "/etc/config",
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    return deployment_resource_data


# 디플로이먼트 생성
def Create_deployment(cctv_name):
    deployment = Setting_deployment_resource(cctv_name)
    apps_v1_Api.create_namespaced_deployment(namespace,deployment)


# 디플로이먼트 삭제
def Delete_deployment(cctv_name):
    apps_v1_Api.delete_namespaced_deployment(cctv_name,namespace)

# 디플로이먼트 조회
def READ_deployment():
    return apps_v1_Api.list_namespaced_deployment(namespace)
