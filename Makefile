IMAGE := bug-tracker-service
VERSION := 1.0.0
REGISTRY_URL := ghcr.io/apinanyogaratnam/${IMAGE}:${VERSION}
REGISTRY_URL_LATEST := ghcr.io/apinanyogaratnam/${IMAGE}:latest

compose-foreign-services:
	docker-compose -f services/postgres/docker-compose.yml -f services/redis/docker-compose.yml up -d

start:
	python3 main.py

build:
	docker build -t ${IMAGE} .

build-linux:
	docker buildx build --platform linux/amd64 ${IMAGE} .

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
	docker tag ${IMAGE} ${REGISTRY_URL_LATEST}

tag-git:
	git tag -m "v${VERSION}" v${VERSION}

push:
	docker push ${REGISTRY_URL}
	git push --tags

push-image:
	docker push ${REGISTRY_URL}
	docker push ${REGISTRY_URL_LATEST}

push-git-tag:
	git push --tags

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

workflow:
	make tag-git && make push-git-tag
