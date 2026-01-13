# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Install Node.js for Tailwind
RUN apk add --no-cache nodejs npm

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy package files and install npm deps
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code
COPY . .

# Build Tailwind CSS
RUN npx @tailwindcss/cli -i input.css -o static/css/output.css --minify

# Build Go binary
RUN CGO_ENABLED=0 GOOS=linux go build -o server cmd/server/main.go

# Runtime stage
FROM alpine:latest

WORKDIR /app

# Copy binary and assets
COPY --from=builder /app/server .
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/static ./static

EXPOSE 8080

CMD ["./server"]
