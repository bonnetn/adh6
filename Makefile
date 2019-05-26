.PHONY: run-dev
run-dev:
	docker-compose -f docker-compose-deploy.yml up --build --force-recreate
.PHONY: run
run:
	docker-compose up --build --force-recreate

.PHONY: clean
clean:
	docker-compose rm -vf

.PHONY: generate
generate:
	docker run --rm -v $(CURDIR):/local openapitools/openapi-generator-cli generate -i /local/openapi/spec.yaml -g typescript-angular -o /local/frontend_angular/src/app/api/
