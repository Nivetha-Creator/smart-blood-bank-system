"""
Blood Stock Analysis Algorithm

Classifies blood inventory based on
available unit levels.
"""


def classify_stock(units):
    """
    Classify inventory into:

    CRITICAL
    LOW
    MODERATE
    HEALTHY
    """

    if units <= 0:
        return "CRITICAL"

    elif units <= 2:
        return "LOW"

    elif units <= 5:
        return "MODERATE"

    else:
        return "HEALTHY"


def analyze_inventory(inventory):
    """
    Analyze every inventory record and assign
    a stock-level classification.
    """

    analyzed_inventory = []

    for item in inventory:

        units = item["units"]

        analyzed_item = dict(item)

        analyzed_item["stock_level"] = classify_stock(
            units
        )

        analyzed_inventory.append(
            analyzed_item
        )

    return analyzed_inventory


def find_low_stock(inventory):
    """
    Return inventory records that need attention.
    """

    analyzed_inventory = analyze_inventory(
        inventory
    )

    return [
        item
        for item in analyzed_inventory
        if item["stock_level"] in [
            "CRITICAL",
            "LOW"
        ]
    ]


def calculate_total_units(inventory):
    """
    Calculate the total number of blood units.
    """

    return sum(
        item["units"]
        for item in inventory
    )