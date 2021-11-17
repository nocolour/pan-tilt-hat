from vilib import Vilib

def main():
    Vilib.camera_start(vflip=True,hflip=True) 
    Vilib.display(local=True,web=True)
    Vilib.object_detect_set_model(path='/opt/vilib/detect.tflite')
    Vilib.object_detect_set_labels(path='/opt/vilib/coco_labels.txt')
    Vilib.object_detect_switch(True)

if __name__ == "__main__":
    main()