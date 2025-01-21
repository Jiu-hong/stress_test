import argparse
import threading
import requests
import json
import random


def get_peers(node_ip):
    try:
        # info_get_peers
        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "info_get_peers",
            "params": []
        }

        rpc_result = requests.post(f'http://{node_ip}:7777/rpc', json=payload)

        if rpc_result.status_code == 200:
            return [(peer["address"].split(":")[0])
                    for peer in rpc_result.json()["result"]["peers"]]
        return []

    except Exception as err:
        print(err)


def get_rpc_sse_open():
    try:
        # nodes_list = get_peers("54.201.37.77")
        # url = f'http://{random.choice(nodes_list)}:8888/status'
        url = "http://54.201.37.77:8888/status"

        resp = requests.get(url)
        if resp.status_code == 200:
            print(resp.json())
            print("===")
            print(json.dumps(resp.json()))

    except Exception as err:
        pass


get_rpc_sse_open()
# def _main(args: argparse.Namespace):

#     # Query: get_node_peers.
#     node_peers = client.get_node_peers()

#     active_peers = [x["address"].split(":")[0] for x in node_peers]

#     # creating threads
#     threads_list = [threading.Thread(
#         target=get_rpc_sse_open, args=(peer,)) for peer in active_peers]

#     # starting process 1 - n
#     for thread in threads_list:
#         thread.start()

#     print("\nActive peers with rest port opened.")


# # Entry point.
# if __name__ == "__main__":
#     _main()
