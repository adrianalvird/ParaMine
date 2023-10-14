cat subdomains.py | python paramine.py -p
echo "target.com" | python paramine.py -p
python paramine.py -u https://target.com
python paramine.py -f subdomains-file.txt
python paramine.py -f subdomains-file.txt -o putput.txt
python paramine.py -f subdomains-file.txt -o putput.txt --silent 


----------------------------------------------------
RUST


rustc script.rs
./script <subdomain or -f filename> [-o output-file] [--silent]



-------------------------------------------------------
GO


go run script.go <subdomain or -f filename> [-o output-file] [--silent]
go run script.go example.com
go run script.go -f subdomains.txt -o output.txt
go run script.go -f subdomains.txt --silent
cat subdomains.txt | go run script.go -f -o output.txt
cat subdomains.txt | go run script.go -o output.txt

