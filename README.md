# gmail-homework

## Description 
지정한 메일주소에서 url을 읽어들여 이미지면 다운받아 정리해주는 스크립트입니다.

~~집에가고싶어요..~~

## TODO
 - [ ] postman - 메인 실행 함수
 - [x] constructor - 폴더 생성 함수
 - [x] downloader - 이미지 다운로더 함수
 - [x] gps_finder - EXIF GPS 파싱 함수
 - [x] hashman - 해쉬 추출 함수
 - [x] stenographer - CSV 작성 함수
 - [ ] map_drawer - 각 이미지별 GPS 시각화 함수
 - [ ] treasure_hunter - 전체 이미지 GPS 시각화 함수 (selenium) 
 - [ ] watchmaker - 윈도우 스케쥴러 등록 함수 
 - [ ] Code beautify
 
## Goal
 - [x] Q1) 프로그램은 한번 실행되면 “fl0ckfl0ck@hotmail.com"로부터 수신된 이메일의 본문에서 단축URL을 파싱하여 업로드된 이미지파일을 다운로드하는 기능을 구현할 것(20점)
 - [ ] Q2) py2exe를 이용하여 윈도우 실행파일로 만들 것(20점)
 - [ ] Q3) 윈도우 스케쥴러를 이용하여 매일 11:50, 23:50 실행파일이 동작하도록 만들 것(10점)
 - [ ] Q4) 프로그램이 실행되면 “YYYY-MM-DD”의 형태로 디렉토리를 만들고 그날의 결과물을 모두 저장할 것(결과물 : 각 이미지파일, csv 파일, 20점)
 - [ ] Q5) 이미지파일의 EXIF 정보를 파싱하여 GPS 데이터를 추출한 뒤 구글맵으로 표현할 것 (10점) 
 - [ ] Q6) 위 과제 모두 해결 후 selenium 라이브러리를 이용하여 위 과제를 해결 할 것(20점)

## config.json
```json
{
  "/": "## Account option ##",
  "account_user": "your_gmail@gmail.com",
  "account_pass": "your_account_pass -> myaccount.google.com/apppasswords",

  ".": "## Mail receive option ##",
  "mail_sender": "search_email@example.com",

  "_": "## Database option ##",
  "database_path": "./db.sqlite"
}
```
