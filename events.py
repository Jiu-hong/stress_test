from sseclient import SSEClient

messages = SSEClient('http://54.201.37.77:9999/events')
for msg in messages:
    print(msg)
