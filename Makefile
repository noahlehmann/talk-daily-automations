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

all: setup slides
setup: venv git

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
    	else \
    		echo "Virtual environment already exists."; \
    	fi

sqlite: .venv/bin/flask # todo!
	@echo "Setting up the database..."
	@if [ ! -f "src/api/instance/db.sqlite" ]; then \
			echo "Creating database..."; \
			.venv/bin/flask migrate; \
		else \
			echo "Database already exists."; \
		fi

# Build Docker
slides: $(CONTAINERFILE) $(TEX_BASE)/
	docker build --output type=local,dest=$(TEX_BASE)/$(PDF_NAME) --target pdf -f $(Containerfile) $(TEX_BASE)
	@echo "Document $(PDF_NAME) built successfully."
