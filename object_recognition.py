# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.


import os
from ultralytics import YOLO
import numpy
import utils
import config
config = config.load_config()

dashcam_model = YOLO(config["dashcam"]["parked"]["event"]["trigger_object_recognition"]["model_weights"])

def predict(frame, selected_model):
    if (selected_model == "dashcam"):
        model = dashcam_model
    else:
        utils.display_message("Unrecognized model specified for `predict()`.", 3)
    results = model(frame, verbose=False)
    class_names = results[0].names

    detected_objects = [] # This is a placeholder that will hold all of the detected objects.
    for result in results:
        boxes = result.boxes
        for i in range(0, len(boxes)):
            obj = {}
            box = result.boxes[i].xyxy.numpy().tolist()[0]
            obj["bbox"] = {}
            obj["bbox"]["x1"] = round(box[0])
            obj["bbox"]["y1"] = round(box[1])
            obj["bbox"]["x2"] = round(box[2])
            obj["bbox"]["y2"] = round(box[3])
            obj["name"] = class_names[int(result.boxes[i].cls.numpy().tolist()[0])]
            obj["conf"] = result.boxes[i].conf.numpy().tolist()[0]
            detected_objects.append(obj)
    return detected_objects
