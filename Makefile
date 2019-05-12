.PHONY: run-dev
run-dev:
	docker-compose -f docker-compose-deploy.yml up --build --force-recreate
.PHONY: run
run:
	docker-compose up --build --force-recreate

.PHONY: clean
clean:
	docker-compose rm -vf

.PHONY: build
build:
	docker run -v ${PWD}:/local swaggerapi/swagger-codegen-cli-v3:3.0.8 generate -i /local/openapi/spec.yaml -l typescript-angular -o /local/frontend_angular/src/app/api/
