# Test pynetbox outside of Netbox

```bash
python3 -m venv ./netbox-venv
source ./netbox-venv/bin/activate
pip install pynetbox
export NETBOX_URL="http://localhost:8080"
export NETBOX_API_TOKEN="nbt_GBMhCDhhfGyg.EnjV1Yc2fYbWUq3oQpecIJTP7B82aMMKSsr6cOOW"
```


```bash
mickm@ubuntu24-2:~/git/netbox-docker$ python3 -m venv netbox-venv
mickm@ubuntu24-2:~/git/netbox-docker$ source netbox-venv/bin/activate
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$ pip install pynetbox
Collecting pynetbox
  Downloading pynetbox-7.6.1-py3-none-any.whl.metadata (5.2 kB)
Collecting requests<3.0,>=2.20.0 (from pynetbox)
  Using cached requests-2.33.1-py3-none-any.whl.metadata (4.8 kB)
Collecting packaging (from pynetbox)
  Downloading packaging-26.2-py3-none-any.whl.metadata (3.5 kB)
Collecting charset_normalizer<4,>=2 (from requests<3.0,>=2.20.0->pynetbox)
  Using cached charset_normalizer-3.4.7-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
Collecting idna<4,>=2.5 (from requests<3.0,>=2.20.0->pynetbox)
  Using cached idna-3.13-py3-none-any.whl.metadata (8.0 kB)
Collecting urllib3<3,>=1.26 (from requests<3.0,>=2.20.0->pynetbox)
  Using cached urllib3-2.6.3-py3-none-any.whl.metadata (6.9 kB)
Collecting certifi>=2023.5.7 (from requests<3.0,>=2.20.0->pynetbox)
  Using cached certifi-2026.4.22-py3-none-any.whl.metadata (2.5 kB)
Downloading pynetbox-7.6.1-py3-none-any.whl (39 kB)
Using cached requests-2.33.1-py3-none-any.whl (64 kB)
Downloading packaging-26.2-py3-none-any.whl (100 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.2/100.2 kB 3.3 MB/s eta 0:00:00
Using cached certifi-2026.4.22-py3-none-any.whl (135 kB)
Using cached charset_normalizer-3.4.7-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (216 kB)
Using cached idna-3.13-py3-none-any.whl (68 kB)
Using cached urllib3-2.6.3-py3-none-any.whl (131 kB)
Installing collected packages: urllib3, packaging, idna, charset_normalizer, certifi, requests, pynetbox
Successfully installed certifi-2026.4.22 charset_normalizer-3.4.7 idna-3.13 packaging-26.2 pynetbox-7.6.1 requests-2.33.1 urllib3-2.6.3
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$ 
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$ export NETBOX_URL="http://localhost:8080"
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$ export NETBOX_API_TOKEN="nbt_GBMhCDhhfGyg.EnjV1Yc2fYbWUq3oQpecIJTP7B82aMMKSsr6cOOW"
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$ cat count_devices.py
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
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$ python3 count_devices.py
Total devices in NetBox: 90
(netbox-venv) mickm@ubuntu24-2:~/git/netbox-docker$
```
