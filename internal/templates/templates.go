package templates

import (
	"html/template"
	"io"
	"path/filepath"
)

var templates *template.Template

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
