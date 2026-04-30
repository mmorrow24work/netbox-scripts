from extras.scripts import Script
from django.utils import timezone
import os
import pynetbox

class CountDevicesJob(Script):
    class Meta:
        name = "Count Devices (API)"
        description = "Counts devices via the /api/dcim/devices/ endpoint and logs a date-stamped result."

    def run(self, data, commit):
        # Date in ISO format (e.g. 2026-04-30)
        today = timezone.localdate().isoformat()

        netbox_url = os.getenv("NETBOX_URL", "http://localhost:8080")
        token = os.getenv("NETBOX_API_TOKEN")

        if not token:
            self.log_failure("NETBOX_API_TOKEN environment variable not set")
            return

        nb = pynetbox.api(netbox_url, token=token)

        try:
            count = nb.dcim.devices.count()
        except Exception as exc:
            self.log_failure(f"Failed to query devices count via API: {exc}")
            return

        # Your requested output format
        self.log_success(f"{today} - Total devices in NetBox: {count}")
