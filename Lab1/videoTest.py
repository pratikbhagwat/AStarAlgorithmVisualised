import cv2
import os

videoName = "AstarVisualized.avi"

images = []

numberOfImages = os.listdir("/Users/pratikbhagwat/PycharmProjects/PratikBhagwatFAI2020Spring/ImagesForVideo").__len__()


frame = cv2.imread("/Users/pratikbhagwat/PycharmProjects/PratikBhagwatFAI2020Spring/ImagesForVideo/0.jpg")

height, width, layers = frame.shape

video = cv2.VideoWriter(videoName, 0, 200, (width, height))

for i in range(numberOfImages):
    video.write(cv2.imread("/Users/pratikbhagwat/PycharmProjects/PratikBhagwatFAI2020Spring/ImagesForVideo/"+str(i)+".jpg"))


cv2.destroyAllWindows()
video.release()


