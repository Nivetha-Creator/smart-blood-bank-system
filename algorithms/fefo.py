"""
FEFO Algorithm

FEFO = First Expire, First Out

Blood inventory with the earliest expiry date
is allocated first to reduce wastage.
"""


from datetime import date


def filter_valid_inventory(inventory):
    """
    Remove inventory that has already expired.

    Inventory expiring today is still considered valid
    for this prototype.
    """

    today = date.today()

    valid_inventory = []

    for item in inventory:

        expiry_date = date.fromisoformat(
            item["expiry_date"]
        )

        if expiry_date >= today:
            valid_inventory.append(item)

    return valid_inventory


def sort_by_expiry(inventory):
    """
    Sort valid blood inventory using FEFO.

    Earliest expiry date comes first.
    """

    return sorted(
        inventory,
        key=lambda item: item["expiry_date"]
    )


def apply_fefo(inventory):
    """
    Complete FEFO process:

    1. Remove expired blood
    2. Sort remaining blood by expiry date
    """

    valid_inventory = filter_valid_inventory(inventory)

    return sort_by_expiry(valid_inventory)