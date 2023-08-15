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

pip install -r requirements.txt 


# Run
## For the beginning

For Windows: call .\venv\Scrips\activate.bat

For Linux:   source ./venv/bin/activate

## Then

python DemoKivyMD.py

## Enjoy  


# Addition. Build exe-file for Windows
## Install pyinstaller
call .\venv\Scrips\activate.bat

then

pip install pyinstaller

## Build application
call .\venv\Scrips\activate.bat

pyinstaller --clean -y -n "DemoKivyMD" --onefile DemoKivyMD.py

## Run application

.\dist\DemoKivyMD.exe 

