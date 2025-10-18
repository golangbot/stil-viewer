package main

import (
	"log/slog"
	"mime"
	"net"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/golangbot/stl-viewer/openscadmodel"
	"github.com/gorilla/mux"
)

func main() {
	webServer()
}

type sphereHandler struct {
}

func webServer() {
	// openScadModel := openscadmodel.OpenScadModel{Name: "cylinderhole", File: "cylinderhole"}
	// if _, err := openScadModel.GenerateStl(); err != nil {
	// 	slog.Error("unable to generate stl file", "error", err)
	// 	os.Exit(1)
	// }

	r := mux.NewRouter()
	mime.AddExtensionType(".xml", "text/xml; charset=utf-8")
	sphereHandler := sphereHandler{}

	r.HandleFunc("/sphere", sphereHandler.processUserInput).Methods("POST")
	r.PathPrefix("/").Handler(http.FileServer(http.Dir("static-assets")))

	srv := &http.Server{
		Handler:      r,
		Addr:         "0.0.0.0:6001",
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}
	_, port, err := net.SplitHostPort(srv.Addr)
	if err != nil {
		slog.Error("unable to find port no")
		os.Exit(1)
	}
	slog.Info("Web server started", "port", port)

	if err := srv.ListenAndServe(); err != nil {
		slog.Error("unable to start web server", "error", err)
		os.Exit(1)
	}
}

func (u sphereHandler) processUserInput(w http.ResponseWriter, r *http.Request) {
	slog.Info("Processing user input for sphere radius")
	if err := r.ParseForm(); err != nil {
		slog.Error("unable to parse job submission form", "error", err)
		http.Error(w, "unable to create job post, please try again", http.StatusInternalServerError)
		return
	}
	userInput := r.Form.Get("userinput")
	if userInput == "" {
		slog.Error("userinput is empty")
		http.Error(w, "Please fill user input", http.StatusBadRequest)
	}

	radius, err := openscadmodel.CallOpenAI(r.Context(), userInput)
	if err != nil {
		slog.Error("unable to process user input", "error", err)
		http.Error(w, "unable to process user input, please try again", http.StatusInternalServerError)
		return
	}
	slog.Info("radius from openAI", "radius", radius)
	_, err = strconv.ParseFloat(radius, 64)
	if err != nil {
		slog.Error("invalid radius", "radius", radius)
		http.Error(w, "invalid radius from user input, please try again", http.StatusBadRequest)
		return
	}
	openScadModel := openscadmodel.OpenScadModel{Name: "cylinderhole", File: "cylinderhole"}
	if _, err := openScadModel.GenerateStl(radius); err != nil {
		slog.Error("unable to generate stl file", "error", err)
		os.Exit(1)
	}
	http.Redirect(w, r, "/", http.StatusSeeOther)
}
