#!/usr/bin/env python3

import os
import sys
import pynetbox

def main():
    netbox_url = os.getenv("NETBOX_URL", "http://localhost:8080")
    netbox_token = os.getenv("NETBOX_API_TOKEN")

    if not netbox_token:
        print("ERROR: NETBOX_API_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)

    nb = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    device_count = nb.dcim.devices.count()
    print(f"Total devices in NetBox: {device_count}")

if __name__ == "__main__":
    main()
