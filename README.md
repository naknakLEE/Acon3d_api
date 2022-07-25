# acon3d

Acon3d의 상품을 관리하는 api를 구현

- 각 상품은 ( 제목 / 본문 / 판매 가격 / 수수료 )을 포함합니다.
    - 제목과 본문은 언어별로 여러 쌍이 존재합니다. (한국어, 영어, 중국어)
    - 판매 가격은 각 나라의 환율을 적용하여 계산됩니다.
    - 수수료는 에디터가 결정합니다.
- 3가지 종류의 사용자가 있습니다.
    - 작가: Acon3d에서 판매를 희망하여, 상품에 대한 정보( 제목 / 본문 / 가격 )를 작성하여 올립니다.
    - 에디터: 작가가 업로드한 상품을 검토&수정 합니다. 에디터에게 승인된 작품만이 Acon3d 쇼핑몰에서 노출됩니다.
    - 고객: Acon3d에서 상품들을 둘러보고 구매합니다.
- 상품은 다음과 같은 단계를 거쳐서 쇼핑몰에 등록됩니다.
    1. 작가가 새로운 상품을 한국어로 **작성**하여, **검토를 요청**합니다.
    2. 에디터가 검토 요청이 들어온 상품들을 확인하여, 본문 등을 읽어보고 수정합니다. 다국어 정보, 수수료 등을 추가로 입력합니다.
    3. 에디터가 **검토를 완료**한 이후에는 쇼핑몰에 노출이 됩니다. 이 때, 쇼핑몰에 설정된 언어에 맞게 상품 정보가 표시되어야 합니다.


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
