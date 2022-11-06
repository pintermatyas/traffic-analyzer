# Temalab22-23-1: Vehicle Tracking

Mivel a Git nem engedi hogy >100MB méretű filet pusholjak, ezért ahhoz hogy működjön, töltsd le ezt: https://pjreddie.com/media/files/yolov3.weights 

A sample.py fileban a model_file_path változó helyére írd be az előző .weights file elérési útját.

Tracking előtt:

![Output](sampleOutputGif.gif)


Tracking után

![Output](sampleOutputGifTracking.gif)

## _TODO_
- GPU-ra kiszervezés, mert CPU-n lassú
- Úgy tűnik, hogy 
  - Egy ID-t több autónak is kiad &rarr; Ennek javítása
  - Az ID-k osztásánál többször van az, hogy nem eggyel növeli az új autó ID-jét az előzőhöz képest