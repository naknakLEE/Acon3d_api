# acon3d

This project was generated using fastapi_template.


## 사전 install
docker
docker-compose
## 사용방법

1. docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
1. docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
1. 브라우저에 localhost:8000 접속 후 api 문서 확인
![img](/docs/Screenshot%20from%202022-07-26%2002-59-24.png)

## API 설명
- [GET] /
    - root path입니다. root path로 정상 접근을 확인하기 위함입니다. 특별한 작동은 없습니다.
- [POST] /token
    - 사용자 인증 API입니다.
    - [GET] /product, [PUT] /product, [POST] /product 를 사용하기 위해 먼저 [POST] /token로 토큰을 발급받아야됩니다.
    - 사용자 정보는 db/user_db.csv를 확인하시면 됩니다.
    - ex) username: writer1 passwodr: 1234 -> 작가 역할
- [GET] /product
    - 작가가 새로운 상품을 한국어로 작성된 리스트를 **에디터**가 확인합니다.
    - token을 에디터 권한으로 받아야 상품 리스트를 조회할 수 있습니다.
- [PUT] /product
    - 에디터가 검토 요청이 들어온 상품들을 확인하여, 본문 등을 읽어보고 수정합니다. 다국어 정보, 수수료 등을 추가로 입력합니다.
    - token을 에디터 권한으로 받아야 상품을 수정할 수 있습니다.
- [POST] /product
    - 작가가 새로운 상품을 한국어로 작성하여 상품을 등록합니다.
    - token을 작가 권한으로 받아야 상품을 등록할 수 있습니다.
- [GET] /list/product
    - 에디터가 검토를 완료한 이후에는 쇼핑몰에 노출이 됩니다.
    - 특별한 권한 없이 누구나 열람 가능합니다.


## Project structure

```bash
$ tree "acon3d"
├── acon3d
│   ├── core
│   │   ├── app.py
│   │   ├── base.py
│   │   ├── config.py
│   │   ├── development.py
│   │   └── logging.py
│   ├── main.py
│   ├── models
│   │   └── common.py
│   ├── router
│   │   └── index.py
│   └── utils
│       ├── auth.py
│       └── db_connection.py
├── build
│   └── Dockerfile
├── db
│   ├── acon3d_db.csv
│   └── user_db.csv
├── docker-compose.dev.yml
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── requirements.txt
```
