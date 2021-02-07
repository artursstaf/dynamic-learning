import argparse


def get_translate_args():
    parser = argparse.ArgumentParser()
    # Marian config
    parser.add_argument('--config', required=False, type=str)
    parser.add_argument('--devices', required=False, type=str)
    parser.add_argument('--after-batches', required=False, type=str, default="10")
    parser.add_argument('--workspace', required=False, type=str, default="8000")
    parser.add_argument('--after-epochs', required=False, type=str, default="10")
    parser.add_argument('--learn-rate', required=False, type=str, default="0.1")
    parser.add_argument('--mini-batch', required=False, type=str, default="15")
    # TM Config
    parser.add_argument('--bleu-rescoring-threshold', required=False, type=str, default="0.05")
    parser.add_argument('--language', required=True, type=str)
    parser.add_argument('--uid', required=True, type=str)
    # Servers url
    parser.add_argument('--tm-server', required=False, type=str)
    parser.add_argument('--marian-server', required=False, type=str)
    return parser.parse_args()


def get_fill_tm_args():
    parser = argparse.ArgumentParser()
    # TM Config
    parser.add_argument('--language', required=True, type=str)
    parser.add_argument('--uid', required=True, type=str)
    parser.add_argument('--bleu-rescoring-threshold', required=False, type=str, default="0.05")
    # Server url
    parser.add_argument('--tm-server', required=False, type=str)
    # Input files
    parser.add_argument('--source', required=True, type=argparse.FileType('r'))
    parser.add_argument('--target', required=True, type=argparse.FileType('r'))
    return parser.parse_args()
