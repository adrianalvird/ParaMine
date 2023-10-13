package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

const waybackAPIURL = "https://web.archive.org/cdx/search/cdx"

func fetchSubdomainData(subdomain string, output string, silent bool) {
	url := fmt.Sprintf("%s/*", subdomain)
	resp, err := http.Get(waybackAPIURL + "?url=" + url + "&output=json")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to fetch data for subdomain: %s\n", subdomain)
		return
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to read response for subdomain: %s\n", subdomain)
		return
	}

	var data [][]string
	if err := json.Unmarshal(body, &data); err != nil {
		fmt.Fprintf(os.Stderr, "Failed to parse JSON for subdomain: %s\n", subdomain)
		return
	}

	if !silent {
		for _, entry := range data {
			fmt.Println(entry[2])
		}
	}

	if output != "" {
		file, err := os.Create(output)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Failed to create output file: %v\n", err)
			return
		}
		defer file.Close()

		for _, entry := range data {
			fmt.Fprintln(file, entry[2])
		}
	}
}

func main() {
	var subdomains []string
	var output string
	var silent bool

	flag.StringVar(&output, "o", "", "Specify an output file for saving extracted URLs")
	flag.BoolVar(&silent, "silent", false, "Enable silent mode (no output to the terminal)")
	flag.Parse()

	if flag.NArg() == 0 {
		fmt.Fprintln(os.Stderr, "Usage: script.go <subdomain or -f filename> [-o output-file] [--silent]")
		os.Exit(1)
	}

	for _, arg := range flag.Args() {
		if arg == "-f" {
			file := flag.Arg(1)
			fileContents, err := ioutil.ReadFile(file)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Failed to read subdomains file: %v\n", err)
				os.Exit(1)
			}
			lines := []byte(fileContents)
			subdomains = append(subdomains, string(lines))
			break
		}
		subdomains = append(subdomains, arg)
	}

	for _, subdomain := range subdomains {
		fetchSubdomainData(subdomain, output, silent)
	}
}

