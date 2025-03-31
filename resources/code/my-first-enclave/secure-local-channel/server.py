# // Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# // SPDX-License-Identifier: MIT-0
import argparse
import socket
import sys
import json
import urllib.request

# Running server you have pass port the server  will listen to. For Example:
# $ python3 /app/server.py server 5005
class VsockListener:
    # Server
    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog

    def bind(self, port):
        # Bind and listen for connections on the specified port
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.bind((socket.VMADDR_CID_ANY, port))
        self.sock.listen(self.conn_backlog)

    def recv_data(self):
        # Receive data from a remote endpoint
        while True:
            try:
                print("Let's accept stuff")
                (from_client, (remote_cid, remote_port)) = self.sock.accept()
                print("Connection from " + str(from_client) + str(remote_cid) + str(remote_port))
                
                query = from_client.recv(1024).decode()
                print("Message received: " + query)
                
                # Call the external URL
                # for our scenario we will download list of published ip ranges and return list of S3 ranges for porvided region.
                response = get_s3_ip_by_region(query)
                
                # Send back the response                 
                from_client.send(str(response).encode())
    
                from_client.close()
                print("Client call closed")
            except Exception as ex:
                print(ex)

def server_handler(args):
    server = VsockListener()
    server.bind(args.port)
    print("Started listening to port : ",str(args.port))
    server.recv_data()

# Get list of current ip ranges for the S3 service for a region.
# Learn more here: https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html#aws-ip-download 
def get_s3_ip_by_region(region):
    
    # full_query = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
    url = 'https://pro-openapi.debank.com/v1/user/total_balance?id=0xFa214723917091b78a0624d0953Ec1BD35F723DC';

    # url = "https://example.com/total_balance?id=0x1234567890abcdef"  # Replace with your actual URL and wallet ID

    headers = {
        'Accept': 'application/json',
        'AccessKey': 'fad0656e445fa7a1f06abc9e0330a82e36705678'
    }

    req = urllib.request.Request(url, headers=headers, method='GET')

    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise Exception(f"HTTP Error {response.status}")
            data = json.loads(response.read().decode('utf-8'))
            print("Response:>>",data)
            return data
    except Exception as e:
        print("get_total_balance error:", e)
        return None


def main():
    parser = argparse.ArgumentParser(prog='vsock-sample')
    parser.add_argument("--version", action="version",
                        help="Prints version information.",
                        version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(title="options")

    server_parser = subparsers.add_parser("server", description="Server",
                                          help="Listen on a given port.")
    server_parser.add_argument("port", type=int, help="The local port to listen on.")
    server_parser.set_defaults(func=server_handler)
    
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
