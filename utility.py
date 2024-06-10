# utility.py
import argparse

class Utility:
    @staticmethod
    def parseArgs():
        def algorithm(string):
            if string in {"ap", "pr"}:
                return string
            raise argparse.ArgumentTypeError("Algorithm should be one of 'ap' (Augmenting Path) or 'pr' (Push Relabel).")

        parser = argparse.ArgumentParser()
        parser.add_argument("imagefile")
        parser.add_argument("--size", "-s", default=30, type=int, help="Defaults to 30x30")
        parser.add_argument("--algo", "-a", default="ap", type=algorithm, help="Algorithm to use: 'ap' for Augmenting Path, 'pr' for Push Relabel")
        return parser.parse_args()
