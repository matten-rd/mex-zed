from ultralytics import YOLO
import cv2

class YOLOv8_Tracker:
    def __init__(self, classes, conf = 0.5, iou = 0.5, modelName="yolov8n.pt", camera=0, outputFile="outputvideo.avi"):
        self.model = YOLO(modelName)
        self.classes = classes
        self.conf = conf
        self.iou = iou
        self.cap = cv2.VideoCapture(camera)
        
        h, w = self.getHeightWidth()
        self.videoWriter = cv2.VideoWriter(
            outputFile,
            cv2.VideoWriter_fourcc(*'MJPG'),
            int(self.cap.get(cv2.CAP_PROP_FPS)),
            (w, h)
        )
        
        self.windowName = "ZED"
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

        self.setResolution(1344, 376)


    def setResolution(self, width, height):
        # MODE  FPS     Width x Height  Config File Option
        # 2.2K 	15 	    4416 x 1242     2K
        # 1080p 30 	    3840 x 1080     FHD
        # 720p 	60 	    2560 x 720      HD
        # WVGA 	100 	1344 x 376      VGA
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cv2.resizeWindow(self.windowName, 1344, 376)

    def getFullFrame(self):
        _, frame = self.cap.read()
        return frame

    def getHeightWidth(self):
        frame = self.getFullFrame()
        height, width, _ = frame.shape
        return height, width
    
    def getLeftRightFrame(self):
        frame = self.getFullFrame()
        _, width = self.getHeightWidth()
        # split single ZED frame into left an right
        frameL= frame[:,0:int(width/2),:]
        frameR = frame[:,int(width/2):width,:]
        return frameL, frameR

    def trackObjects(self):
        frame = self.getFullFrame()
        # Run tracking
        results = self.model.track(
            source=frame, 
            persist=True, 
            conf=self.conf, 
            iou=self.iou, 
            show=False, 
            classes=self.classes
        )
        frame = results[0].plot()

        return frame
    
    def showVideoFeed(self, frame):
        cv2.imshow(self.windowName, frame)

    def destroyVideoFeed(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def captureVideoFeed(self, frame):
        self.videoWriter.write(frame)
