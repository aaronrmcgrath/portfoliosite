package handlers

import (
	"net/http"

	"github.com/aaronmcgrath/website02/internal/templates"
)

// ArcadePageData holds data for arcade templates
type ArcadePageData struct {
	Title string
}

// ArcadeIndex serves the arcade landing page
func ArcadeIndex(w http.ResponseWriter, r *http.Request) {
	data := ArcadePageData{
		Title: "Game Select",
	}
	if err := templates.RenderArcade(w, "index.html", data); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// TennisGame serves the tennis/pong game page
func TennisGame(w http.ResponseWriter, r *http.Request) {
	data := ArcadePageData{
		Title: "Classic Tennis",
	}
	if err := templates.RenderArcade(w, "tennis.html", data); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// GuessNumberGame serves the guess my number game page
func GuessNumberGame(w http.ResponseWriter, r *http.Request) {
	data := ArcadePageData{
		Title: "Guess My Number",
	}
	if err := templates.RenderArcade(w, "guessnumber.html", data); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
