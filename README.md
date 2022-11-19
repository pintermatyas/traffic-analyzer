# Temalab22-23-1: Vehicle Tracking

Mivel a Git nem engedi hogy >100MB méretű filet pusholjak, ezért ahhoz hogy működjön, töltsd le ezt: https://pjreddie.com/media/files/yolov3.weights 

A sample.py fileban a model_file_path változó helyére írd be az előző .weights file elérési útját.

Tracking előtt:

![Output](md_files/sampleOutputGif.gif)


Tracking és sebességmeghatározás után:

![Output](md_files/sampleOutputGifTracking.gif)

Le lett korlátozva a felismeréshez használható rész az alsó felére a képnek, hogy ne legyen olyan sok fals pozitív felismerés, amit egy frame után el is veszít. Az autók irányát színkódoltam: a felénk haladó zöld, az elfele haladó kék téglalapot kap.

Heatmap az elhaladó autókról, a sample3 file-on futtatva:

![Output](md_files/sample2_detections.png)

## _TODO_
- GPU-ra kiszervezés, mert CPU-n lassú
- Úgy tűnik, hogy 
  - Egy ID-t több autónak is kiad &rarr; Ennek javítása