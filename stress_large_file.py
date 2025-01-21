import subprocess
import concurrent.futures
from list_ec2 import list_running_ec2
from random import randrange
from create_acount import create_target_account

COUNT = 10000


def get_ec2s():
    running_ec2s = list(list_running_ec2().items())
    return running_ec2s


def choose_node(running_ec2s):
    chosen_node = randrange(len(running_ec2s))
    print("chosen node - ", running_ec2s[chosen_node])
    return running_ec2s[chosen_node][1]


def myfunc(running_ec2s, x):
    try:
        # choose random ip
        node_ip = choose_node(running_ec2s)
        # transfer to target
        send_large_file_command = construct_command_send_large_file(
            node_ip)[0]
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
            "--chain-name", "casper-test-jh",
            "-n", f"http://{node_ip}:7777/rpc",
            "--transaction-path", "/home/ubuntu/my_large_file_3M",
            "--secret-key", "faucet_secret_key.pem",
            "--payment-amount", "500000000000",
            "--gas-price-tolerance", "2",
            # "--install-upgrade",
            "--standard-payment", "true",
            "--pricing-mode", "classic"],
    return args_list


def _main():
    running_ec2s = get_ec2s()
    # creating process to deploy transfer
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Start the load operations and mark each future with its URL

        transfer = {executor.submit(
            myfunc, running_ec2s, x): x for x in range(COUNT)}
        for future in concurrent.futures.as_completed(transfer):
            url = transfer[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))


if __name__ == "__main__":
    _main()
