package main

import (
	"log/slog"
	"mime"
	"net"
	"net/http"
	"os"
	"time"

	"github.com/golangbot/stl-viewer/openscadmodel"
	"github.com/gorilla/mux"
)

func main() {
	webServer()
}

//	func initializeModels() {
//		openScadModels = []openscadmodel.OpenScadModel{
//			{Name: "cylinderhole", File: "cylinderhole"},
//		}
//	}
func webServer() {
	openScadModel := openscadmodel.OpenScadModel{Name: "cylinderhole", File: "cylinderhole"}
	if _, err := openScadModel.GenerateStl(); err != nil {
		slog.Error("unable to generate stl file", "error", err)
		os.Exit(1)
	}

	r := mux.NewRouter()
	mime.AddExtensionType(".xml", "text/xml; charset=utf-8")

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
