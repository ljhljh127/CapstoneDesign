# 종합설계(CapstoneDesign)

### ※ 개발 규칙

**main 브랜치** : 모든 통합이 완료된 후 최종본을 적용할 브랜치(release)<br>
**develop 브랜치** : 각 기능들을 만든 후 통합시키는 브랜치<br>
**feature/~ 브랜치** : 각 기능을 만드는 브랜치

시작하기
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
      <img src= "./MarkdownImage/jeonghyeon/main readme/4.PNG" width="400" height="200"><br><br>
      <img src= "./MarkdownImage/jeonghyeon/main readme/5.PNG" width="400" height="200"><br><br>

 6. 리뷰어로 전체 팀원을 등록 후 담당자를 ljhljh127로 설정한다.
    <img src= "./MarkdownImage/jeonghyeon/main readme/6.PNG" width="400" height="200"><br><br>

 7. 요청이 수락되면 파생된 브랜치가 develop으로 merge된다.
    
