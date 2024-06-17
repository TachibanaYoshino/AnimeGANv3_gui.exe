# Qt interface tool based on AnimeGANv3.
This is the official repository for the [AnimeGANv3 repo](https://github.com/TachibanaYoshino/AnimeGANv3).


## Installation

Tested on Windows 10 and python 3.7.

### Install dependency

```bash
conda create -n gui python=3.7
conda activate gui
pip install -r requirements.txt
```

## Usage

#### Build 
```python
pyinstaller -F home.py -w  -i ./assets/kitsune.png --hidden-import face_det
```

#### Notice
- This repo supports encrypting onnx models and codes before packaging and publishing.
- The open AnimeGANv3 model can be obtained in the Releases.   

#### Screenshot
![](https://github.com/TachibanaYoshino/AnimeGANv3_gui.exe/blob/main/assets/screenshot.png)     


## License
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
