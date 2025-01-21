from paramiko import SSHClient, AutoAddPolicy

client = SSHClient()
# client.load_system_host_keys()
# client.load_host_keys('/Users/jh/.ssh/known_hosts')
client.set_missing_host_key_policy(AutoAddPolicy())

client.connect('35.94.144.81', username='cladmin',
               key_filename='/Users/jh/.ssh/cladmin_id_ed25519', passphrase='')

sftp_client = client.open_sftp()
localFilePath = "faucet_secret_key.pem"
remoteFilePath = "/etc/casper/faucet/secret_key.pem"

try:
    sftp_client.get(remoteFilePath, localFilePath)
except FileNotFoundError as err:
    print(f"File: {remoteFilePath} was not found on the source server ")

sftp_client.close()
client.close()
