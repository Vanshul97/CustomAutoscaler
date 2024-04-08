**AutoScaler**
AutoScaler is a Python class for managing the scaling of a separate application based on CPU utilization metrics.

**Installation**
No installation required. Just include the autoscaler.py file in your project.

**Usage**
Import the AutoScaler class from autoscaler.py.
Instantiate an AutoScaler object with the necessary parameters.
Call the auto_scale() method to start auto-scaling.


import logging
from autoscaler import AutoScaler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app_url = "http://example.com"  # Replace with the actual URL of the application
    target_cpu = 0.80  # Specify the target CPU utilization (80%)
    auto_scaler = AutoScaler(app_url, target_cpu=target_cpu)
    auto_scaler.auto_scale()

    auto_scaler.auto_scale()
**Parameters**
app_url: The URL of the target application.
target_cpu: The target CPU utilization (default 0.80).
max_replicas: The maximum number of replicas (default 20).
min_replicas: The minimum number of replicas (default 1).
scale_up_threshold: The CPU utilization threshold for scaling up (default 0.85).
scale_down_threshold: The CPU utilization threshold for scaling down (default 0.75).
polling_interval: The interval for polling CPU utilization (default 60 seconds).
