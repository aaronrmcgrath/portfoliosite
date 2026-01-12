.PHONY: run build css css-watch clean

# Run the development server
run:
	go run cmd/server/main.go

# Build production binary
build:
	go build -o bin/server cmd/server/main.go

# Compile TailwindCSS
css:
	npx @tailwindcss/cli -i input.css -o static/css/output.css --minify

# Watch and compile TailwindCSS on changes
css-watch:
	npx @tailwindcss/cli -i input.css -o static/css/output.css --watch

# Fetch Go dependencies
deps:
	go mod tidy

# Clean build artifacts
clean:
	rm -rf bin/

# Development: run CSS watcher and server (requires 2 terminals or use &)
dev:
	@echo "Run 'make css-watch' in one terminal and 'make run' in another"
