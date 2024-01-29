package main

import (
	"fmt"
	nuclio "github.com/nuclio/nuclio-sdk-go"
	"github.com/valyala/fasthttp"
	"net/url"
	"os"
)

func Handler(context *nuclio.Context, event nuclio.Event) (interface{}, error) {
	context.Logger.Info("Got request, sending it to sidecar container")
	req := fasthttp.AcquireRequest()
	req.SetBody(event.GetBody())
	sidecarHost := os.Getenv("SIDECAR_HOST")
	sidecarPort := os.Getenv("SIDECAR_PORT")
	sidecarHost, _ := url.JoinPath(fmt.Sprintf("%s:%s", sidecarHost, sidecarPort), event.GetPath())
	context.Logger.Info(sidecarHost)
	req.SetRequestURI(sidecarHost)
	resp := fasthttp.AcquireResponse()
	err := fasthttp.Do(req, resp)
	return nuclio.Response{
		StatusCode:  resp.StatusCode(),
		ContentType: "application/text",
		Body:        resp.Body(),
	}, err
}
