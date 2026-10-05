"""
Blood Allocation Engine

This module combines:

1. Blood-group compatibility
2. Expiry filtering
3. FEFO
4. Multi-bank allocation

The allocation engine is the main decision-making
component of the Smart Blood Bank System.
"""
from database import get_connection
from algorithms.load_balancing import balance_allocation
from algorithms.compatibility import get_compatible_groups
from algorithms.fefo import apply_fefo
from algorithms.priority_queue import get_priority
from algorithms.stock_analysis import classify_stock


def find_compatible_inventory(blood_group):
    """
    Find all available inventory that is compatible
    with the requested blood group.
    """

    compatible_groups = get_compatible_groups(
        blood_group
    )

    if not compatible_groups:
        return []

    connection = get_connection()
    cursor = connection.cursor()

    placeholders = ",".join(
        ["?"] * len(compatible_groups)
    )

    query = f"""
        SELECT
            inventory.id,
            inventory.blood_bank_id,
            blood_banks.name AS blood_bank_name,
            blood_banks.location,
            inventory.blood_group,
            inventory.units,
            inventory.expiry_date

        FROM inventory

        JOIN blood_banks
        ON inventory.blood_bank_id = blood_banks.id

        WHERE inventory.blood_group
        IN ({placeholders})

        AND inventory.units > 0
    """

    cursor.execute(
        query,
        compatible_groups
    )

    inventory = cursor.fetchall()

    connection.close()

    inventory = apply_fefo(inventory)

    for item in inventory:
        item["stock_level"] = classify_stock(
            item["units"]
        )

    return inventory

def calculate_allocation(inventory, required_units):
    """
    Calculate allocation across available blood banks.

    The load-balancing algorithm distributes the required
    units across suitable inventory records.
    """

    banks = []

    for item in inventory:

        banks.append({
            "blood_bank_id": item["blood_bank_id"],
            "blood_bank_name": item["blood_bank_name"],
            "units": item["units"]
        })

    allocations, remaining_units = balance_allocation(
        banks,
        required_units
    )

    # Add inventory information required
    # for database updates.

    final_allocations = []

    for allocation in allocations:

        matching_item = next(
            item
            for item in inventory
            if item["blood_bank_id"]
            == allocation["blood_bank_id"]
            and item["units"]
            >= allocation["units"]
        )

        final_allocations.append({
            "inventory_id": matching_item["id"],
            "blood_bank_id": allocation["blood_bank_id"],
            "blood_bank_name": allocation["blood_bank_name"],
            "blood_group": matching_item["blood_group"],
            "units": allocation["units"]
        })

    return final_allocations, remaining_units
def allocate_blood(request_id):
    """
    Allocate blood for a specific request.

    Process:

    Request
       ↓
    Read blood group + required units
       ↓
    Find compatible inventory
       ↓
    Remove expired stock
       ↓
    Apply FEFO
       ↓
    Calculate allocation
       ↓
    Update inventory
       ↓
    Record allocation
       ↓
    Update request status
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM blood_requests
        WHERE id = ?
        """,
        (request_id,)
    )

    blood_request = cursor.fetchone()

    connection.close()

    if not blood_request:

        return {
            "success": False,
            "status": "REQUEST_NOT_FOUND",
            "message": "Blood request not found."
        }


    if blood_request["status"] == "ALLOCATED":

        return {
            "success": False,
            "status": "ALREADY_ALLOCATED",
            "message": "This request has already been allocated."
        }


    required_units = blood_request["units_required"]

    blood_group = blood_request["blood_group"]


    # Find compatible inventory

    inventory = find_compatible_inventory(
        blood_group
    )


    # Calculate allocation

    allocations, remaining_units = calculate_allocation(
        inventory,
        required_units
    )


    # Check whether enough blood exists

    if remaining_units > 0:

        available_units = (
            required_units - remaining_units
        )

        return {
            "success": False,
            "status": "INSUFFICIENT_STOCK",
            "required_units": required_units,
            "available_units": available_units,
            "remaining_units": remaining_units,
            "allocations": allocations
        }


    # Enough blood is available.
    # Now update the database.

    connection = get_connection()
    cursor = connection.cursor()


    for allocation in allocations:

        # Reduce inventory

        cursor.execute(
            """
            UPDATE inventory

            SET units = units - ?

            WHERE id = ?
            """,
            (
                allocation["units"],
                allocation["inventory_id"]
            )
        )


        # Record allocation

        cursor.execute(
            """
            INSERT INTO allocations
            (
                request_id,
                blood_bank_id,
                blood_group,
                units_allocated
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                request_id,
                allocation["blood_bank_id"],
                allocation["blood_group"],
                allocation["units"]
            )
        )


    # Update request status

    cursor.execute(
        """
        UPDATE blood_requests

        SET status = 'ALLOCATED'

        WHERE id = ?
        """,
        (request_id,)
    )


    connection.commit()

    connection.close()


    return {
        "success": True,
        "status": "ALLOCATED",
        "allocated_units": required_units,
        "allocations": allocations
    }
def process_next_priority_request():
    """
    Find and process the highest-priority pending request.

    Priority:
    CRITICAL → URGENT → NORMAL

    If urgency is the same, older requests
    are processed first.
    """

    from algorithms.priority_queue import get_next_pending_request

    request_id = get_next_pending_request()

    if request_id is None:
        return {
            "success": False,
            "status": "NO_PENDING_REQUESTS",
            "message": "There are no pending blood requests."
        }

    result = allocate_blood(request_id)

    result["processed_request_id"] = request_id

    return result