import os
import torch
from ultralytics import YOLO


device = 0 if torch.cuda.is_available() else "cpu"

yolo_model = YOLO(os.path.join("resources", "yolov8_model.pt"))
class_names= yolo_model.names

def get_pred(img):
    pred_dict= {}
    results = yolo_model.predict(img, imgsz=640, device=device, batch=1)
    result = results[0]

    for detection in result.boxes:
        x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy()
        bbox= [x1, y1, x2, y2]
        conf = detection.conf[0].cpu().numpy()
        cls = detection.cls[0].cpu().numpy()
    pred_dict['bbox']= bbox
    pred_dict['conf']= conf
    pred_dict['cls_idx'] = int(cls)
    pred_dict['cls_name'] = yolo_model.names[int(cls)]

    return pred_dict
