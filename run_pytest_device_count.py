import pytest
import sys
from pathlib import Path

from extras.scripts import Script


class RunPytestDeviceCount(Script):
    """
    Runs a pytest test that validates the number of devices in NetBox.
    Fails if the device count is < 100.
    """

    class Meta:
        name = "Pytest: Validate minimum device count"
        description = "Runs pytest and fails if fewer than 100 devices exist in NetBox."

    def run(self, data, commit):

        # Locate the pytest file relative to this script
        # Adjust path if you store tests elsewhere
        pytest_file = Path(__file__).parent / "tests" / "test_device_count.py"

        if not pytest_file.exists():
            self.log_failure(f"Pytest file not found: {pytest_file}")
            return

        self.log_info(f"Running pytest: {pytest_file}")

        # Run pytest programmatically
        # -q = quiet
        # return code: 0=pass, 1=fail
        result = pytest.main([
            "-q",
            str(pytest_file)
        ])

        if result == 0:
            self.log_success("✅ Pytest device count check PASSED")
        else:
            self.log_failure("❌ Pytest device count check FAILED")
            raise RuntimeError("Pytest reported a failure")
