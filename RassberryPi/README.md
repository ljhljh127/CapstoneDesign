# 라즈베리파이 RTSP 전송 설정

## RTSP 설정

  ### 1. 우분투(Rasbian OS)를 모두 업데이트 시킨다.
  ```
      sudo apt-get update
      sudo apt-get upgrade
  ```

        
  ### 2. 필요한 유틸리티를 설치한다.
  ```
      sudo apt-get install v4l-utils
      sudo modprobe bcm2835-v4l2
      sudo apt-get install liblivemedia-dev libv4l-dev cmake libasound2-dev
  ``` 

       
  ### 3. RTSP 설치 소스를 다운 받는다(현재 폴더에 존재)
   h264_v4l2_rtspserver

  ### 4. 소스를 컴파일한다.
  ```
      cd h264_v4l2_rtspserver
      sudo cmake .
      sudo make
  ```

       
  
  ### 5. OpenSSL 에러가 날시 편집기를 열어 다음과 같은 내용을 기술한 후 bash 명령으로 실행한다.
  ```
  vim install-openssl.sh
  ```
  ```
  OPENSSL_VER=1.1.0g
  mkdir openssl
  cd openssl
  wget https://www.openssl.org/source/openssl-${OPENSSL_VER}.tar.gz
  tar xf openssl-${OPENSSL_VER}.tar.gz
  cd openssl-${OPENSSL_VER}
  ./config zlib shared no-ssl3
  make -j4
  sudo make install
  ```

  ```
  bash install-openssl.sh
  ```
  ### 6. 실행
  ```
  sudo ./h264_v4l2_rtspserver/h264_v4l2_rtspserver -F 25 -W 1280 -H 720 -P 8555 /dev/video0
  ```



본 문서는 https://remnant24c.tistory.com/357 를 참고하였으며
설치시 에러가 발생하는 부분의 코드를 수정하여 놓았습니다.
(h264_v4l2_rtspserver의 src/cpp 에서 에러가 발생하였음)

