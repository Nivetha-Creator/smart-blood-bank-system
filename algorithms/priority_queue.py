"""
Priority Queue Algorithm

Handles pending blood requests based on urgency.

Priority:
CRITICAL → highest
URGENT   → medium
NORMAL   → lowest

For requests with the same urgency,
older requests are processed first.
"""

import heapq

from database import get_connection


PRIORITY = {
    "CRITICAL": 1,
    "URGENT": 2,
    "NORMAL": 3
}


def get_priority(urgency):
    """
    Convert urgency into a numerical priority.
    Lower number means higher priority.
    """

    return PRIORITY.get(
        urgency.upper(),
        4
    )


def get_pending_requests():
    """
    Retrieve all pending blood requests
    from the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM blood_requests
        WHERE status = 'PENDING'
    """)

    requests = cursor.fetchall()

    connection.close()

    return requests


def build_priority_queue(requests):
    """
    Create a priority queue using a min-heap.

    Priority is decided by:

    1. Urgency
    2. Request creation time
    """

    priority_queue = []

    for blood_request in requests:

        priority = get_priority(
            blood_request["urgency"]
        )

        heapq.heappush(
            priority_queue,
            (
                priority,
                blood_request["created_at"],
                blood_request["id"]
            )
        )

    return priority_queue


def get_next_request(priority_queue):
    """
    Remove and return the highest-priority
    request from the queue.
    """

    if not priority_queue:
        return None

    return heapq.heappop(
        priority_queue
    )


def get_next_pending_request():
    """
    Get the highest-priority pending request.

    Returns:
        Request ID
    """

    requests = get_pending_requests()

    if not requests:
        return None

    priority_queue = build_priority_queue(
        requests
    )

    next_request = get_next_request(
        priority_queue
    )

    if next_request is None:
        return None

    # Tuple structure:
    # (priority, created_at, request_id)

    return next_request[2]