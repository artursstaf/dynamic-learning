import json
import sys
import time

import requests
from websocket import create_connection

from utils.arg_parser import get_translate_args
from utils.launch_servers import launch_tm_server, local_tm_server_url, launch_marian_server, local_marian_server_url


def translate(url, line, context):
    ws = create_connection(url + '/translate')
    ws.send(json.dumps({'input': line, 'context': [context]}))
    result = ws.recv()
    ws.close()
    result_json = json.loads(result.strip())
    return result_json['output']


def get_context(url, line, uid, language):
    result = requests.post(url + "/retrieve", json={'uid': uid, 'language': language, 'text': line}, timeout=60).json()
    return ["\n".join(result["sourceContext"]), "\n".join(result["targetContext"])]


def main(args):
    processes = []

    try:
        # Start servers if needed
        if args.tm_server is None:
            processes.append(launch_tm_server(args))
            tm_server_url = local_tm_server_url
        else:
            tm_server_url = args.tm_server

        if args.marian_server is None:
            processes.append(launch_marian_server(args))
            marian_server_url = local_marian_server_url
        else:
            marian_server_url = args.marian_server

        time.sleep(5)

        for line in sys.stdin:
            line = line.strip()

            # Translate
            context = get_context(tm_server_url, line, args.uid, args.language)
            translation = translate(marian_server_url, line, context)

            sys.stdout.write(translation.strip() + '\n')

    finally:
        for proc in processes:
            proc.kill()


if __name__ == "__main__":
    main(get_translate_args())
