# is-ros2-gateway

### To run the project

```
sudo docker run --rm -it --network=host matheusdutra0207/is-ros2-gateway:0.0.1 bash
```

```
source install/setup.bash
```

```
ros2 run is_ros2_gateway is_ros2_gateway --uri amqp://10.20.5.2:30000
```

```
export FASTDDS_BUILTIN_TRANSPORTS=UDPv4
```
