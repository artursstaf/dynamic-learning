import sys
import yaml
import os


def prune(model_config_file):
    whitelist = {"model", "vocabs", "log-level", "quiet", "quiet-translation", "seed", "clip-gemm",
                 "interpolate-env-vars", "relative-paths", "type", "dim-vocabs", "dim-emb", "dim-rnn", "enc-type",
                 "enc-cell", "enc-cell-depth", "enc-depth", "dec-cell", "dec-cell-base-depth", "dec-cell-high-depth",
                 "dec-depth", "skip", "layer-normalization", "right-left", "best-deep", "tied-embeddings",
                 "tied-embeddings-src", "tied-embeddings-all", "transformer-heads", "transformer-no-projection",
                 "transformer-dim-ffn", "transformer-ffn-depth", "transformer-ffn-activation", "transformer-dim-aan",
                 "transformer-aan-depth", "transformer-aan-activation", "transformer-aan-nogate",
                 "transformer-decoder-autoreg", "transformer-tied-layers", "transformer-guided-alignment-layer",
                 "transformer-preprocess", "transformer-postprocess-emb", "transformer-postprocess", "dropout-rnn",
                 "dropout-src", "dropout-trg", "grad-dropping-rate", "grad-dropping-momentum", "grad-dropping-warmup",
                 "transformer-dropout", "transformer-dropout-attention", "transformer-dropout-ffn", "cost-type",
                 "overwrite", "no-reload", "after-epochs", "after-batches", "disp-freq", "disp-label-counts",
                 "save-freq",
                 "max-length", "max-length-crop", "no-shuffle", "no-restore-corpus", "tempdir", "sqlite", "sqlite-drop",
                 "cpu-threads", "mini-batch", "mini-batch-words", "maxi-batch", "maxi-batch-sort", "optimizer",
                 "optimizer-params", "optimizer-delay", "sync-sgd", "learn-rate", "lr-report", "lr-decay",
                 "lr-decay-strategy", "lr-decay-start", "lr-decay-freq", "lr-decay-reset-optimizer",
                 "lr-decay-repeat-warmup", "lr-decay-inv-sqrt", "lr-warmup", "lr-warmup-start-rate", "lr-warmup-cycle",
                 "lr-warmup-at-reload", "label-smoothing", "clip-norm", "exponential-smoothing",
                 "guided-alignment-cost",
                 "guided-alignment-weight", "data-weighting-type", "embedding-normalization", "embedding-fix-src",
                 "embedding-fix-trg", "multi-node", "multi-node-overlap", "beam-size", "normalize", "max-length-factor",
                 "word-penalty", "allow-unk", "n-best"}

    with open(os.path.join(os.path.dirname(model_config_file), "model.npz.decoder.yml")) as yfile:
        decoder_config = yaml.load(yfile, Loader=yaml.FullLoader)
        model = decoder_config["models"][0]
        vocabs = decoder_config["vocabs"]

    with open(model_config_file) as yfile:
        model_config = yaml.load(yfile, Loader=yaml.FullLoader)

        # Some Marian versions produce lr-decay-inv-sqrt as a list
        if "lr-decay-inv-sqrt" in model_config and type(model_config["lr-decay-inv-sqrt"]) is list:
            model_config["lr-decay-inv-sqrt"] = model_config["lr-decay-inv-sqrt"][0]

        pruned_config = {k: v for k, v in model_config.items() if k in whitelist}

        # letsMT requires relative paths
        pruned_config["relative-paths"] = "true"
        pruned_config["model"] = os.path.basename(model)
        pruned_config["vocabs"] = [os.path.basename(fname) for fname in vocabs]

    pruned_model_config_file = "{}.da.yml".format(os.path.splitext(model_config_file)[0])
    with open(pruned_model_config_file, 'w') as yfile:
        documents = yaml.dump(pruned_config, yfile)


if __name__ == "__main__":
    prune(sys.argv[0])
