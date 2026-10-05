"""
Blood Group Compatibility Algorithm

This module determines which donor blood groups
can be considered compatible with a requested
recipient blood group for this prototype.
"""


COMPATIBILITY = {
    "O-": [
        "O-"
    ],

    "O+": [
        "O+",
        "O-"
    ],

    "A-": [
        "A-",
        "O-"
    ],

    "A+": [
        "A+",
        "A-",
        "O+",
        "O-"
    ],

    "B-": [
        "B-",
        "O-"
    ],

    "B+": [
        "B+",
        "B-",
        "O+",
        "O-"
    ],

    "AB-": [
        "AB-",
        "A-",
        "B-",
        "O-"
    ],

    "AB+": [
        "AB+",
        "AB-",
        "A+",
        "A-",
        "B+",
        "B-",
        "O+",
        "O-"
    ]
}


def get_compatible_groups(blood_group):
    """
    Return all compatible donor blood groups
    for the requested blood group.
    """

    return COMPATIBILITY.get(blood_group, [])


def is_compatible(donor_group, recipient_group):
    """
    Check whether a donor blood group is compatible
    with the requested recipient blood group.
    """

    compatible_groups = get_compatible_groups(recipient_group)

    return donor_group in compatible_groups