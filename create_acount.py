import subprocess


def create_target_account(x):
    keygen_command = construct_command_keygen(x)[0]
    result = subprocess.run(keygen_command,
                            capture_output=True)
    print(result.returncode)
    print(result.stdout.decode("utf-8"))
    print(result.stderr.decode("utf-8"))


def construct_command_keygen(x):
    args_list = \
        ["./casper-client", "keygen", "-f", f'key{x}'],
    return args_list
