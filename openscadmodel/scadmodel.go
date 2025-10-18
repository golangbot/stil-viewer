package openscadmodel

import (
	"fmt"
	"os"
	"os/exec"
)

type OpenScadModel struct {
	Name string
	File string
}

func (s OpenScadModel) GenerateStl(cubeLength string) (string, error) {
	app := "openscad"
	arg0 := "-o"
	arg1 := "outputs/" + s.Name + ".stl"
	arg2 := "models/" + s.File
	arg3 := "-D"
	arg4 := "cube_length=" + cubeLength // Your desired cube length value

	cmd := exec.Command(app, arg0, arg1, arg2, arg3, arg4)
	cmd.Stderr = os.Stderr
	stdout, err := cmd.Output()

	if err != nil {
		fmt.Println(err.Error())
		return "", err
	}
	return string(stdout), nil
}
