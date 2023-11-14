# cython: language_level=3
#setup.py  python3.7
from setuptools import setup
from Cython.Build import cythonize

"""
Downloading upx.exe can also compress the size function
Use Cython to encrypt the main py file. Remove the py file when using pyinstaller to generate exe. Finally, move the original py file back to ensure it is not lost.
If the module in the py file is not successfully imported, add --hidden-import to the command line to import it.

> pyinstaller -F home.py -w  -i ./assets/kitsune.png --hidden-import face_det
"""
setup(
  name='AnimeGANv3',  # Package names
  ext_modules=cythonize(["photo_page.py",])  #The .py here is the py file that needs to be converted to pyd; modify it yourself.
)

"""
Run the following command to compile photo_page.pyx and generate the corresponding .so or pyd file.

python setup.py build_ext --inplace
"""