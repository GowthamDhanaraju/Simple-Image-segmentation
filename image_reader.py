# image_reader.py
import cv2
import os
from seeding import Seeding
from graph_builder import GraphBuilder
from display import Display
from AugmentingPath import AugmentingPath
from PushRelabel import PushRelabel
SIGMA = 30
SOURCE, SINK = -2, -1
# image_reader.py

class ImageReader:
    def __init__(self, imagefile, size=(30, 30), algo="ap"):
        self.imagefile = imagefile
        self.size = size
        self.algo = algo

    def imageSegmentation(self):
        pathname = os.path.splitext(self.imagefile)[0]
        image = cv2.imread(self.imagefile, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, self.size)
        graph, seededImage = GraphBuilder(image).buildGraph()
        cv2.imwrite(pathname + "seeded.jpg", seededImage)

        global SOURCE, SINK
        SOURCE += len(graph)
        SINK += len(graph)

        if self.algo == "ap":
            cuts = AugmentingPath.augmentingPath(graph, SOURCE, SINK)
        elif self.algo == "pr":
            cuts = PushRelabel.pushRelabel(graph, SOURCE, SINK)
        else:
            raise ValueError("Unknown algorithm: " + self.algo)

        print("cuts:")
        print(cuts)
        image = Display(image).displayCut(cuts)
        image = cv2.resize(image, (0, 0), fx=10, fy=10)
        Seeding(image).show_image(image)
        savename = pathname + "cut.jpg"
        cv2.imwrite(savename, image)
        print("Saved image as", savename)
