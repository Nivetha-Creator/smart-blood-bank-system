from algorithms.search import search_blood_group
from algorithms.stock_analysis import classify_stock
from algorithms.nearest_bank import find_nearest_banks
from flask import Flask, render_template, request, redirect, url_for
from database import get_connection, initialize_database
from algorithms.allocation import allocate_blood
from algorithms.allocation import process_next_priority_request
app = Flask(__name__)

# Make sure database tables exist
initialize_database()


# --------------------------------------------------
# HOME / DASHBOARD
# --------------------------------------------------

@app.route("/")
def index():

    connection = get_connection()
    cursor = connection.cursor()

    # Total blood banks
    cursor.execute("SELECT COUNT(*) FROM blood_banks")
    total_banks = cursor.fetchone()[0]

    # Total available units
    cursor.execute("SELECT COALESCE(SUM(units), 0) FROM inventory")
    total_units = cursor.fetchone()[0]

    # Pending requests
    cursor.execute("""
        SELECT COUNT(*)
        FROM blood_requests
        WHERE status = 'PENDING'
    """)
    pending_requests = cursor.fetchone()[0]

    # Critical requests
    cursor.execute("""
        SELECT COUNT(*)
        FROM blood_requests
        WHERE urgency = 'CRITICAL'
        AND status = 'PENDING'
    """)
    critical_requests = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        total_banks=total_banks,
        total_units=total_units,
        pending_requests=pending_requests,
        critical_requests=critical_requests
    )

# --------------------------------------------------
# ADD BLOOD BANK
# --------------------------------------------------

@app.route("/add-bank", methods=["POST"])
def add_bank():

    name = request.form.get("name")
    location = request.form.get("location")
    contact = request.form.get("contact")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    print("Adding blood bank:")
    print("Name:", name)
    print("Location:", location)
    print("Contact:", contact)
    print("Latitude:", latitude)
    print("Longitude:", longitude)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO blood_banks
        (
            name,
            location,
            contact,
            latitude,
            longitude
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        location,
        contact,
        latitude,
        longitude
    ))

    connection.commit()

    print("Blood bank inserted successfully!")

    connection.close()

    return redirect(url_for("inventory"))

# --------------------------------------------------
# INVENTORY PAGE
# --------------------------------------------------
@app.route("/inventory")
def inventory():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            inventory.id,
            blood_banks.name AS blood_bank_name,
            blood_banks.location,
            inventory.blood_group,
            inventory.units,
            inventory.expiry_date
        FROM inventory
        JOIN blood_banks
        ON inventory.blood_bank_id = blood_banks.id
        ORDER BY inventory.expiry_date
    """)

    inventory_rows = cursor.fetchall()

    inventory_data = []

    for row in inventory_rows:
        item = dict(row)

        item["stock_level"] = classify_stock(
            item["units"]
        )

        inventory_data.append(item)

    cursor.execute("""
        SELECT *
        FROM blood_banks
        ORDER BY name
    """)

    blood_banks = cursor.fetchall()

    connection.close()

    return render_template(
        "inventory.html",
        inventory=inventory_data,
        blood_banks=blood_banks
    )
    # Get blood banks for dropdown
    cursor.execute("""
        SELECT *
        FROM blood_banks
        ORDER BY name
    """)

    blood_banks = cursor.fetchall()

    connection.close()

    return render_template(
        "inventory.html",
        inventory=inventory_data,
        blood_banks=blood_banks
    )


# --------------------------------------------------
# ADD INVENTORY
# --------------------------------------------------

@app.route("/add-inventory", methods=["POST"])
def add_inventory():

    blood_bank_id = request.form["blood_bank_id"]
    blood_group = request.form["blood_group"]
    units = request.form["units"]
    expiry_date = request.form["expiry_date"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO inventory
        (
            blood_bank_id,
            blood_group,
            units,
            expiry_date
        )
        VALUES (?, ?, ?, ?)
    """, (
        blood_bank_id,
        blood_group,
        units,
        expiry_date
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("inventory"))


