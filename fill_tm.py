import sys
import time

import requests

from utils.arg_parser import get_fill_tm_args
from utils.launch_servers import launch_tm_server, local_tm_server_url


def send_pair(url, uid, language, src, trg):
    result = requests.post(url + "/save",
                           json={'uid': uid, 'language': language, 'source': src, 'target': trg},
                           timeout=60).json()
    sys.stderr.write(f"{src} ||| {trg} ||| status: {result['status']}" + '\n')


def main(args):
    processes = []

    try:
        # Start servers if needed
        if args.tm_server is None:
            processes.append(launch_tm_server(args))
            tm_server_url = local_tm_server_url
        else:
            tm_server_url = args.tm_server

        time.sleep(5)

        for src, trg in zip(args.source, args.target):
            send_pair(tm_server_url, args.uid, args.language, src.strip(), trg.strip())

    finally:
        for proc in processes:
            proc.kill()


if __name__ == "__main__":
    main(get_fill_tm_args())
