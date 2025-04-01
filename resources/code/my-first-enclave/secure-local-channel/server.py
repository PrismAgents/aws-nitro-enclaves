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
                response = trigger_auction(query)
                
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


def get_on_chain_history(user_address):
    print("User Address:>>",user_address)
    url = `https://pro-openapi.debank.com/v1/user/total_balance?id=${user_address}`;

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

def get_auction_bidders():

def get_active_campaigns():
    try:
        conn = psycopg2.connect(
            host="3.129.1.135",
            port=5432,
            dbname="postgres",
            user="postgres",
            password="123456",
            sslmode="prefer"
        )
        cur = conn.cursor()

        # SQL with placeholder and bound parameter
        query = '''
            SELECT * FROM Campaign
            JOIN CampaignConditions ON Campaign.id = CampaignConditions.campaign_id
            WHERE Campaign.status = %s
        '''
        cur.execute(query, ('active',))  # <-- parameters as tuple

        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Database error:", e)

def trigger_auction(user_address):
    on_chain_history = get_on_chain_history(user_address)
    print("On Chain History:>>",on_chain_history)
    return on_chain_history
    


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
psycopg2