# lunch-menu
- [x] 팀원들의 점심메뉴를 수집
- [x] 분석
- [ ] 알람(입력하지 않은 사람들에게)
- [ ] CSV to DB


## Install DB with Docker
- https://hub.docker.com/_/postgres

```bash
sudo docker run --name local-postgres \
-e POSTGRES_USER=sunsin \
-e POSTGRES_PASSWORD=mysecretpassword \
-e POSTGRES_DB=sunsindb \
-p 5432:5432 \
-d postgres:15.10
```


## Create Table
- postgres

```sql
CREATE TABLE public.lunch_menu (
	id serial4 NOT NULL,
	menu_name text NOT NULL,
	member_name text NOT NULL,
	dt date NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id)
        CONSTRAINT lunch_menu_unique UNIQUE (menu_name, member_name, dt)
);
```


## DEV

- DB
```bash
$ sudo docker start local-postgres

$ sudo docker stop local-postgres

# 도커 지우기
$ sudo docker rm local-postgres

# docker 실행상태 확인
$ sudo docker ps -a 

# 컨테이너 안에서 bash
$ sudo docker exec -it local-postgres bash
```


- RUN
```bash
# DB정보에 맞춰 수정
$ cp env.dummy .env

# 서버 시작
$ streamlit run App.py
```
