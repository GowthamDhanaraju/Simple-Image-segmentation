# display.py
import cv2

class Display:
    def __init__(self, image):
        self.image = image

    def displayCut(self, cuts):
        def colorPixel(i, j):
            self.image[i][j] = (0, 0, 255)

        r, c = self.image.shape
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        for c in cuts:
            if c[0] != -2 and c[0] != -1 and c[1] != -2 and c[1] != -1:
                colorPixel(c[0] // r, c[0] % r)
                colorPixel(c[1] // r, c[1] % r)
        return self.image
