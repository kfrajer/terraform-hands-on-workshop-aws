// REFERENCE: https://www.digitalocean.com/community/tutorials/how-to-make-http-requests-in-go
// https://mocktarget.apigee.net/help

package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
	//"time"
)

const serverPort = 3333

func main() {
	/* ****************************************
	go func() {
		mux := http.NewServeMux()
		mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
			fmt.Printf("server: %s /\n", r.Method)
			fmt.Fprintf(w, `{"message": "Hello!"}`)
		})
		server := http.Server{
			Addr:    fmt.Sprintf(":%d", serverPort),
			Handler: mux,
		}
		if err := server.ListenAndServe(); err != nil {
			if !errors.Is(err, http.ErrServerClosed) {
				fmt.Printf("error running http server: %s\n", err)
			}
		}
	}()

	time.Sleep(100 * time.Millisecond)
	**************************************** */

	var urlUAT string = os.Getenv("ENDPOINTUAT")
	//SAMPLE: export ENDPOINTUAT='https://jeai60f6hc.execute-api.us-west-2.amazonaws.com'
	if urlUAT == "" {
		fmt.Printf("ERROR::Expected url UAT ENDPOINTUAT but found empty\n")
		os.Exit(1)
	}

	//REFERENCE: https://www.honeybadger.io/blog/a-definitive-guide-to-regular-expressions-in-go/
	pattern := regexp.MustCompile("^https://")
	if !pattern.MatchString(urlUAT) {
		fmt.Printf("ERROR::Incorrect format found for ENDPOINTUAT!\n")
		os.Exit(1)
	}

	requestURL := fmt.Sprintf("%s/test/helloworld/", urlUAT)
	//res, err := http.Get(requestURL)
	req, err := http.NewRequest(http.MethodGet, requestURL, nil)
	if err != nil {
		fmt.Printf("client: Could not create request: %s\n", err)
		os.Exit(1)
	}

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Printf("client: error making http request: %s\n", err)
		os.Exit(1)
	}
	fmt.Printf("client: got response!\n")
	fmt.Printf("client: status code: %d\n", res.StatusCode)

	resBody, err := io.ReadAll(res.Body)
	if err != nil {
		fmt.Printf("client: Could not read response body %s\n", err)
		os.Exit(1)
	}
	fmt.Printf("client: Respose body %s\n", resBody)
}
