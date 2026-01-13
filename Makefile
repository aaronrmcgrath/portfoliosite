# =============================================================================
# Aaron McGrath Portfolio & Arcade - Development Makefile
# =============================================================================
#
# QUICK START:
#   make install    # Install all dependencies (Go + Node)
#   make dev        # Start development (CSS watcher + server)
#
# COMMON COMMANDS:
#   make run        # Run the Go server only
#   make css        # Compile Tailwind CSS once
#   make css-watch  # Watch and auto-compile CSS on changes
#   make build      # Build production binary
#   make clean      # Remove build artifacts
#
# URLS:
#   Main site:  http://localhost:3000
#   Arcade:     http://arcade.localhost:3000
#
# =============================================================================

.PHONY: help install deps run build css css-watch clean dev dev-css dev-server

# Default target - show help
help:
	@echo ""
	@echo "Available commands:"
	@echo "  make install     - Install Go and Node dependencies"
	@echo "  make run         - Run the development server"
	@echo "  make build       - Build production binary to bin/server"
	@echo "  make css         - Compile Tailwind CSS (minified)"
	@echo "  make css-watch   - Watch and compile CSS on changes"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make dev         - Run CSS watcher and server (requires 2 terminals)"
	@echo ""
	@echo "URLs:"
	@echo "  Main site:  http://localhost:3000"
	@echo "  Arcade:     http://arcade.localhost:3000"
	@echo ""

# =============================================================================
# SETUP & DEPENDENCIES
# =============================================================================

# Install all dependencies (Go modules + Node packages for Tailwind)
install: deps
	@echo "Installing Node dependencies for Tailwind CSS..."
	npm install
	@echo ""
	@echo "All dependencies installed!"

# Fetch and tidy Go module dependencies
deps:
	@echo "Tidying Go modules..."
	go mod tidy

# =============================================================================
# DEVELOPMENT
# =============================================================================

# Run the development server
# Access main site at http://localhost:3000
# Access arcade at http://arcade.localhost:3000
run:
	@echo "Starting server..."
	@echo "  Main site: http://localhost:3000"
	@echo "  Arcade:    http://arcade.localhost:3000"
	@echo ""
	go run cmd/server/main.go

# Compile Tailwind CSS once (minified for production)
css:
	@echo "Compiling Tailwind CSS..."
	npx @tailwindcss/cli -i input.css -o static/css/output.css --minify
	@echo "Done! Output: static/css/output.css"

# Watch for CSS changes and recompile automatically
# Use this during development alongside 'make run'
css-watch:
	@echo "Watching for CSS changes..."
	@echo "Press Ctrl+C to stop"
	npx @tailwindcss/cli -i input.css -o static/css/output.css --watch

# Development helper - prints instructions for running both services
dev:
	@echo ""
	@echo "=== DEVELOPMENT MODE ==="
	@echo ""
	@echo "Run these commands in separate terminals:"
	@echo ""
	@echo "  Terminal 1 (CSS watcher):"
	@echo "    make css-watch"
	@echo ""
	@echo "  Terminal 2 (Server):"
	@echo "    make run"
	@echo ""
	@echo "Or use these shortcuts:"
	@echo "  make dev-css     # Start CSS watcher"
	@echo "  make dev-server  # Start server"
	@echo ""

# Shortcut aliases for dev workflow
dev-css: css-watch
dev-server: run

# =============================================================================
# BUILD & PRODUCTION
# =============================================================================

# Build production binary
build: css
	@echo "Building production binary..."
	@mkdir -p bin
	go build -o bin/server cmd/server/main.go
	@echo "Done! Binary: bin/server"
	@echo ""
	@echo "To run: ./bin/server"

# =============================================================================
# CLEANUP
# =============================================================================

# Remove build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf bin/
	@echo "Done!"
