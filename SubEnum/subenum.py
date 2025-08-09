import argparse, dns.resolver as resolve, pyfiglet, time

subList = ""
output = ""


def subenum(site):
   record = 'A'
   found = []
   subs = []
   x = 0

   for i in range(10):
        print("Loading" + "." * i, end="\r")
        time.sleep(0.18)

   if subList == "none":
       subs = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'webdisk','pop', 'cpanel', 'blog', 'test', 'forum', 'admin', 'beta', 'dev', 'support', 'shop', 'demo', 'portal', 'media', 'images', 'api']
   else:
       with open(subList, 'r') as file:
        for line in file:
            subs.append(line.strip())
   resolver = resolve.Resolver()
   for sub in subs:
        url = f"{sub}.{site}"
        try:
            result = resolver.resolve(url, record)
            if result:
              found.append(url)
              x += 1
        except resolve.NXDOMAIN:
            pass
        except:
            pass
   timeTaken = time.process_time() 
   print("Loading complete!")
   time.sleep(0.6)

   if len(found) >= 1:
        print("FOUND")
        print('_' * 14)
        for domain in found:
            print(domain)

        if args.whois:
            print('')
            whoisSearch(args.target)
            print('')
        else:
            pass
    
        print('')
        print(f"{x} Subdomains Found in {timeTaken} Seconds")
       
        if not output == "none":
                with open(output, 'w') as outFile:
                    for domain in found:
                        outFile.write(str(domain) + "\n")
   else:
       print(f"No Subdomains Found For {site}")


def whoisSearch(site):
    try: 
       query = "WHOIS Query Request"
       #whois.whois(site)
       print("WHOIS QUERY")
       print('-' * 14)
       print(str(query))
       return query         
    except Exception as err:
        print("Something Went Wrong... Please Try Again")


title = pyfiglet.figlet_format("SubEnum", font = "doom") 
print(title)
#ArgumentParser object
parser = argparse.ArgumentParser(description='A basic subdomain enumeration tool which searches DNS records to identify active domains from a list of common subdomains')

# Define arguments
parser.add_argument('-t', '--target', help='Target Domain', required=True)
parser.add_argument('-l', '--list', default='none', help='File Containing Subdomains', required=False)
parser.add_argument('-o', '--output', default= 'none', help='File to Output Found Subdomains', required=False)
parser.add_argument('-w', '--whois', action='store_true', help='Whois Query of Target Domain', required=False)

# Parse arguments
args = parser.parse_args()


subList = args.list
output = args.output

subenum(str(args.target))
