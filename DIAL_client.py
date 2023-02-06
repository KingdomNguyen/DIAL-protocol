import re
import socket
import requests

# Multicast IP, multicast port
SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900

# Seconds to delay response
SSDP_MX = 2 

# Search target
SSDP_ST = "urn:dial-multiscreen-org:service:dial:1"

# M-search request
SSDP_request = 'M-search * HTTP/1.1\r\n' + \
               'Host:{}:{:d}\r\n'.format(SSDP_ADDR, SSDP_PORT) + \
               'MAN: "ssdp:discover"\r\n' + \
               'MX: {:d}\r\n'.format(SSDP_MX) + \
               'ST: {}\r\n'.format(SSDP_ST) + \
               '\r\n'

# Discover UPNP server.
# Sending the multicast message to find UPNP servers, parsing the URL out of the "location" from HTTP and returing the sets of locations found
def discover_dial():
    locations = set()
    location_regex = re.compile("location:[ ]*(.+)\r\n", re.IGNORECASE)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(SSDP_request.encode("ASCII"), (SSDP_ADDR, SSDP_PORT))
    sock.settimeout(3)
    try:
        while True:
             data, addr = sock.recvfrom(1024)
             location_result = location_regex.search(data.decode("ASCII"))
             if location_result and (location_result.group(1) in locations) == False:
                locations.add(location_result.group(1))
    except socket.error:
        sock.close()

    return locations

# Print response from server
# Printing the content of "Server" from HTTP that reply by the server
def response():
    for location in locations:
        print('Parse %s' % location)
        try:
            resp = requests.get(location, timeout=2)
            if resp.headers.get('SERVER'):
                print('\tServer: %s' %resp.headers.get('SERVER'))
            else:
                print('\tNo server string')
        except 
            print("Fail to print from server")
                  
def main():
    print('Discovering UPnP locations')
    locations = discover_dial()
    print('Discovery complete')
    print('%d locations found:' %len(locations))
    for location in locations:
        print('\t%s' %location)

    response(locations)


if __name__ == "__main__":
    main()
