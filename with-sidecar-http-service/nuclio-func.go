package main

import (
	"fmt"
	"net/url"
	"os"

	nuclio "github.com/nuclio/nuclio-sdk-go"
	"github.com/valyala/fasthttp"
)

func Handler(context *nuclio.Context, event nuclio.Event) (interface{}, error) {
	sidecarHost := os.Getenv("SIDECAR_HOST")
	sidecarPort := os.Getenv("SIDECAR_PORT")
	// url for request forwarding
	sidecarUrl, _ := url.JoinPath(fmt.Sprintf("%s:%s", sidecarHost, sidecarPort), event.GetPath())

	// create new request to forward
	req := fasthttp.AcquireRequest()
	resp := fasthttp.AcquireResponse()

	// set body and request uri
	req.SetBody(event.GetBody())
	req.SetRequestURI(sidecarUrl)

	// sending request to sidecar
	context.Logger.InfoWith("Forwarding request to sidecar", "sidecarUrl", sidecarUrl)
	err := fasthttp.Do(req, resp)

	return nuclio.Response{
		StatusCode:  resp.StatusCode(),
		ContentType: "application/text",
		Body:        resp.Body(),
	}, err
}
