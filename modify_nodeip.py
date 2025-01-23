import tomlkit,argparse

parser = argparse.ArgumentParser()
parser.add_argument('node_ip_address', type=str)
args = parser.parse_args()
    
with open('config-sidecar.toml', 'r') as f:
    config = tomlkit.load(f)


config['rpc_server']['node_client']['ip_address'] = args.node_ip_address
config['sse_server']['connections'][0]['ip_address'] = args.node_ip_address

with open('config-sidecar.toml', 'w') as f:
    tomlkit.dump(config, f)
