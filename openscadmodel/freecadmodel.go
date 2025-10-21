package openscadmodel

import (
	"log/slog"
	"net"
	"os"
	"strings"

	"github.com/google/uuid"
)

type FreeCadModel struct {
	Name string
	File string
}

func (s FreeCadModel) LoadModelFile() ([]byte, error) {
	model, err := os.ReadFile("/home/naveen/Documents/source-code/free-cad-ai/stl-viewer/freecadmodels/FreeCAD_Console_Testcode_creating_sketch_and_features.py")
	if err != nil {
		return nil, err
	}
	return model, nil
}
func (s FreeCadModel) GenerateStl(champferSize string) (string, error) {
	//strEcho := "print ('Hello World')"
	model, err := s.LoadModelFile()
	if err != nil {
		slog.Error("unable to load freecad model file", "error", err)
		return "", err
	}
	model = []byte(strings.ReplaceAll(string(model), "chamfer.Size = 1.0", "chamfer.Size = "+champferSize))
	stlFileName := uuid.New().String()
	model = []byte(strings.ReplaceAll(string(model), "STL_FILE_NAME", stlFileName))
	servAddr := "localhost:38059"
	tcpAddr, err := net.ResolveTCPAddr("tcp", servAddr)
	if err != nil {
		println("ResolveTCPAddr failed:", err.Error())
		os.Exit(1)
	}

	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		println("Dial failed:", err.Error())
		os.Exit(1)
	}

	_, err = conn.Write([]byte(model))
	if err != nil {
		println("Write to server failed:", err.Error())
		os.Exit(1)
	}

	println("write to server = ", model)

	reply := make([]byte, 1024)

	_, err = conn.Read(reply)
	if err != nil {
		println("Write to server failed:", err.Error())
		os.Exit(1)
	}

	println("reply from server=", string(reply))

	conn.Close()
	return stlFileName, nil
}
