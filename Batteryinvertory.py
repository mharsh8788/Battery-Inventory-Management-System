import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="harsh",  
    database="ev_battery_db"
)

cursor = conn.cursor()

def add_battery():
    battery_id = input("Enter Battery ID: ")
    battery_type = input("Enter Battery Type: ")
    battery_condition = input("Enter Battery Condition (Good/Average/Poor): ")

    try:
        cursor.execute("""
            INSERT INTO batteries (id, type, battery_condition, in_use, usage_count)
            VALUES (%s, %s, %s, %s, %s)
        """, (battery_id, battery_type, battery_condition, False, 0))
        conn.commit()
        print("Battery added successfully.")
    except mysql.connector.IntegrityError:
        print("Battery with this ID already exists.")

def swap_out():
    cursor.execute("SELECT * FROM batteries WHERE in_use = FALSE")
    rows = cursor.fetchall()

    if not rows:
        print("No available batteries.")
        return

    print("Available Batteries:")
    for b in rows:
        print(f"ID: {b[0]} | Type: {b[1]} | Condition: {b[2]}")

    selected_id = input("Enter the Battery ID to swap out: ")
    cursor.execute("SELECT * FROM batteries WHERE id = %s AND in_use = FALSE", (selected_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE batteries SET in_use = TRUE, usage_count = usage_count + 1
            WHERE id = %s
        """, (selected_id,))
        conn.commit()
        print(f"Battery {selected_id} has been swapped out.")
    else:
        print("Battery not found or already in use.")

def swap_in():
    cursor.execute("SELECT * FROM batteries WHERE in_use = TRUE")
    rows = cursor.fetchall()

    if not rows:
        print("No batteries are currently in use.")
        return

    print("Batteries in Use:")
    for b in rows:
        print(f"ID: {b[0]} | Type: {b[1]}")

    selected_id = input("Enter the Battery ID to return: ")
    cursor.execute("SELECT * FROM batteries WHERE id = %s AND in_use = TRUE", (selected_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE batteries SET in_use = FALSE WHERE id = %s", (selected_id,))
        conn.commit()
        print(f"Battery {selected_id} has been returned.")
    else:
        print("Battery not found or not in use.")

def view_logs():
    cursor.execute("SELECT * FROM batteries")
    rows = cursor.fetchall()

    if not rows:
        print("No battery records found.")
        return

    print("Battery Logs:")
    for b in rows:
        print(f"ID: {b[0]} | Type: {b[1]} | Condition: {b[2]} | In Use: {b[3]} | Usage Count: {b[4]}")

while True:
    print("\n--- Battery Inventory Menu ---")
    print("1. Add Battery")
    print("2. Swap Out Battery")
    print("3. Swap In Battery")
    print("4. View Logs")
    print("5. Exit")

    choice = input("Enter your choice (1–5): ")

    if choice == '1':
        add_battery()
    elif choice == '2':
        swap_out()
    elif choice == '3':
        swap_in()
    elif choice == '4':
        view_logs()
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice.")
