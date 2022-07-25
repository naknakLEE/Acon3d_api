# acon3d

This project was generated using fastapi_template.


## 사전 install
docker
docker-compose
## 사용방법

1. docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
1. docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

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
