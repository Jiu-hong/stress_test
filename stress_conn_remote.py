import tomlkit
import concurrent.futures
import subprocess
import argparse

COUNT = 10

def create_tomls(index,node_ip_address):
    # Load a TOML file
    with open('config-sidecar-original.toml', 'r') as f:
        config = tomlkit.load(f)

    config['rpc_server']['main_server']['port'] = 7100 + index
    config['rpc_server']['speculative_exec_server']['port'] = 6000 + index
    config['rpc_server']['node_client']['ip_address'] = node_ip_address
    config['rpc_server']['speculative_exec_server']['port'] = 6000 + index
    config['sse_server']['event_stream_server']['port'] = 19000 + index
    config['sse_server']['connections'][0]['ip_address'] =node_ip_address
    config['rest_api_server']['port'] = 18000 + index
    config['admin_api_server']['port'] = 17000 + index
    with open(f'config-sidecar-{index}.toml', 'w') as f:
        tomlkit.dump(config, f)
    return 7100 + index


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('node_ip_address', type=str)
    args = parser.parse_args()

    # creating process to deploy transfer
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL

        transfer = {executor.submit(
            start_sidecar, x, args.node_ip_address,): x for x in range(COUNT)}
        for future in concurrent.futures.as_completed(transfer):
            url = transfer[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))


if __name__ == "__main__":
    _main()
