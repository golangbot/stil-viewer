package openscadmodel

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
)

type openAIInput struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type openAIRequest struct {
	Model       string         `json:"model"`
	Temperature float64        `json:"temperature"`
	Input       []openAIInput  `json:"input"`
	Text        map[string]any `json:"text"`
}

type openAPIResponse struct {
	Output []struct {
		Content []struct {
			Type string `json:"type"`
			Text string `json:"text"`
		} `json:"content"`
	} `json:"output"`
}

type functionSchema struct {
	Radius string `json:"radius"`
}

func CallOpenAI(ctx context.Context, userInput string) (string, error) {
	openAIRequest := openAIRequest{
		Model:       "gpt-4o-mini",
		Temperature: 0.1,
		Input: []openAIInput{
			{
				Role: "developer",
				Content: `I have a openscad model function which takes a cube length as parameter. 
				Process the users input and give me the cube length. For example, if the user says 
				I want to draw a cube with length 10, then return 10. Return only the length as I am going to pass this as parameter
				 to the function. If the user follows up and says, change the length to 1. Then return only 1 as the output. 
				 If the length is invalid, return NA`,
			},
			{
				Role:    "user",
				Content: userInput,
			},
		},
		Text: map[string]any{
			"format": map[string]any{
				"type": "json_schema",
				"name": "function_schema",
				"schema": map[string]any{
					"type": "object",
					"properties": map[string]any{
						"radius": map[string]string{"type": "string"},
					},
					"required":             []string{"radius"},
					"additionalProperties": false,
				},
			},
		},
	}

	jsonRequest, err := json.Marshal(openAIRequest)
	if err != nil {
		return "", err
	}

	openAPIRequest, err := http.NewRequestWithContext(ctx, "POST", "https://api.openai.com/v1/responses", bytes.NewReader(jsonRequest))
	if err != nil {
		return "", err
	}
	openAPIRequest.Header.Set("Authorization", "Bearer "+os.Getenv("OPENAI_API_KEY"))
	openAPIRequest.Header.Set("Content-Type", "application/json")
	openAIResponseRaw, err := http.DefaultClient.Do(openAPIRequest)
	if err != nil {
		return "", err
	}
	defer openAIResponseRaw.Body.Close()
	responseBody, err := io.ReadAll(openAIResponseRaw.Body)
	if err != nil {
		return "", err
	}
	if openAIResponseRaw.StatusCode != 200 {
		slog.Error("openAI response code is not 200", "response", string(responseBody))
		return "", fmt.Errorf("openAI response code is not 200")
	}
	var openAIResponse openAPIResponse
	if err := json.Unmarshal(responseBody, &openAIResponse); err != nil {
		return "", err
	}
	if len(openAIResponse.Output) == 0 {
		return "", fmt.Errorf("openAI response is empty")
	}
	output := openAIResponse.Output[0]
	if len(output.Content) == 0 {
		return "", fmt.Errorf("openAI response content is empty")
	}

	var functionData functionSchema
	if err := json.Unmarshal([]byte(output.Content[0].Text), &functionData); err != nil {
		return "", err
	}
	slog.Debug("open ai output", "location", functionData)

	return functionData.Radius, nil
}
