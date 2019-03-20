# Eman's Edge Computing System For AI Applications

Highly accurate AI applications, particularly for Computer Vision requires extensive memory and computational power.
Eman's Edge Computing System orchestrates resource limited devices that requires using resource heavy AI algorithms so that
a system can still achieve ideal system performances. This is done through Edge's monitoring modules that determines
how to adjust the system so the system can operate efficiently based on its environments conditions.

The components of the system are the following:

1. Node: 4 or more Raspberry PI 3 B+

2. Edge: Windows Laptop with NVIDIA GPU 1080 TI

3. Cloud: Google Cloud Platform, Compute Engine, Ubuntu 16.04 with Tesla P100

### Requirements: software

1. Python packages from requirements.txt.
   It can be access through pip install -r requirements.txt

2. NVIDIA CUDA 9.0 installed in computer

3. Weights that are generated during training.

4. Monitoring module. Currently only in Eman's private Github account.


### Requirements: hardware

1. For EDGE and CLOUD: NVIDIA GPU that supports NVIDIA CUDA 9.0

2. For NODE: Raspberry PI 3 B+

3. For CLOUD: Google Cloud Platform, Compute Engine

### Requirements: Design Patterns Used

1. Chain of Responsibility

2. Factory Method

3. Strategy Pattern

4. Builder

5. Observer

6. Singleton

### Running application

python main.py -s WINDOWS -c EDGE -m YOLOV2 -v NONE
