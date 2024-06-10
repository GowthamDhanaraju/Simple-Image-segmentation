# graph_builder.py
import numpy as np
import cv2
from math import exp, pow
from seeding import Seeding
SIGMA = 30

class GraphBuilder:
    def __init__(self, image):
        self.image = image

    def boundaryPenalty(self, ip, iq):
        bp = 100 * exp(- pow(int(ip) - int(iq), 2) / (2 * pow(SIGMA, 2)))
        return bp

    def buildGraph(self):
        V = self.image.size + 2
        graph = np.zeros((V, V), dtype='int32')
        K = self.makeNLinks(graph)
        seeds, seededImage = Seeding(self.image).plantSeed(self.image)
        self.makeTLinks(graph, seeds, K)
        return graph, seededImage

    def makeNLinks(self, graph):
        K = -float("inf")
        r, c = self.image.shape
        for i in range(r):
            for j in range(c):
                x = i * c + j
                if i + 1 < r:  # pixel below
                    y = (i + 1) * c + j
                    bp = self.boundaryPenalty(self.image[i][j], self.image[i + 1][j])
                    graph[x][y] = graph[y][x] = bp
                    K = max(K, bp)
                if j + 1 < c:  # pixel to the right
                    y = i * c + j + 1
                    bp = self.boundaryPenalty(self.image[i][j], self.image[i][j + 1])
                    graph[x][y] = graph[y][x] = bp
                    K = max(K, bp)
        return K

    def makeTLinks(self, graph, seeds, K):
        r, c = seeds.shape
        for i in range(r):
            for j in range(c):
                x = i * c + j
                if seeds[i][j] == 1:
                    graph[-2][x] = K
                elif seeds[i][j] == 2:
                    graph[x][-1] = K
