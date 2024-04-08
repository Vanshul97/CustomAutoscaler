**AutoScaler**
AutoScaler is a Python class for managing the scaling of a separate application based on CPU utilization metrics.

**Installation**
No installation required. Just include the autoscaler.py file in your project.

**Usage**
Import the AutoScaler class from autoscaler.py.
Instantiate an AutoScaler object with the necessary parameters.
Call the auto_scale() method to start auto-scaling.

**Parameters**
app_url: The URL of the target application.
target_cpu: The target CPU utilization (default 0.80).
max_replicas: The maximum number of replicas (default 20).
min_replicas: The minimum number of replicas (default 1).
scale_up_threshold: The CPU utilization threshold for scaling up (default 0.85).
scale_down_threshold: The CPU utilization threshold for scaling down (default 0.75).
polling_interval: The interval for polling CPU utilization (default 60 seconds).
