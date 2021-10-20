from vilib import Vilib

def main():
    Vilib.camera_start(inverted_flag=True)
    Vilib.display()
    # Vilib.object_detect_set_model(path='/opt/vilib/detect.tflite')
    # Vilib.object_detect_set_labels(path='/opt/vilib/coco_labels.txt')
    Vilib.object_detect_switch(True)

if __name__ == "__main__":
    main()