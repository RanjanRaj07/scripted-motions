import subprocess
import os
import sys

def python_exec():
    return os.path.join(sys.prefix, 'bin', 'python.exe')

def installModule(packageName):
    python_exe = python_exec()
   # upgrade pip
    subprocess.call([python_exe, "-m", "ensurepip"])
    subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
   # install required packages
    subprocess.call([python_exe, "-m", "pip", "install", packageName])
    
installModule("spacy")