# --------------------------------------------------
# BLOOD REQUEST PAGE
# --------------------------------------------------
@app.route("/request-blood", methods=["GET", "POST"])
def request_blood():

    if request.method == "POST":

        hospital_name = request.form.get("hospital_name")
        blood_group = request.form.get("blood_group")
        units_required = request.form.get("units_required")
        urgency = request.form.get("urgency")
        location = request.form.get("location")

        # Basic validation
        if not all([
            hospital_name,
            blood_group,
            units_required,
            urgency,
            location
        ]):
            return render_template(
                "request_blood.html",
                result={
                    "success": False,
                    "status": "INVALID_REQUEST",
                    "message": "Please fill in all fields."
                }
            )

        try:

            units_required = int(units_required)

            if units_required <= 0:
                raise ValueError

        except ValueError:

            return render_template(
                "request_blood.html",
                result={
                    "success": False,
                    "status": "INVALID_UNITS",
                    "message": "Units must be a positive number."
                }
            )

        # Save request
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO blood_requests
            (
                hospital_name,
                blood_group,
                units_required,
                urgency,
                location
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            hospital_name,
            blood_group,
            units_required,
            urgency,
            location
        ))

        request_id = cursor.lastrowid

        connection.commit()
        connection.close()

        print("================================")
        print("NEW BLOOD REQUEST")
        print("Request ID:", request_id)
        print("Hospital:", hospital_name)
        print("Blood Group:", blood_group)
        print("Units:", units_required)
        print("Urgency:", urgency)
        print("Location:", location)
        print("================================")

        # Run matching and allocation
        try:

            result = allocate_blood(request_id)

            print("ALLOCATION RESULT:")
            print(result)

        except Exception as error:

            print("ALLOCATION ERROR:")
            print(error)

            result = {
                "success": False,
                "status": "ALLOCATION_ERROR",
                "message": str(error)
            }

        return render_template(
            "request_blood.html",
            result=result
        )

    return render_template(
        "request_blood.html",
        result=None
    )

# --------------------------------------------------
# VIEW ALL REQUESTS
# --------------------------------------------------

@app.route("/requests")
def view_requests():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            hospital_name,
            blood_group,
            units_required,
            urgency,
            location,
            status,
            created_at
        FROM blood_requests
        ORDER BY
            CASE urgency
                WHEN 'CRITICAL' THEN 1
                WHEN 'URGENT' THEN 2
                WHEN 'NORMAL' THEN 3
                ELSE 4
            END,
            created_at ASC
    """)

    blood_requests = cursor.fetchall()

    print("================================")
    print("REQUESTS FOUND:", len(blood_requests))
    print("REQUEST DATA:", [dict(row) for row in blood_requests])
    print("================================")

    connection.close()

    return render_template(
        "requests.html",
        blood_requests=blood_requests
    )

# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------
@app.route("/process-next-request")
def process_next_request():

    result = process_next_priority_request()

    return render_template(
        "request_blood.html",
        result=result
    )
# --------------------------------------------------
# FIND NEAREST BLOOD BANKS
# --------------------------------------------------

@app.route("/nearest-banks")
def nearest_banks():

    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if not latitude or not longitude:
        return {
            "success": False,
            "message": "Please provide latitude and longitude."
        }

    try:
        latitude = float(latitude)
        longitude = float(longitude)

    except ValueError:
        return {
            "success": False,
            "message": "Latitude and longitude must be numbers."
        }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            location,
            latitude,
            longitude
        FROM blood_banks
        WHERE latitude IS NOT NULL
        AND longitude IS NOT NULL
    """)

    blood_banks = cursor.fetchall()

    connection.close()

    blood_banks = [
        dict(bank)
        for bank in blood_banks
    ]

    result = find_nearest_banks(
        latitude,
        longitude,
        blood_banks
    )

    return {
        "success": True,
        "banks": result
    }
@app.route("/search-blood")
def search_blood():

    blood_group = request.args.get("blood_group")

    if not blood_group:
        return {
            "found": False,
            "message": "Please select a blood group."
        }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            inventory.id,
            inventory.blood_group,
            inventory.units,
            inventory.expiry_date,
            blood_banks.name AS blood_bank_name,
            blood_banks.location
        FROM inventory
        JOIN blood_banks
        ON inventory.blood_bank_id = blood_banks.id
        WHERE inventory.units > 0
        ORDER BY inventory.blood_group
    """)

    inventory_rows = cursor.fetchall()

    connection.close()

    inventory_data = [
        dict(row)
        for row in inventory_rows
    ]

    result = search_blood_group(
        inventory_data,
        blood_group
    )

    if result:
        return {
            "found": True,
            "blood_group": result["blood_group"],
            "units": result["units"],
            "expiry_date": result["expiry_date"],
            "blood_bank_name": result["blood_bank_name"],
            "location": result["location"]
        }

    return {
        "found": False,
        "message": "No available stock found for this blood group."
    }

if __name__ == "__main__":
    app.run()
