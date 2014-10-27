# Bitvid Frontend Prerender

## Installation

Please install the backend server first before installing
the frontend prerender. This project is entirely dependent
on the backend server and is just a UI around it.

```
# Install Python & friends
sudo apt-get install -y python python-pip python-virtualenv

# Clone this repository to your favorite location and enter it
git clone git@git.bitvid.tv:bitvid/frontend-prerender.git
cd frontend-prerender

# Fetch the Git submodules
git submodule init && git submodule update && git submodule status

# Create a virtual environment for the project and enter it
# (this is basically its own little drawer of packages)
virtualenv env
. env/bin/activate

# Install the Python packages
pip install -r requirements.txt

# And last but certainly not least, get it running
python app.py runserver
```
