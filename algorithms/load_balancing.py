"""
Blood Bank Load Balancing Algorithm

Distributes blood allocation across multiple
blood banks when possible.

The algorithm considers the amount of available
stock at each bank to avoid unnecessary
concentration of allocation.
"""


def calculate_bank_load(
    allocations
):
    """
    Calculate the number of units allocated
    from each blood bank.
    """

    bank_load = {}

    for allocation in allocations:

        bank_id = allocation["blood_bank_id"]

        units = allocation["units"]

        if bank_id not in bank_load:
            bank_load[bank_id] = 0

        bank_load[bank_id] += units

    return bank_load


def sort_banks_by_stock(banks):
    """
    Sort blood banks by available stock.

    Banks with greater available stock appear first.
    """

    return sorted(
        banks,
        key=lambda bank: bank["units"],
        reverse=True
    )


def distribute_units(banks, required_units):
    """
    Distribute required units across multiple banks.

    The algorithm takes stock from available banks
    until the requirement is fulfilled.
    """

    remaining_units = required_units

    allocations = []

    for bank in banks:

        if remaining_units <= 0:
            break

        units_to_allocate = min(
            remaining_units,
            bank["units"]
        )

        if units_to_allocate <= 0:
            continue

        allocations.append({
            "blood_bank_id": bank["blood_bank_id"],
            "blood_bank_name": bank["blood_bank_name"],
            "units": units_to_allocate
        })

        remaining_units -= units_to_allocate

    return allocations, remaining_units


def balance_allocation(
    banks,
    required_units
):
    """
    Perform load-balanced allocation.

    Banks are ordered according to available stock
    before distribution.
    """

    sorted_banks = sort_banks_by_stock(
        banks
    )

    return distribute_units(
        sorted_banks,
        required_units
    )