"""
Binary Search Algorithm

Searches for a specific blood group in
sorted inventory.

Binary Search has O(log n) search complexity.
"""


def binary_search(
    inventory,
    blood_group
):
    """
    Search for a blood group using binary search.

    The inventory must be sorted alphabetically
    by blood_group.
    """

    left = 0

    right = len(inventory) - 1

    while left <= right:

        middle = (left + right) // 2

        current_group = inventory[middle][
            "blood_group"
        ]

        if current_group == blood_group:

            return inventory[middle]

        elif current_group < blood_group:

            left = middle + 1

        else:

            right = middle - 1

    return None


def sort_inventory(inventory):
    """
    Sort inventory by blood group before
    performing binary search.
    """

    return sorted(
        inventory,
        key=lambda item: item["blood_group"]
    )


def search_blood_group(
    inventory,
    blood_group
):
    """
    Sort inventory and perform binary search.
    """

    sorted_inventory = sort_inventory(
        inventory
    )

    return binary_search(
        sorted_inventory,
        blood_group
    )