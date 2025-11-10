.PHONY: docker-build docker-push docker-build-cuda docker-push-cuda download-models help

# Docker image configuration
IMAGE_NAME := pbusenius/nllb-api
TAG ?= main
DOCKERFILE := Dockerfile
DOCKERFILE_CUDA := Dockerfile.cuda

# Default target
help:
	@echo "Available targets:"
	@echo "  docker-build      - Build Docker image (CPU)"
	@echo "  docker-build-cuda - Build Docker image (CUDA)"
	@echo "  docker-push       - Push Docker image to registry"
	@echo "  docker-push-cuda  - Push CUDA Docker image to registry"
	@echo "  download-models   - Download models to local cache"
	@echo ""
	@echo "Variables:"
	@echo "  TAG              - Image tag (default: main)"
	@echo "  IMAGE_NAME       - Image name (default: pbusenius/nllb-api)"

# Download models to local cache
download-models:
	@uv run python scripts/download_models.py

# Build Docker image (CPU)
docker-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) .

# Build Docker image (CUDA)
docker-build-cuda:
	@if [ ! -d "models" ]; then \
		echo "Warning: models/ directory not found. Creating empty directory."; \
		echo "Run 'make download-models' first to include models in the image."; \
		mkdir -p models; \
	fi
	docker build -f $(DOCKERFILE_CUDA) -t $(IMAGE_NAME):$(TAG)-cuda .

# Push Docker image to registry
docker-push: docker-build
	docker push $(IMAGE_NAME):$(TAG)

# Push CUDA Docker image to registry
docker-push-cuda: docker-build-cuda
	docker push $(IMAGE_NAME):$(TAG)-cuda

