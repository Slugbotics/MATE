import mediapipe as mp
import cv2
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# https://developers.google.com/mediapipe/api/solutions/python/mp/tasks/vision/ObjectDetector
# According to an article, media pipe does not do well with python object detection but does with other
# languages - there is a thing called objectron however, which might be worth a try

# STEP 2: Create an ObjectDetector object.
base_options = python.BaseOptions(model_asset_path='lite-model_object_detection_mobile_object_localizer_v1_1_metadata_2.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5)
detector = vision.ObjectDetector.create_from_options(options)

hands = mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3,
        max_num_hands=4)

#@markdown We implemented some functions to visualize the object detection results. <br/> Run the following cell to activate the functions.

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def visualize(
    image,
    detection_result
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  image.flags.writeable = True
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)


def write_marks_detection(image, copy):
   i = mp.Image(
    image_format=mp.ImageFormat.SRGB, data=image)
   detection_result = detector.detect(i)
   visualize(copy, detection_result)


def write_marks_hands(image, copy):
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                copy,
                (hand_landmarks),
                (mp_hands.HAND_CONNECTIONS),
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())