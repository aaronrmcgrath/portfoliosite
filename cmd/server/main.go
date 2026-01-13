package main

import (
	"log"
	"net/http"
	"os"

	"github.com/aaronmcgrath/website02/internal/handlers"
	"github.com/aaronmcgrath/website02/internal/templates"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func main() {
	// Initialize templates
	if err := templates.Load(); err != nil {
		log.Fatalf("Failed to load templates: %v", err)
	}

	// Create router
	r := chi.NewRouter()

	// Middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	// Static files
	fileServer := http.FileServer(http.Dir("static"))
	r.Handle("/static/*", http.StripPrefix("/static/", fileServer))

	// Routes
	r.Get("/", handlers.Index)
	r.Get("/partials/about", handlers.About)
	r.Get("/partials/projects", handlers.Projects)
	// r.Get("/partials/blog", handlers.Blog) // Blog hidden for now - uncomment when ready
	r.Get("/partials/resume", handlers.Resume)

	// Get port from environment or default to 3000
	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	log.Printf("Server starting on http://localhost:%s", port)
	if err := http.ListenAndServe(":"+port, r); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
