import subprocess
import concurrent.futures
from list_ec2 import list_running_ec2
from random import randrange
from create_acount import create_target_account
from datetime import datetime

COUNT = 10000


# send large files to local sidecars

def choose_node(running_ec2s):
    chosen_node = randrange(len(running_ec2s))
    print("chosen node - ", running_ec2s[chosen_node])
    return running_ec2s[chosen_node]


def myfunc(running_ec2s, x):
    try:
        # choose random ip
        node_ip = choose_node(running_ec2s)
        print(node_ip)
        # transfer to target
        send_large_file_command = construct_command_send_large_file(
            node_ip)
        result = subprocess.run(send_large_file_command,
                                capture_output=True)
        print(result.returncode)
        print(result.stdout.decode("utf-8"))
        print(result.stderr.decode("utf-8"))
    except Exception as err:
        print(err)


def construct_command_send_large_file(node_ip):
    args_list = \
        ["./casper-client", "put-transaction", "session",
            "--chain-name", "casper-test-jh-1",
            "-n", f"http://{node_ip}/rpc",
            "--transaction-path", "/home/ubuntu/my_large_file_5M",
            "--secret-key", "faucet_secret_key.pem",
            "--payment-amount", "500000000000",
            "--gas-price-tolerance", "2",
            # "--install-upgrade",
            "--standard-payment", "true",
            "--pricing-mode", "classic"],
    return args_list[0]


def _main():
    print(f"start time: {datetime.now(tz=None)}")
    running_ec2s = ["localhost:7100","localhost:7101","localhost:7102","localhost:7103",
                    "localhost:7104","localhost:7105","localhost:7106"]
    # creating process to deploy transfer
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL

        transfer = {executor.submit(
            myfunc, running_ec2s, x): x for x in range(COUNT)}
        for future in concurrent.futures.as_completed(transfer):
            url = transfer[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
                
    print(f"stop time: {datetime.now(tz=None)}")
if __name__ == "__main__":
    _main()
