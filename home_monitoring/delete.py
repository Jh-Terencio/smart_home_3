from database import get_db_connection

def clear_all_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Deleting all rows from each table
    cursor.execute('DELETE FROM sensor_data')
    cursor.execute('DELETE FROM device_actions')
    cursor.execute('DELETE FROM sensors')
    
    # Optional: Reset the auto-increment primary key
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="sensor_data"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="device_actions"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="sensors"')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    clear_all_tables()
    print("All tables cleared.")
