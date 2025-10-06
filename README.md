# Flask Inventory Management Web Application

This is a **Flask** web application to manage inventory across multiple locations (warehouses). It allows you to add products, locations, track product movements, and generate inventory reports in a user-friendly interface.

---

## Features

- Add, Edit, and View Products
- Add, Edit, and View Locations
- Record Product Movements (From/To locations)
- Generate Inventory Report with **balance quantity** per product per location
- Support for multiple warehouses and products

---

## Database Tables

- **Product**: `product_id` (PK), `name`
- **Location**: `location_id` (PK), `name`
- **ProductMovement**: `movement_id` (PK), `timestamp`, `from_location`, `to_location`, `product_id`, `qty`

---

## Use Cases / Sample Data

- **Products**: `Laptop`, `Mouse`, `Keyboard`, `Monitor`
- **Locations**: `Warehouse A`, `Warehouse B`, `Store 1`, `Store 2`
- **Sample Movements**:
  - Move `Laptop` to `Warehouse A`
  - Move `Mouse` to `Warehouse A`
  - Move `Laptop` from `Warehouse A` to `Warehouse B`
  - Perform **20 such movements** to simulate real-world activity
- **Report**: View product balance in each location in a grid with columns: **Product | Warehouse | Quantity**

---

## Screenshots

### Products Page
![Products Page](https://github.com/user-attachments/assets/8f2b061d-6645-4172-bfbf-51ca4e1b87f5)

### Locations Page
![Locations Page](https://github.com/user-attachments/assets/ef45ccc1-3d88-4957-97fe-14a48920f01e)

### Movements Page
![Movements Page](https://github.com/user-attachments/assets/164e1b63-a56f-4e7d-9733-f20103d528f8)

### Inventory Report
![Inventory Report](https://github.com/user-attachments/assets/25fe48a8-e06e-4140-acf1-af98ff1e918e)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/flask-inventory-app.git
cd flask-inventory-app
