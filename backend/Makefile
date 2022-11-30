build:
	docker compose -f docker-compose.yaml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.yaml up -d

down:
	docker compose -f docker-compose.yaml down

show_logs:
	docker compose -f docker-compose.yaml logs

migrate:
	docker compose -f docker-compose.yaml run --rm api python3 manage.py migrate

makemigrations:
	docker compose -f docker-compose.yaml run --rm api python3 manage.py makemigrations

collectstatic:
	docker compose -f docker-compose.yaml run --rm api python3 manage.py collectstatic --no-input --clear

superuser:
	docker compose -f docker-compose.yaml run --rm api python3 manage.py createsuperuser

down-v:
	docker compose -f docker-compose.yaml down -v

pop_ambas:
	docker compose -f docker-compose.yaml run --rm api python3 manage.py populate_ambassadors

pop_orders:
	docker compose -f docker-compose.yaml run --rm api python3 manage.py populate_orders

pop_prod::
	docker compose -f docker-compose.yaml run --rm api python3 manage.py populate_products

update_rankings:
	docker compose -f docker-compose.yaml run --rm api python3 manage.py update_rankings

flake8:
	docker compose -f docker-compose.yaml exec api flake8 .

black-check:
	docker compose -f docker-compose.yaml exec api black --check --exclude=migrations .

black-diff:
	docker compose -f docker-compose.yaml exec api black --diff --exclude=migrations .

black:
	docker compose -f docker-compose.yaml exec api black --exclude=migrations .

isort-check:
	docker compose -f docker-compose.yaml exec api isort . --check-only --skip env --skip migrations

isort-diff:
	docker compose -f docker-compose.yaml exec api isort . --diff --skip env --skip migrations

isort:
	docker compose -f docker-compose.yaml exec api isort . --skip env --skip migrations	

test:
	docker compose -f docker-compose.yaml run --rm api pytest
