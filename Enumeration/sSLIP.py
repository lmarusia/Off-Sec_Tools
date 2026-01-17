#Imports
import sys, argparse
import requests
import ssl, certifi, socket
from datetime import datetime
import pyfiglet

   
#Function to retrieve IP geo-location info via IP API
def ip_trace(source):

    API_URL = "http://ip-api.com/json/" #Identifies the API endpoint
   
    url = API_URL + source
    try:
        response = requests.get(url, timeout=10) #Performs Request
        data = response.json()

        #If Statement to check for errors
        if data.get("status") != "success":
            print(f"[!] Lookup failed: {data.get('message', 'Unknown error')}")
        
        #Display Results
        print(f"IP Trace for: {source}")
        print("-" * 24)
        print(f"IP Address:   {data.get('query', 'N/A')}")
        print(f"Country:      {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})")
        print(f"Region:       {data.get('regionName', 'N/A')}")
        print(f"City:         {data.get('city', 'N/A')}")
        print(f"ZIP Code:     {data.get('zip', 'N/A')}")
        print(f"ISP:          {data.get('isp', 'N/A')}")
        print(f"Organization: {data.get('org', 'N/A')}")
        print(f"AS Number:    {data.get('as', 'N/A')}")
        print(f"Latitude:     {data.get('lat', 'N/A')}")
        print(f"Longitude:    {data.get('lon', 'N/A')}")
        print(f"Timezone:     {data.get('timezone', 'N/A')}")
        print(f"Reverse DNS:  {data.get('reverse', 'N/A')}")
        print("*" * 24) #Border

    #Catches Request based Errors
    except requests.exceptions.RequestException as e:
        print(f"[!] Request error: {e}")
        return {"status": "fail", "message": f"Request error: {e}"}
    #Catch All
    except Exception as e:
        return {"status": "fail", "message": f"request error: {e}"}

#Function to retrieve SSL Certificate Information
def ssl_cert(target, port=443):
    #Retreives SSL Cert via certifi
    context = ssl.create_default_context(cafile=certifi.where())

    with socket.create_connection((target, port)) as sock:
        with context.wrap_socket(sock, server_hostname=target) as ssock:
            cert = ssock.getpeercert()

    expires = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
    days_left = (expires - datetime.now()).days

    issuer = dict(x[0] for x in cert['issuer'])

    print(f"Domain: {target}")
    print(f"Issuer: {issuer.get('organizationName', 'Unknown')}")
    print(f"Valid until: {expires}")
    print(f"Days remaining: {days_left}")


#Main Function
def main():

    #Displays Title of App
    title = pyfiglet.figlet_format("sSLIP", font = "slant") 
    print(title)

    parser = argparse.ArgumentParser(
        description="sSLIP Intelligence Tool — perform IP trace and SSL cert lookup."
    )

    # Define mutually exclusive group to prevent conflict
    group = parser.add_mutually_exclusive_group(required=True)

    #Defines Arguments
    group.add_argument("-t", "--trace", metavar="IP", help="Perform an IP trace (geolocation lookup)")
    group.add_argument("-s", "--ssl", metavar="DOMAIN", help="Retrieve SSL certificate info for a domain")

    args = parser.parse_args() #Parses

    #Determines Function Call based on argument 
    try:
        if args.trace:
            ip_trace(args.trace)
        elif args.ssl:
            ssl_cert(args.ssl)
        else:
            parser.print_help()

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()