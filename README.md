# Smart Blood Bank Allocation & Emergency Blood Matching System

A web-based blood bank management and emergency blood allocation system developed using Python, Flask, SQLite, HTML, CSS, and JavaScript.

The system helps manage blood inventory, process blood requests, identify compatible blood groups, prioritize emergency requests, and efficiently allocate available blood units.

## Features

- Blood bank registration and management
- Blood inventory management
- Blood group compatibility checking
- Emergency blood request processing
- Priority-based request handling
- FEFO (First Expiry, First Out) inventory allocation
- Stock-level classification
- Blood group search using Binary Search
- Nearest blood bank detection using geographical distance
- Load-based blood allocation
- SQLite database integration
- Responsive web interface
- Light/Dark mode

## Algorithms Used

The system integrates multiple algorithms to improve blood allocation and decision-making:

1. **Blood Group Compatibility**
   - Identifies compatible donor blood groups for a recipient.

2. **Priority Queue**
   - Gives higher priority to CRITICAL and URGENT blood requests.

3. **FEFO (First Expiry, First Out)**
   - Prioritizes blood units that are closest to their expiry date.

4. **Stock Level Analysis**
   - Classifies inventory as Healthy, Moderate, Low, or Critical.

5. **Load Balancing**
   - Distributes required blood units efficiently across available blood banks.

6. **Binary Search**
   - Searches inventory for a specific blood group.

7. **Nearest Blood Bank**
   - Calculates geographical distance to identify nearby blood banks.

## Technologies Used
- **Python**
- **Flask**
- **SQLite**
- **HTML5**
- **CSS3**
- **JavaScript**

## Project Structure
Smart-Blood-Bank-System/
│
├── app.py
├── database.py
│
├── algorithms/
│   ├── __init__.py
│   ├── compatibility.py
│   ├── priority_queue.py
│   ├── fefo.py
│   ├── allocation.py
│   ├── nearest_bank.py
│   ├── stock_analysis.py
│   ├── load_balancing.py
│   └── search.py
│
├── templates/
│   ├── index.html
│   ├── inventory.html
│   ├── request_blood.html
│   └── requests.html
│
└── static/
    ├── style.css
    └── script.js
    
How It Works
The system allows blood banks to register their available inventory. Hospitals can submit blood requests by specifying the required blood group, number of units, urgency, and location.
When a request is submitted, the system uses multiple algorithms to determine compatible blood, prioritize the request, select suitable inventory based on expiry dates, and allocate available units efficiently.

Future Enhancements
Real-time blood availability tracking
Hospital and blood bank authentication
Email/SMS emergency notifications
Interactive map integration
Cloud database support
Mobile application
Advanced analytics and reporting
Project Objective

The main objective of this project is to develop an intelligent blood bank management system that can improve emergency blood allocation, reduce processing time, and support efficient utilization of available blood resources.

Author
Nivetha M
B.E. Computer Science Engineering
