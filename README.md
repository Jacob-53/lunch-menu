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
);
```


## DEV
```bash
$ sudo docker start local-postgres
$ sudo docker stop local-postgres
$ sudo docker rm local-postgres
$ sudo docker ps -a 
$ sudo docker exec -it local-postgres bash
```

