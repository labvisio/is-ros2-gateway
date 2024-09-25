FROM ros:humble

RUN apt update
RUN apt install -y usbutils net-tools software-properties-common wget
RUN apt-get install -y libjpeg-dev libjpeg8-dev libfreetype6-dev vim

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

RUN apt-get update
RUN apt-get install -y ros-humble-diagnostic-updater
RUN apt-get install -y ros-humble-tf-transformations
RUN apt-get install -y ros-humble-rosbridge-server

RUN pip3 install is-msgs==1.1.10 \
    &&   pip3 install is-wire==1.2.0 \
    &&   pip3 install numpy==1.21.6 \
    &&   pip3 install vine==1.3.0 \
    && pip3 install --upgrade protobuf==3.20.0 

Workdir /ros2_ws/src    
RUN git clone -b main https://github.com/labvisio/is-ros2-gateway.git 
Workdir /ros2_ws
SHELL [ "/bin/bash" , "-c" ]
RUN source ../opt/ros/humble/setup.bash 
RUN colcon build --packages-select is_ros2_gateway