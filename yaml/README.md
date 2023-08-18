 # YAML

본 YAML 파일은 쿠버네티스 API통신을 위하여 ClusterRole을 만들고 바인딩 하기 위함임
<br>클러스터내의 모든 항목에 대한 CRUD를 가능하게함

---
## YAML 파일 설명

### cctv-api-secret.yaml
- ServiceAccount에 반영시킬 secret(토큰)

### ServiceAccount.yaml
- 위에서 만든 secret을 포함한 ServiceAccount

### CCTVManagerRole.yaml
- Cluster Role을 생성하는 yaml(여기서는 모든 권한을 주었음)

### CCTVMangerRoleBinding.yaml
- 생성된 Cluster Role을 바인딩하는 yaml

---
### 적용법
먼저 cctv라는 namespace를 생성 후
```
kubectl create namespace cctv
```

아래의 명령어를 사용하여 위부터 순차적으로 적용
```
kubectl apply -f ~
```

