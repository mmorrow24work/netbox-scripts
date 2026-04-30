# tests/test_device_count.py

from dcim.models import Device

def test_device_count_minimum():
    device_count = Device.objects.count()
    assert device_count >= 100, (
        f"Device count check failed: only {device_count} devices found (minimum is 100)"
    )
