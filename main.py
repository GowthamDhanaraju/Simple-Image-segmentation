# main.py
from utility import Utility
from image_reader import ImageReader

if __name__ == "__main__":
    args = Utility.parseArgs()
    ImageReader(args.imagefile, (args.size, args.size), args.algo).imageSegmentation()
