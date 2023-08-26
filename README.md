# KitchenSink.KivyMD
## KitchenSink for KivyMD

### Demo application of the [KivyMD](https://github.com/longvalery/KitchenSink.KivyMD.git) library widgets

# Description
These are collections of simple stylish and modern user interface design for mobile and desktop applications.

# Install

## Step 1. Download this project

git clone https://github.com/longvalery/KitchenSink.KivyMD.git

## Step 2. Change the directory

cd KitchenSink.KivyMD 

## Step 3. Create python environment

python -m venv venv

## Step 4. Run python environment

For Windows: call .\venv\Scripts\activate.bat

For Linux:   source ./venv/bin/activate

## Step 5. Install all dependent packages

For Windows: 
pip install -r requirements.txt 

For Linux:
pip install -r linux.requirements.txt

# Run
## For the beginning

For Windows: call .\venv\Scrips\activate.bat

For Linux:   source ./venv/bin/activate

## Then

python main.py

## Enjoy 

Hot keys are

Shift+F11 - change Orientation (standard Kivy)

Shift+F8 - change Theme

Shift+F7 - change Language

Shift+F6 - change Animation

Shift+F5 - change primary color of the application 



# Addition. Build exe-file for Windows
## Install pyinstaller
call .\venv\Scrips\activate.bat

then

pip install pyinstaller

## Build application and copy images
call .\venv\Scrips\activate.bat

pyinstaller --clean -y -n "DemoKivyMD" --onefile main.py

mkdir .\dist\assets

copy .\assets\*.png .\dist\assets\*.*

## Run application

.\dist\DemoKivyMD.exe 

# Addition. Build and install apk-file for Android
## Install Buildozer. Only Linux
call .\venv\Scrips\activate.bat

then

pip install -r android.requirements.txt

## Build apk-file 

./buildozerBuild.bash 

##  apk-file

./buildozerDeploy.bash 

The log file will be written to the ./out.txt file







