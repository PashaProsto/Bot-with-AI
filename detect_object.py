from imageai.Detection import ObjectDetection

def detect_all_objects(img, model):

  detector = ObjectDetection()
  detector.setModelTypeAsYOLOv3()
  detector.setModelPath(model)
  detector.loadModel()

  detections = detector.detectObjectsFromImage(input_image=img, minimum_percentage_probability=35)

  return detections

def analyze_objects(detections):
  road_obj = ['bird']
  find_obj = []

  if len(detections) >= 0:
    for i in detections:
      if i['name'] in road_obj:
          find_obj.append(i)

  return find_obj