# Use the ROS 2 Humble desktop base image
FROM osrf/ros:humble-desktop

# Install common dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3-pip \
    ros-humble-gazebo-ros-pkgs \
    tmux \
    ros-humble-gazebo-ros \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --user -U empy pyros-genmsg setuptools

RUN pip3 install kconfiglib \
    && pip install --user jsonschema \
    && pip install --user jinja2

WORKDIR /root

# Setup PX4 Autopilot
RUN git clone https://github.com/PX4/PX4-Autopilot.git \
    && bash ./PX4-Autopilot/Tools/setup/ubuntu.sh \
    && cd PX4-Autopilot \
    && make px4_sitl

# Build Micro XRCE-DDS Agent
RUN git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git && \
    cd Micro-XRCE-DDS-Agent && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    sudo make install && \
    sudo ldconfig /usr/local/lib/

# Install gazebo
RUN curl -sSL http://get.gazebosim.org | sh
RUN apt-get update && apt-get install -y ros-humble-gazebo-ros

# Install x11
RUN apt-get update && apt-get install -y \
    libx11-xcb1 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/ros_ws

COPY ./ ./ 

RUN rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y

# Build the workspace
RUN . /opt/ros/humble/setup.sh && colcon build

RUN apt-get update && apt-get install -y ros-humble-gazebo-ros-pkgs

RUN cd /root/PX4-Autopilot && make px4_sitl_default sitl_gazebo-classic && make px4_sitl

CMD ["./run.sh"]




