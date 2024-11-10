# led-matrix

## Setup

Run `git submodule update --init` to pull the `rpi-rgb-led-matrix` library

In the `rpi-rgb-led-matrix` directory, run the following commands to setup the python library

```bash
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
make build-python 
sudo make install-python 
```

Create a virtualenv and run `pip install -r requirements.txt`

Start app with `python3 app.py`
