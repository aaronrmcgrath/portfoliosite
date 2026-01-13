package templates

import (
	"fmt"
	"html/template"
	"io"
	"path/filepath"
)

var templates *template.Template

// arcadeTemplateMap holds separate template instances for each arcade page
// This is necessary because each page defines "arcade-content" and they would
// overwrite each other if parsed into a single template set
var arcadeTemplateMap map[string]*template.Template

// Load parses all templates from the templates directory
func Load() error {
	var err error
	templates, err = template.ParseGlob(filepath.Join("templates", "*.html"))
	if err != nil {
		return err
	}

	// Parse partials
	templates, err = templates.ParseGlob(filepath.Join("templates", "partials", "*.html"))
	if err != nil {
		return err
	}

	// Load arcade templates - each page needs its own template instance
	// because they all define "arcade-content" which would conflict
	arcadeTemplateMap = make(map[string]*template.Template)

	// Get base template path
	basePath := filepath.Join("templates", "arcade", "base.html")

	// Load index page (base + index)
	indexTmpl, err := template.ParseFiles(basePath, filepath.Join("templates", "arcade", "index.html"))
	if err != nil {
		return fmt.Errorf("failed to load arcade index: %w", err)
	}
	arcadeTemplateMap["index.html"] = indexTmpl

	// Load each game template (base + game)
	gameFiles, err := filepath.Glob(filepath.Join("templates", "arcade", "games", "*.html"))
	if err != nil {
		return fmt.Errorf("failed to glob game templates: %w", err)
	}

	for _, gameFile := range gameFiles {
		gameTmpl, err := template.ParseFiles(basePath, gameFile)
		if err != nil {
			return fmt.Errorf("failed to load game template %s: %w", gameFile, err)
		}
		// Use just the filename as the key
		name := filepath.Base(gameFile)
		arcadeTemplateMap[name] = gameTmpl
	}

	return nil
}

// Render executes a template by name and writes to the writer
func Render(w io.Writer, name string, data any) error {
	return templates.ExecuteTemplate(w, name, data)
}

// RenderPartial renders a partial template (for HTMX responses)
func RenderPartial(w io.Writer, name string, data any) error {
	return templates.ExecuteTemplate(w, name, data)
}

// RenderArcade renders an arcade template
func RenderArcade(w io.Writer, name string, data any) error {
	tmpl, ok := arcadeTemplateMap[name]
	if !ok {
		return fmt.Errorf("arcade template not found: %s", name)
	}
	// Execute the base template which will pull in the page's arcade-content
	return tmpl.ExecuteTemplate(w, "arcade-base", data)
}
