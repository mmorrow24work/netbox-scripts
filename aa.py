from extras.scripts import Script
from django.utils import timezone
from dcim.models import Device

class CountDevicesJob(Script):
    class Meta:
        name = "Count Devices (DB)"
        description = "Counts devices using NetBox's internal database models and logs a date-stamped result."

    def run(self, data, commit):
        today = timezone.localdate().isoformat()
        count = Device.objects.count()
        self.log_success(f"{today} - Total devices in NetBox: {count}")
