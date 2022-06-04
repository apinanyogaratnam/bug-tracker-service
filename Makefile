IMAGE := bug-tracker-service
VERSION := 0.0.2
REGISTRY_URL := ghcr.io/apinanyogaratnam/${IMAGE}:${VERSION}

start:
	python3 main.py

build:
	docker build -t ${IMAGE} .

up:
	docker-compose up --build --remove-orphans

down:
	docker-compose down

run:
	docker run -d -p 8000:8000 ${IMAGE}

exec:
	docker exec -it $(sha) /bin/sh

auth:
	grep -v '^#' .env.local | grep -e "CR_PAT" | sed -e 's/.*=//' | docker login ghcr.io -u USERNAME --password-stdin

tag:
	docker tag ${IMAGE} ${REGISTRY_URL}
	git tag -m "v${VERSION}" v${VERSION}

tag-image:
	docker tag ${IMAGE} ${REGISTRY_URL}

tag-git:
	git tag -m "v${VERSION}" v${VERSION}

push:
	docker push ${REGISTRY_URL}
	git push --tags

push-image:
	docker push ${REGISTRY_URL}

all:
	make build && make auth && make tag && make push

# script commands
create-users:
	python3 scripts/create_users_table.py

create-projects:
	python3 scripts/create_projects_table.py

create-tables:
	python3 create_tables.py

load-test-data:
	python3 test_data_loader.py
