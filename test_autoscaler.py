import unittest
from unittest.mock import MagicMock, patch
from autoscaler import AutoScaler

class TestAutoScaler(unittest.TestCase):
    def setUp(self):
        self.app_url = "http://example.com"
        self.target_cpu = 0.80 #target cpu
        self.max_replicas = 20
        self.min_replicas = 1
        self.scale_up_threshold = 0.85
        self.scale_down_threshold = 0.75
        self.polling_interval = 60
        self.auto_scaler = AutoScaler(
            self.app_url,
            self.target_cpu,
            self.max_replicas,
            self.min_replicas,
            self.scale_up_threshold,
            self.scale_down_threshold,
            self.polling_interval
        )

    def test_get_cpu_utilization_success(self):
        expected_cpu_utilization = 0.75
        response_mock = MagicMock()
        response_mock.json.return_value = {"cpu": {"highPriority": expected_cpu_utilization}}
        with patch("requests.get", return_value=response_mock):
            cpu_utilization = self.auto_scaler.get_cpu_utilization()
            self.assertEqual(cpu_utilization, expected_cpu_utilization)

    def test_get_cpu_utilization_failure(self):
        with patch("requests.get", side_effect=Exception("Test exception")):
            cpu_utilization = self.auto_scaler.get_cpu_utilization()
            self.assertIsNone(cpu_utilization)

    def test_set_replica_count_success(self):
        replica_count = 15
        response_mock = MagicMock()
        response_mock.raise_for_status.return_value = None
        with patch("requests.put", return_value=response_mock):
            with patch("logging.info"):
                self.auto_scaler.set_replica_count(replica_count)

    def test_set_replica_count_invalid(self):
        invalid_replica_count = 0
        with patch("requests.put"):
            with patch("logging.error") as mock_logging_error:
                self.auto_scaler.set_replica_count(invalid_replica_count)
                mock_logging_error.assert_called_once()

    @patch("autoscaler.AutoScaler.get_cpu_utilization", return_value=0.90)
    @patch("autoscaler.AutoScaler.set_replica_count")
    def test_auto_scale_scale_up(self, mock_set_replica_count, mock_get_cpu_utilization):
        self.auto_scaler.auto_scale()
        mock_set_replica_count.assert_called_once_with(18)  # 0.90 * 20 = 18

    @patch("autoscaler.AutoScaler.get_cpu_utilization", return_value=0.70)
    @patch("autoscaler.AutoScaler.set_replica_count")
    def test_auto_scale_scale_down(self, mock_set_replica_count, mock_get_cpu_utilization):
        self.auto_scaler.auto_scale()
        mock_set_replica_count.assert_called_once_with(14)  # 0.70 * 20 = 14

if __name__ == "__main__":
    unittest.main()
