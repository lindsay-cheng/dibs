#!/usr/bin/env python3
"""Print every distinct company name in the data, so you copy exact names
into config.yaml. Run once: `python companies.py`."""
from dibs import fetch_listings

names = {
    l["company_name"]
    for l in fetch_listings()
    if l.get("active") and l.get("is_visible")
}
for n in sorted(names, key=str.lower):
    print(n)
