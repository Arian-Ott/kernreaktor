.PHONY: dev prod

dev:
	docker compose down
	docker compose up -d

prod:
	docker compose down
	docker compose up -d maria reaktor