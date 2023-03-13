local_install:
	pip install -r requirements.txt

local_run_app:
	pip install -r requirements.txt
	uvicorn app.main:app --reload --port 8000

test:
	pip install -r requirements.txt
	pytest test/test.py

docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

docker_remove_dangling_images:
	docker images --filter "dangling=true" -q --no-trunc | xargs docker rmi

docker_test:
	docker-compose exec app pytest test/test.py

run:
	./scripts/utils.sh

destroy:
	helm uninstall fastapi --namespace fastapi

get_endpoint:
	minikube service fastapi-service --url -n fastapi

unset_minikube_docker_daemon:
	eval $(minikube docker-env -u)
