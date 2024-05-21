import cv2
import time
import numpy as np
import tflite_runtime.interpreter as tflite
from picamera2 import MappedArray, Picamera2, Preview

rectangles = [] # Global list to store rectangle coordinates for detected objects
camera = Picamera2()


def ReadLabelFile(file_path):
    """
    Reads a label file and returns a dictionary mapping IDs to labels.
    
    Args:
        file_path (str): Path to the label file.
    
    Returns:
        dict: A dictionary where keys are integer IDs and values are the corresponding labels.
    """
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    dict = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        dict[int(pair[0])] = pair[1].strip()
    return dict


def DrawRectangles(request):
    """
    Draws rectangles on the image based on the coordinates in the global `rectangles` list.
    
    Args:
        request: A request object containing image data.
    """
    
    with MappedArray(request, "main") as m:
        for rect in rectangles:
            rect_start = (int(rect[0] * 2) - 5, int(rect[1] * 2) - 5)
            rect_end = (int(rect[2] * 2) + 5, int(rect[3] * 2) + 5)
            cv2.rectangle(m.array, rect_start, rect_end, (0, 255, 0, 0))


def InferenceTensorFlow(image, model, label, video_out_location):
    """
    Performs object detection on an image using a TensorFlow Lite model.
    
    Args:
        image: The image on which to perform inference.
        model (str): Path to the TensorFlow Lite model file.
        label (str): Path to the label file.
        video_out_location (str): Path where the video will be saved if a person is detected.
    """
    
    global rectangles

    if label:
        labels = ReadLabelFile(label)
    else:
        labels = None

    interpreter = tflite.Interpreter(model_path=model, num_threads=4)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Prepare the input image
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    floating_model = False
    if input_details[0]['dtype'] == np.float32:
        floating_model = True

    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    initial_h, initial_w, channels = rgb.shape

    picture = cv2.resize(rgb, (width, height))

    input_data = np.expand_dims(picture, axis=0)
    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke() # Start interpreting the frame using the pretrained model
    
    # Get detection results
    detected_boxes = interpreter.get_tensor(output_details[0]['index'])
    detected_classes = interpreter.get_tensor(output_details[1]['index'])
    detected_scores = interpreter.get_tensor(output_details[2]['index'])
    num_boxes = interpreter.get_tensor(output_details[3]['index'])

    rectangles = []
    for i in range(int(num_boxes)):
        top, left, bottom, right = detected_boxes[0][i]
        classId = int(detected_classes[0][i])
        score = detected_scores[0][i]
        if score > 0.5: # Filter out detections with low confidence
            xmin = left * initial_w
            ymin = bottom * initial_h
            xmax = right * initial_w
            ymax = top * initial_h
            if labels:
                print(labels[classId], 'score = ', score)
                if (labels[classId] == 'person') and (score >= 0.60):
                    # If a person is detected with high confidence, capture video
                    capture_video(video_out_location)
            else:
                print('score = ', score)
            box = [xmin, ymin, xmax, ymax]
            rectangles.append(box)


def capture_video(video_out_location):
    """
    Captures a video for a set duration (30 sec) and saves it to the specified location.
    
    Args:
        video_out_location (str): Path where the video will be saved.
    """
    camera.start_and_record_video(video_out_location, duration=30)
    camera.stop_preview()
    quit() # Exit the program after finished capturing video


def main():
    """
    Main function to initialize camera preview, configure it, and perform continuous inference.
    """
    global camera
    camera.start_preview(Preview.QTGL)
    config = camera.create_preview_configuration(
        main={
            "size": (
                640, 480)}, lores={
            "size": (
                320, 240), "format": "YUV420"})
    camera.configure(config)

    stride = camera.stream_configuration("lores")["stride"]
    # Called automatically by camera for each frame
    camera.post_callback = DrawRectangles

    camera.start()
    
    timeout = 120 # Set operation timeout for 2 minutes
    timeout_start = time.time()
    
    while time.time() < timeout_start + timeout:
        buffer = camera.capture_buffer("lores")
        # Create a 2D numpy array representing a grayscale image
        grey = buffer[:stride * 240].reshape((240, stride))
        _ = InferenceTensorFlow(
            grey,
            "mobilenet_v2.tflite",
            "coco_labels.txt",
            "test.mp4")
    quit()


if __name__ == '__main__':
    main()
