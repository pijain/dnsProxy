import socketserver
import ssl
import socket
import logging, sys

FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s - %(funcName)20s() — %(message)s")
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(FORMATTER)
logger = logging.getLogger('DNS PROXY')
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.propagate = False


class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """
        Function to handle tcp request and query DNS Over TLS to get the response
        self.request is the TCP socket connected to the client
        :return: Resolved DNS query from TLS Encrypted server
        """
        logger.debug("In TCP RequestHandler class")
        data = self.request.recv(1024).strip()
        logger.debug("Request received : {request}".format(request=data))
        upstream_response = dns_over_tls_query(data, "1.0.0.1", 853, "cloudflare-dns.com")
        logger.debug("Response from upstream DNS Server: {response}".format(response=upstream_response))
        self.request.sendall(upstream_response)


def dns_over_tls_query(request, host, port, hostname):
    """
    Function to query upstream DNS server
    :param request: DNS request to resolve
    :param host: DNS server host to send data
    :param port: DNS server port to send data
    :param hostname: DNS server hostname on which request will be sent
    :return: Resolved dns response from upstream DNS server
    """
    logger.debug("Request received by Resolver: {request}".format(request=request))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = ""
    conn = ssl.wrap_socket(s)
    conn.connect((host, port))
    conn.sendall(request)
    response = conn.recv(1024)
    return response


if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 6565
    with socketserver.TCPServer((HOST, PORT), TCPRequestHandler) as server:
        server.serve_forever()
