AWS_REGION ?= us-east-1
AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --query Account --output text)
REPOSITORY_NAME ?= mlops-uv-app
IMAGE_TAG ?= latest

ECR_URI = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(REPOSITORY_NAME):$(IMAGE_TAG)

## commands

.PHONY: ecr-login
ecr-login:
	@echo "Logging into ecr"
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

.PHONY: build
build:
	@echo "Bilding docker image"
	docker build --platform linux/amd64 -t $(ECR_URI) .

.PHONY: push	
push:
	@echo "Pushing image: $(ECR_URI)"
	docker push $(ECR_URI)

.PHONY: deploy
deploy: ecr-login build push
	@echo "Succesfully deployed to $(ECR_URI)"


