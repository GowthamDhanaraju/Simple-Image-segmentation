# seeding.py
import cv2
import numpy as np
SF = 10

class Seeding:
    def __init__(self, image):
        self.image = image

    def show_image(self, image):
        windowname = "Segmentation"
        cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
        cv2.startWindowThread()
        cv2.imshow(windowname, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def plantSeed(self, image):
        def drawLines(x, y, pixelType):
            if pixelType == "OBJ":
                color, code = (0, 0, 255), 1
            else:
                color, code = (0, 255, 0), 2
            cv2.circle(image, (x, y), radius, color, thickness)
            cv2.circle(seeds, (x // SF, y // SF), radius // SF, code, thickness)

        def onMouse(event, x, y, flags, pixelType):
            global drawing
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                drawLines(x, y, pixelType)
            elif event == cv2.EVENT_MOUSEMOVE and drawing:
                drawLines(x, y, pixelType)
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False

        def paintSeeds(pixelType):
            print("Planting", pixelType, "seeds")
            global drawing
            drawing = False
            windowname = "Plant " + pixelType + " seeds"
            cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback(windowname, onMouse, pixelType)
            while True:
                cv2.imshow(windowname, image)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            cv2.destroyAllWindows()

        seeds = np.zeros(image.shape, dtype="uint8")
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        image = cv2.resize(image, (0, 0), fx=SF, fy=SF)

        radius = 10
        thickness = -1  # fill the whole circle
        global drawing
        drawing = False

        paintSeeds("OBJ")
        paintSeeds("BKG")
        return seeds, image
