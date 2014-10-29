#!/bin/sh

# Install Python & friends
echo "Installing Python and friends..."
sudo apt-get install -y python python-pip python-virtualenv

# Fetch the Git submodules
echo "Fetching submodules..."
git submodule init && git submodule update && git submodule status

# Create a virtual environment for the project if it doesn't exist yet
if [ ! -f /tmp/foo.txt ]
then
    echo "Creating virtual environment..."
    virtualenv env
fi

# Enter the virtual environment
. env/bin/activate

# Install the Python packages
echo "Installing Python packages..."
pip install -r requirements.txt

echo "\n------------------------------------------------------------------------\n"

echo "Congrats, it looks like you just installed the Bitvid Frontend Prerender!"
echo "You've unlocked this unicode cookie: 🍪\n"

echo "You can run this thing with:"
echo "    . env/bin/activate"
echo "    python app.py\n"

echo "Good luck!\n"
