FROM ubuntu:latest

RUN sudo apt install python3.10

RUN pip install tensorflow[and-cuda]

RUN python -m pip install "tensorflow[and-cuda]==2.15" --extra-index-url https://pypi.nvidia.com

RUN python -c "import tensorflow as tf
    if tf.test.gpu_device_name():
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))"






