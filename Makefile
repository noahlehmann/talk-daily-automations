# Variables
PDF_NAME := "slides.pdf"
TEX_BASE := "slides"
CONTAINERFILE := "build/tex/Containerfile"
BUILD_TOOL := $(shell command -v docker 2>/dev/null)

# Ensure Docker is available
ifeq ($(BUILD_TOOL),)
$(error "Docker not found! Install it first.")
endif

.PHONY: all git slides

all: init slides
init: venv git web-env sqlite

# Install pre-commit hooks
git: .githooks/pre-commit
	@echo "Installing pre-commit hooks..."
	cp -r .githooks/* .git/hooks/
	@echo "Make pre-commit hooks executable..."
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hooks installed."

venv:
	@echo "Setting up the project..."
	@if [ ! -d ".venv" ]; then \
    		echo "Creating virtual environment..."; \
    		python3 -m venv .venv; \
    		.venv/bin/pip install --upgrade pip; \
    		.venv/bin/pip install -r ansible/requirements.txt -r src/api/requirements.txt; \
    	else \
    		echo "Virtual environment already exists."; \
    	fi

web-env: src/web
	@echo "Setting up the web app..."
	@if [ ! -d "src/web/node_modules" ]; then \
			echo "Installing node modules..."; \
			cd src/web && npm install; \
		else \
			echo "Node modules already installed."; \
		fi

sqlite: src/api
	@echo "Setting up the database..."
	@if [ ! -f "src/api/instance/db.sqlite" ]; then \
			echo "Creating database..."; \
			cd src/api && ../../.venv/bin/flask db upgrade; \
		else \
			echo "Database already exists."; \
		fi

# Build Docker
slides: $(CONTAINERFILE) $(TEX_BASE)/
	docker build --output type=local,dest=$(TEX_BASE)/$(PDF_NAME) --target pdf -f $(Containerfile) $(TEX_BASE)
	@echo "Document $(PDF_NAME) built successfully."

# Run locally
run-local: compose.yaml src/api src/web
	@echo "Running the project locally..."
	docker compose up --build -d

# Run dockerless
run-standalone:
	@echo "Running the project standalone..."
	nohup python -m http.server 80 -d src/web &
	cd src/api && nohup flask run --port 5000 --host 0.0.0.0 &
	@echo "Project running with web on :80 and api on :5000."
