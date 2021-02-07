import subprocess
from pathlib import Path

from utils.prune_model_config import prune

MARIAN_PORT = str(8089)
TM_PORT = str(8088)

local_tm_server_url = f"http://localhost:{TM_PORT}"
local_marian_server_url = f"ws://localhost:{MARIAN_PORT}"


def launch_tm_server(args):
    return subprocess.Popen(
        ["./tm/bin/tm",
         "--port", TM_PORT,
         "--blue-rescoring-threshold", args.bleu_rescoring_threshold,
         ])


def launch_marian_server(args):
    assert args.config is not None, "No config file specified"
    config = Path(args.config)
    assert config.exists(), "Config path doesnt exist"
    assert args.devices is not None, "Device id not specified"

    prune(str(config))
    pruned_config = str(config.with_suffix(".da.yml"))

    return subprocess.Popen(["./marian-dev/build/marian-adaptive",
                             "--port", MARIAN_PORT,
                             "--config", pruned_config,
                             "--after-batches", args.after_batches,
                             "--after-epochs", args.after_epochs,
                             "--learn-rate", args.learn_rate,
                             "--mini-batch", args.mini_batch,
                             "--workspace", args.workspace
                             ])
