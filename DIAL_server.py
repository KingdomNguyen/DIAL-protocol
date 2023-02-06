import socketserver
import socket
import struct
import time
import platform
import random
import uuid

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


class SSDPHandler(socketserver.BaseRequestHandler):

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

class SSDPServer(socketserver.UDPServer):

     def __init__(self, device_url, host=''):
          socketserver.UDPServer.__init__(self, (host, SSDP_PORT), 
                    SSDPHandler, False)
          self.allow_reuse_address = True
          self.server_bind()
          mreq = struct.pack("=4sl", socket.inet_aton(SSDP_ADDR),
                                       socket.INADDR_ANY)
          self.socket.setsockopt(socket.IPPROTO_IP, 
                    socket.IP_ADD_MEMBERSHIP, mreq)

     def start(self):
          self.serve_forever()

class DialServer(object):
     def __init__(self):
          pass

     def add_app(self, app_id, app_path):
          pass
    
