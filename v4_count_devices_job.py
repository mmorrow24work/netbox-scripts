from extras.scripts import Script
from django.utils import timezone
from dcim.models import Device, Site
from extras.models import JournalEntry

class v4CountDevicesJob(Script):
    class Meta:
        name = "Count Devices (DB)"
        description = "Counts devices and stores a dated history entry."

    def run(self, data, commit):
        today = timezone.localdate()
        count = Device.objects.count()

        # Log to the Job output (what you already see)
        self.log_success(f"{today} - Total devices in NetBox: {count}")

        # Anchor history to an existing Site
        site = Site.objects.get(name="netbox-docker")

        JournalEntry.objects.create(
            assigned_object=site,
            created_by=self.request.user,
            kind="info",
            comments=f"Device count on {today}: {count}"
        )
