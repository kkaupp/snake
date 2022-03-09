# Setup virtual environment

## Move into project folder
cd 'path_to_snake_folder'
## Setup & activate virtual environment         
python3 -m venv ./venv              
venv\Scripts\activate (Linux/macOS: source ./venv/bin/activate)
## Install pygame & numpy
pip install -r requirements.txt  
## Start program
python3 main.py

## Disable virtual environment when finished
deactivate

# Without virtual environment
cd 'path_to_snake_folder' && pip install -r requirements.txt  
python3 main.py