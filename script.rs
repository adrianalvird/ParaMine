extern crate reqwest;

use std::env;
use std::fs::File;
use std::io::{self, Read, Write};

fn fetch_subdomain_data(subdomain: &str, output_file: Option<&str>, silent: bool) {
    let wayback_api_url = "https://web.archive.org/cdx/search/cdx";
    let url = format!("{}/*", subdomain);
    
    let client = reqwest::blocking::Client::new();
    let mut response = client.get(wayback_api_url).query(&[("url", &url), ("output", "json")]).send().expect("Request failed");
    
    let mut content = String::new();
    response.read_to_string(&mut content).expect("Failed to read response content");
    
    let data: Vec<Vec<String>> = serde_json::from_str(&content).expect("Failed to parse JSON");
    
    if !silent {
        for entry in &data {
            println!("{}", entry[2]);
        }
    }
    
    if let Some(file) = output_file {
        let mut file = File::create(file).expect("Failed to create output file");
        for entry in &data {
            file.write_all(entry[2].as_bytes()).expect("Failed to write to output file");
            file.write_all(b"\n").expect("Failed to write to output file");
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: {} <subdomain or -f filename> [-o output-file] [--silent]", args[0]);
        std::process::exit(1);
    }
    
    let mut subdomains: Vec<String> = Vec::new();
    let mut output_file: Option<String> = None;
    let mut silent: bool = false;
    
    let mut iter = args.iter().skip(1);
    
    while let Some(arg) = iter.next() {
        match arg.as_str() {
            "-o" => output_file = iter.next().cloned(),
            "--silent" => silent = true,
            "-f" => {
                if let Some(file) = iter.next() {
                    let file_contents = std::fs::read_to_string(file).expect("Failed to read subdomains file");
                    for line in file_contents.lines() {
                        subdomains.push(line.to_string());
                    }
                } else {
                    eprintln!("Usage: {} <subdomain or -f filename> [-o output-file] [--silent]", args[0]);
                    std::process::exit(1);
                }
            }
            _ => subdomains.push(arg.to_string()),
        }
    }
    
    for subdomain in subdomains {
        fetch_subdomain_data(&subdomain, output_file.as_deref(), silent);
    }
}

