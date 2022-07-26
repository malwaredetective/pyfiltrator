# pyfiltrator.py


## Description
A Python script used to covertly exfil files over the network.

```
usage: pyfiltrator.py [-h] [-f <string>] [-d <string>] mode ...

A Python script used to covertly exfil files over the network. This script will stage a file into bite-sized chunks of base64 encoded data, then exfiltrate the file over the network using the protocol of your choosing.

positional arguments:
  mode                  Use <mode> -h to list addtional required and optional arguments for the selected mode
    dns                 Use DNS queries to exfil a file over DNS
    http                Use HTTP GET requests to exfil files over HTTP

options:
  -h, --help            show this help message and exit
```

## Requirements
- Python ≥ 3.0
- Non-standard Python Libraries
  - dnspython
  - requests
  - progress

## Usage
- Download the pyfiltrator repository: `git clone https://github.com/malwaredetective/pyfiltrator.git`
- Install the additional Python packages: `pip install -r requirements.txt`
- Execute **pyfiltrator.py** within your terminal: `python pyfiltrator.py`

## Exfiling a File over DNS
```
usage: pyfiltrator.py dns [-h] -f <string> -d <string> -r <string> [-l <int>]

A Python script used to covertly exfil files over the network. This script will stage a file into bite-sized chunks of base64 encoded data, then use a remote DNS server that's under your control to exfil the file over DNS. The victim
host will exfil the payload by querying subdomains for the domain you specify, using the chunked data as a subdomain.

options:
  -h, --help            show this help message and exit
  -f <string>, --file <string>
                        Specify the path to the target file
  -d <string>, --domain <string>
                        The base URL of the target domain: {example.com}
  -r <string>, --resolver <string>
                        The IP Address of the remote DNS server that will resolve the DNS queries
  -l <int>, --length-of-payload <int>
                        Specify a custom payload length when transmitting the file: {24,48,64,88} (Default: 24)
```

## Exfiling a File over HTTP
```
usage: pyfiltrator.py http [-h] -f <string> -d <string> [-l <int>] [-s]

A Python script used to covertly exfil over the network. This script will stage a file into bite-sized chunks of base64 encoded data, then send HTTP GET requests to a server that's under your control to exfil files over the web. The
victim host will exfil the payload by sending requests to <domain>/index.html?id=<payload>.

options:
  -h, --help            show this help message and exit
  -f <string>, --file <string>
                        Specify the path to the target file
  -d <string>, --domain <string>
                        The base URL of the target domain: {example.com}
  -l <int>, --length-of-payload <int>
                        Specify a custom payload length when transmitting the file: {24,48,64,88} (Default: 24)
  -s, --ssl             Use HTTPS when transfering the file (Default: HTTP)
```
