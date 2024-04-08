import requests
import logging
import time

class AutoScaler:
    """
    AutoScaler class for managing the scaling of a separate application based on CPU utilization metrics.
    """

    def __init__(self, app_url, target_cpu=0.80, max_replicas=20, min_replicas=1, scale_up_threshold=0.85, scale_down_threshold=0.75, polling_interval=60):
        self.app_url = app_url
        self.target_cpu = target_cpu
        self.max_replicas = max_replicas
        self.min_replicas = min_replicas
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.polling_interval = polling_interval

    def get_cpu_utilization(self):
        try:
            response = requests.get(f"{self.app_url}/app/status", headers={"Accept": "application/json"})
            response.raise_for_status()  # Exception for non-2xx status codes
            return response.json()["cpu"]["highPriority"]
        except requests.RequestException as e:
            logging.error(f"Failed to get CPU utilization: {e}")
            return None

    def set_replica_count(self, replica_count):
        try:
            if replica_count < 1:
                raise ValueError("Replica count must be greater than or equal to 1")
            payload = {"replicas": replica_count}
            response = requests.put(f"{self.app_url}/app/replicas", json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()  # exception for non-2xx status codes
            logging.info(f"Replica count set to: {replica_count}")
        except ValueError as ve:
            logging.error(f"Invalid replica count: {ve}")
        except requests.RequestException as e:
            logging.error(f"Failed to set replica count: {e}")

    def auto_scale(self):
        while True:
            cpu_utilization = self.get_cpu_utilization()
            if cpu_utilization is not None:
                if cpu_utilization > self.scale_up_threshold and self.max_replicas > 1:
                    new_replicas = min(self.max_replicas, int(round(cpu_utilization * self.max_replicas)))
                    self.set_replica_count(new_replicas)
                elif cpu_utilization < self.scale_down_threshold and self.min_replicas < self.max_replicas:
                    new_replicas = max(self.min_replicas, int(round(cpu_utilization * self.max_replicas)))
                    self.set_replica_count(new_replicas)
            time.sleep(self.polling_interval)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app_url = "http://example.com"  # Replace with the actual URL of the app
    target_cpu = 0.80  # Specify the target CPU utilization (80%)
    auto_scaler = AutoScaler(app_url, target_cpu=target_cpu)
    auto_scaler.auto_scale()
