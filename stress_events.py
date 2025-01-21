from sseclient import SSEClient
import threading


def myfunc():
    messages = SSEClient('http://54.201.37.77:19999/events')
    for msg in messages:
        print(msg)


def _main():

    # creating process
    threads_list = [threading.Thread(target=myfunc) for _ in range(98)]

    # starting process 1 - n
    for thread in threads_list:
        thread.start()

    print("\nActive sse")


if __name__ == "__main__":
    _main()
