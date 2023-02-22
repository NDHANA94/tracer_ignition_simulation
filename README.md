# tracer_ignition_simulation

This package is created and tested only with ros2-foxy version!

### Install package
```
mkdir -p tracer_ws/src
cd tracer_ws/src
git clone https://github.com/NDHANA94/tracer_ignition_simulation.git
cd ..
colcon build
```

### launch ignition gazebo simulation
```
source install/setup.bash
ros2 launch tracer_ign_sim tracer.launch.py
```

### controlling tracer robot via teleop_twist_keyboard
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard -_-ros-args -r /cmd_vel:=/model/tracer/cmd_vel
```

#### send command via terminal
```
ign topic -t "/model/tracer/cmd_vel" -m ignition.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.05}
```
#### listen to odometry
```
ign topic -e -t /model/tracer/odometry
```