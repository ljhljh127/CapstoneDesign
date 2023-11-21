# 종합설계(CapstoneDesign)
## 프로젝트 설명
### 주제: 실시간 영상처리 기반의 압사사고 방지 시스템
### 목적: 압사사고 발생을 사전에 감지하고 막기 위함
### 기술스택
**인프라** 
<br><img src= "./MarkdownImage/jeonghyeon/main readme/kub.png">
<img src= "./MarkdownImage/jeonghyeon/main readme/docker.png"><br><br>
- 쿠버네티스, 도커 : 여러 CCTV를 효율적으로 확장 및 관리하기 위해 사용
   - Scale Up에는 한계가 있기 때문에 Scale Out을 위한 고려한 구조 고안
   - Rolling Update를 통한 알고리즘, 모델의 업데이트시 무중단 업데이트 고안
   - 컨테이너 이미지를 통환 효율적인 관리

**AI**
<br><img src= "./MarkdownImage/jeonghyeon/main readme/yolo.png">
<img src= "./MarkdownImage/jeonghyeon/main readme/opencv.png"><br><br>
- YOLO: 객체 탐지에 특화되어 있으며 현존 모델중 가장 좋은 성능을 보인 v6를 사용하였음
- OpenCV: 영상 처리를 위하여 사용

**Backend**
<br><img src= "./MarkdownImage/jeonghyeon/main readme/nginx.png"  width="130" height="100">
<img src= "./MarkdownImage/jeonghyeon/main readme/fastapi.png" width="130" height="100">
<img src= "./MarkdownImage/jeonghyeon/main readme/grpc.png"  width="130" height="100"><br><br
- Nginx: 웹서버를 위해 사용
- FastAPI: 쿠버네티스 API를 외부에서 fastAPI를 통하여 호출, 실시간 영상을 받아오기 위해 사용
- gRPC 클러스터내 파드간 API 호출보다 빠른 전송을 위해 사용하였음

---
### 개발 규칙

**main 브랜치** : 모든 통합이 완료된 후 최종본을 적용할 브랜치(release)<br>
**develop 브랜치** : 각 기능들을 만든 후 통합시키는 브랜치<br>
**feature/~ 브랜치** : 각 기능을 만드는 브랜치<br>

<span style="color:red">**주의사항**</span><br>
- 충돌을 막기 위하여 서로의 코드를 건드릴 때는 서로 소통 후 진행
- 같은 폴더에서 개발할 때 안에 개인 이름으로 된 폴더 만들고 진행(꼬임 방지)


<br>

**시작하기**
 1. git clone을 진행한다.
    ```
    git clone https://github.com/ljhljh127/CapstoneDesign.git
    ```
    
 2. 각 기능을 제작할 때 feature/기능명 으로 브랜치를 만든다.
    ```
    git checkout -b feature/기능명
    ```
    <img src= "./MarkdownImage/jeonghyeon/main readme/1.PNG"><br><br>

 3. 본 프로젝트에서 기본 브랜치는 develop으로 부터 진행되기 때문에 develop 브랜치를 당겨오고 시작한다.
    ```
    git pull origin develop
    ```
    <img src= "./MarkdownImage/jeonghyeon/main readme/2.PNG" width="400" height="200"><br><br>

 4. 원격 저장소의 브랜치명 충돌을 방지하기 위해 항상 브랜치를 만들면 원격 저장소로 올리고 시작한다.
      ```
      git push origin feature/기능명
      ```
      <img src= "./MarkdownImage/jeonghyeon/main readme/3.PNG" width="400" height="200"><br><br>  

 5. 기능의 추가, 변경사항 이 있을 때 pull/request를 요청한다.
      <img src= "./MarkdownImage/jeonghyeon/main readme/4.PNG" width="600" height="300"><br><br>
      <img src= "./MarkdownImage/jeonghyeon/main readme/5.PNG" width="600" height="300"><br><br>

 6. 리뷰어로 전체 팀원을 등록 후 담당자를 ljhljh127로 설정한다.
    <img src= "./MarkdownImage/jeonghyeon/main readme/6.PNG" width="600" height="300"><br><br>

 7. 요청이 수락되면 파생된 브랜치가 develop으로 merge된다.
<br><br>
---








