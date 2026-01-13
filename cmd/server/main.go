package main

import (
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/aaronmcgrath/website02/internal/handlers"
	"github.com/aaronmcgrath/website02/internal/templates"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

// hostSwitch routes requests based on subdomain
type hostSwitch struct {
	handlers map[string]http.Handler
}

func (hs hostSwitch) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	host := r.Host

	// Strip port if present
	if colonIndex := strings.Index(host, ":"); colonIndex != -1 {
		host = host[:colonIndex]
	}

	// Extract subdomain
	subdomain := ""
	parts := strings.Split(host, ".")

	// Handle various domain patterns:
	// arcade.aaronrmcgrath.com -> arcade
	// arcade.localhost -> arcade (for local testing)
	// localhost -> "" (no subdomain)
	if len(parts) >= 3 {
		subdomain = parts[0]
	} else if len(parts) == 2 && parts[0] == "arcade" {
		// Handle arcade.localhost for local development
		subdomain = "arcade"
	}

	if handler, ok := hs.handlers[subdomain]; ok {
		handler.ServeHTTP(w, r)
		return
	}

	// Default to main handler
	hs.handlers[""].ServeHTTP(w, r)
}

func main() {
	// Initialize templates
	if err := templates.Load(); err != nil {
		log.Fatalf("Failed to load templates: %v", err)
	}

	// Shared static file server
	fileServer := http.FileServer(http.Dir("static"))

	// Create main site router
	mainRouter := chi.NewRouter()
	mainRouter.Use(middleware.Logger)
	mainRouter.Use(middleware.Recoverer)
	mainRouter.Handle("/static/*", http.StripPrefix("/static/", fileServer))
	mainRouter.Get("/", handlers.Index)
	mainRouter.Get("/partials/about", handlers.About)
	mainRouter.Get("/partials/projects", handlers.Projects)
	mainRouter.Get("/partials/resume", handlers.Resume)

	// Create arcade router
	arcadeRouter := chi.NewRouter()
	arcadeRouter.Use(middleware.Logger)
	arcadeRouter.Use(middleware.Recoverer)
	arcadeRouter.Handle("/static/*", http.StripPrefix("/static/", fileServer))
	arcadeRouter.Get("/", handlers.ArcadeIndex)
	arcadeRouter.Get("/games/tennis", handlers.TennisGame)
	arcadeRouter.Get("/games/guessnumber", handlers.GuessNumberGame)

	// Host-based routing
	hostRouter := hostSwitch{
		handlers: map[string]http.Handler{
			"arcade": arcadeRouter,
			"":       mainRouter,
		},
	}

	// Get port from environment or default to 3000
	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	log.Printf("Server starting on http://localhost:%s", port)
	log.Printf("Arcade available at http://arcade.localhost:%s", port)
	if err := http.ListenAndServe(":"+port, hostRouter); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
