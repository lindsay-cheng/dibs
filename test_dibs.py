"""Minimal self-check for the matching logic — the part that silently breaks.
Run: `python test_dibs.py` (no framework needed)."""
from dibs import normalize, matches, load_watchlist

# normalize: casing, corp suffixes, punctuation
assert normalize("Jane Street, Inc.") == "jane street"
assert normalize("Two Sigma") == "two sigma"
assert normalize("Costco") == "costco"  # "co" only stripped on word boundary

wl = load_watchlist({"companies": [
    "Stripe",
    {"name": "Google", "roles": ["software", "swe"]},
]})

def L(company, title):
    return {"company_name": company, "title": title}

assert matches(L("Stripe Inc.", "Anything"), wl)               # bare -> any role
assert matches(L("Google LLC", "Software Engineer Intern"), wl)  # keyword hit
assert not matches(L("Google", "Product Manager"), wl)           # keyword miss
assert not matches(L("Airbnb", "Software Engineer"), wl)         # not on list

# a name that normalizes to "" must never match everything
assert load_watchlist({"companies": ["!!!"]}) == []
assert not matches(L("Anybody", "Any role"), load_watchlist({"companies": ["!!!"]}))

print("ok")
