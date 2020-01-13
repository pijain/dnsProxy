# dnsProxy
DNS proxy server that listens to conventional DNS and sends it over TLS 

## Implementation
Starts a TCP server on port number 6565 and proxies it to cloudflare DNS server over TLS
Used Following for reference:
- https://docs.python.org/3/library/socketserver.html
- https://docs.python.org/3/library/socket.html

## Security Concerns before go live for production
In traditional DNS requests are generally sent as UDP packets, where we might have failures with the order of the packets.
Also the same is being transferred as plain request over the web where one can sniff the packet and pretend as the DNS server, resulting in data exposure.

## Possible Improvements

- Single DNS values are hardcoded, for practical usage to deploy on production, we can leverage advantage of configuration files to provide multiple DNS servers for redundancy.
- Only listens on TCP, we can make it listen on both TCP/UDP
- Can implement instrumentation to get the metrics monitor Hit/Miss ration for monitoring purposes.
- Currently it servers as single thread, we can use socketserver's ThreadingMixIn and run it as threaded application to support multiple requests at the same time.

## Installation

- Build docker image
  ```docker build -t dns-proxy .```
- Start container using the image
  ```docker run -it -p6565:6565 dns-proxy```
- Send DNS query 
  ```dig @127.0.0.1 -p 6565 google.com +tcp```

