import http.server
import socketserver
import socket

# Multicast IP, multicast port
SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900

# Seconds to delay response
SSDP_MX = 2 

# Search target
SSDP_ST = "urn:dial-multiscreen-org:service:dial:1"


UPNP_SEARCH = 'M-SEARCH * HTTP/1.1'
# If we get a M-SEARCH with no or invalid MX value, wait up
# to this many seconds before responding to prevent flooding
CACHE_DEFAULT = 1800
DELAY_DEFAULT = 10

SSDP_REPLY = 'HTTP/1.1 200 OK\r\n' + \
               'LOCATION: {}\r\n' + \
               'CACHE-CONTROL: max-age={}\r\n' + \
               'EXT:\r\n' + \
               'BOOTID.UPNP.ORG: 1\r\n' + \
               'SERVER: {}/{} UPnP/1.1 {}/{}\r\n' + \
               'ST: {}\r\n'.format(SSDP_ST) + \
               'DATE: {}\r\n' + \
               'USN: {}\r\n' + '\r\n'


class SSDPHandler(BaseHTTPRequestHandler):

     # Reads data from the socket checks for the correct
     # search parameters and UPnP search target, and replies
     # with the application URL that the server advertises.
     def handle(self):
          data = str(self.request[0], 'utf-8')
          data = data.strip().split('\r\n')
          if data[0] != UPNP_SEARCH:
               return
          else:
               dial_search = False
               for line in data[1:]:
                    field, val = line.split(':', 1)
                    if field.strip() == 'ST' and val.strip() == SSDP_ST:
                         dial_search = True
                    elif field.strip() == 'MX':
                         try:
                              self.max_delay = int(val.strip())
                         except ValueError:
                              # Use default
                              pass
               if dial_search:
                    self.sendto(SSDP_REPLY, self.client_address)

def main():
     socketserver.UDPServer.allow_reuse_address = True
     server = socketserver.UDPServer(('', 0), SSDPHandler)
     server.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_pton(socket.AF_INET, SSDP_ADDR) +
                      socket.inet_pton(socket.AF_INET, '0.0.0.0'))
     server.serve_forever()

if __name__ == '__main__':
  main()
     
    
