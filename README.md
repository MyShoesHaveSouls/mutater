# mutater

# Update and upgrade the system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3 and pip (if not already installed)
sudo apt-get install python3 python3-pip -y

# Install virtualenv (if not already installed)
pip3 install virtualenv

# Create a virtual environment in the project directory
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip within the virtual environment
pip install --upgrade pip

# Install the required dependencies listed in requirements.txt
pip install -r requirements.txt

# Run the Python script
python guided_search.py
