# Temalab22-23-1

Mivel a Git nem engedi hogy >100MB méretű filet pusholjak, ezért ahhoz hogy működjön, töltsd le ezt: https://pjreddie.com/media/files/yolov3.weights 

A sample.py fileban a model_file_path változó helyére írd be az előző .weights file elérési útját.

![Output](sampleOutputGif.gif)

## _TODO_
- GPU-ra kiszervezés, mert CPU-n lassú
- Mivel a Yolov3 max. 608 * 608 méretben tud dolgozni, ezért a távolibb autókat nem ismeri fel -> ha lehet, felbontani a frameket több, egymásban átfedésben lévő képre (így azokat az autókat is felismeri, ami alapból az overlap hiánya miatt több képre szerveződött volna ki) és ezeket külön elemezni, majd mergelni a képet és a bounding boxokat