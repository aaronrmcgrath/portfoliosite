package handlers

import (
	"net/http"

	"github.com/aaronmcgrath/website02/internal/templates"
)

// PageData holds data passed to templates
type PageData struct {
	Title string
}

// Index serves the main page
func Index(w http.ResponseWriter, r *http.Request) {
	data := PageData{
		Title: "Aaron McGrath - Portfolio",
	}
	if err := templates.Render(w, "index.html", data); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// About serves the about section partial (for HTMX)
func About(w http.ResponseWriter, r *http.Request) {
	if err := templates.RenderPartial(w, "about.html", nil); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// Resume serves the resume section partial (for HTMX)
func Resume(w http.ResponseWriter, r *http.Request) {
	if err := templates.RenderPartial(w, "resume.html", nil); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// Projects serves the projects section partial (for HTMX)
func Projects(w http.ResponseWriter, r *http.Request) {
	if err := templates.RenderPartial(w, "projects.html", nil); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
