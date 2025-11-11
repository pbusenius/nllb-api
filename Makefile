.PHONY: docker-build docker-push docker-build-cuda docker-push-cuda docker-run-cuda download-models help docker-clean

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
	@echo "  docker-run-cuda   - Run CUDA Docker container with GPU support"
	@echo "  docker-push       - Push Docker image to registry"
	@echo "  docker-push-cuda  - Push CUDA Docker image to registry"
	@echo "  download-models   - Download models to local cache"
	@echo "  docker-clean      - Clean up Docker build cache and intermediate stages"
	@echo ""
	@echo "Variables:"
	@echo "  TAG              - Image tag (default: main)"
	@echo "  IMAGE_NAME       - Image name (default: pbusenius/nllb-api)"
	@echo "  PORT             - Server port (default: 49494)"

# Download models to local cache
download-models:
	@uv run python scripts/download_models.py

# Build Docker image (CPU)
docker-build:
	DOCKER_BUILDKIT=1 docker build --rm -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) .

# Build Docker image (CUDA)
docker-build-cuda:
	@if [ ! -d "models" ]; then \
		echo "Warning: models/ directory not found. Creating empty directory."; \
		echo "Run 'make download-models' first to include models in the image."; \
		mkdir -p models; \
	fi
	DOCKER_BUILDKIT=1 docker build --rm -f $(DOCKERFILE_CUDA) -t $(IMAGE_NAME):$(TAG)-cuda .

# Run CUDA Docker container with GPU support
PORT ?= 49494
docker-run-cuda:
	docker run --init --rm --gpus all \
		-e USE_CUDA=True \
		-e SERVER_PORT=$(PORT) \
		-p $(PORT):$(PORT) \
		$(IMAGE_NAME):$(TAG)-cuda

# Push Docker image to registry
docker-push: docker-build
	docker push $(IMAGE_NAME):$(TAG)

# Push CUDA Docker image to registry
docker-push-cuda: docker-build-cuda
	docker push $(IMAGE_NAME):$(TAG)-cuda

# Clean up Docker build cache and intermediate stages
docker-clean:
	docker builder prune -a -f

