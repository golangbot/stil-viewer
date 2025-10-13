package main

import (
	"log/slog"
	"mime"
	"net"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
)

func main() {
	webServer()
}

func webServer() {
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
