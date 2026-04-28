import csv,json
from connect import execute_query 

def create_table():
    execute_query("""
        CREATE TABLE IF NOT EXISTS contacts (
            username VARCHAR(100), 
            email VARCHAR(100),
            birthday DATE, 
            group_id VARCHAR(50),
            phones VARCHAR(30),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def insert_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")
    phone = input("Phone: ")

    query = "INSERT INTO contacts (username, email, birthday, group_id, phones) VALUES (%s, %s, %s, %s, %s)"
    execute_query(query, (name, email, birthday, group, phone))
    print("Contact added!")

def upload_csv(file='contacts.csv'):
    try:
        with open(file, encoding='utf-8') as f:
            reader = csv.reader(f)
            for r in reader: 
                if len(r) < 5: continue 
                execute_query("INSERT INTO contacts (username, email, birthday, group_id, phones) VALUES (%s, %s, %s, %s, %s)", 
                              (r[0], r[1], r[2], r[3], r[4]))
        print("CSV Data Uploaded.")
    except FileNotFoundError:
        print("File not found.")

def search_contact():
    val = input("Enter group or phone prefix: ") + '%'
    res = execute_query("SELECT * FROM contacts WHERE group_id LIKE %s OR phones LIKE %s", 
                        (val, val), fetch=True)
    for r in res: 
        print(f"Name: {r[0]}, Email: {r[1]}, Phone: {r[4]}")
    if not res: 
        print("No results.")

def searchgmail():
    val = input("Enter needed email: ")
    res = execute_query("SELECT * FROM contacts WHERE email LIKE %s", (val,), fetch=True)
    for r in res: 
        print(f"Name: {r[0]}, Email: {r[1]}, Phone: {r[4]}")
    if not res: 
        print("No results.")
    
def delete_contact():
    val = input("Enter Name or Phone to delete: ")
    execute_query("DELETE FROM contacts WHERE username=%s OR phones=%s", (val, val))
    print("Record removed.")

def sort_contact():
    val = input("Search filter (group/phone, leave empty for all): ") + '%'
    
    print("\nSort by:")
    print("1: Name")
    print("2: Birthday")
    print("3: Date Added")
    sort_choice = input("Choice: ")

    sort_map = {
        "1": "username",
        "2": "birthday",
        "3": "created_at"
    }
    sort_column = sort_map.get(sort_choice, "username")

    query = f"SELECT * FROM contacts WHERE group_id LIKE %s OR phones LIKE %s ORDER BY {sort_column} ASC"
    res = execute_query(query, (val, val), fetch=True)
    
    for r in res: 
        # Добавлена проверка на None для даты создания
        date_str = r[5].strftime('%Y-%m-%d') if r[5] else "N/A"
        print(f"[{date_str}] {r[0]} | B-day: {r[2]} | Phone: {r[4]}")
    
    if not res: 
        print("No results.")
def overview():
    page_size = 5 
    current_page = 0

    while True:
        offset = current_page * page_size
        
        query = "SELECT username, email, phones FROM contacts ORDER BY username LIMIT %s OFFSET %s"
        rows = execute_query(query, (page_size, offset), fetch=True)

        print(f"\n--- Page {current_page + 1} ---")
        
        if not rows:
            print("No more data found.")
        else:
            for r in rows:
                print(f"Name: {r[0]} | Email: {r[1]} | Phone: {r[2]}")

        print("----------------")
        choice = input("1: Next, 2: Prev, 3: Quit: ").strip()

        if choice == "1":
            if rows:
                current_page += 1
            else:
                print("You are at the end.")
        elif choice == "2":
            if current_page > 0:
                current_page -= 1
            else:
                print("You are on the first page.")
        elif choice == "3":
            break
        else:
            print("Invalid input.")

def export_to_json(filename='contacts_export.json'):
    query = "SELECT username, email, birthday, group_id, phones, created_at FROM contacts"
    rows = execute_query(query, fetch=True)

    if not rows:
        print("No data to export.")
        return

    data_list = []
    for r in rows:
        # Создаем словарь для каждой строки
        contact = {
            "username": r[0],
            "email": r[1],
            "birthday": str(r[2]) if r[2] else None, # Дату нужно перевести в строку
            "group_id": r[3],
            "phones": r[4],
            "created_at": r[5].strftime('%Y-%m-%d %H:%M:%S') if r[5] else None
        }
        data_list.append(contact)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=4, ensure_ascii=False)
        print(f"Successfully exported to {filename}")
    except Exception as e:
        print(f"Export failed: {e}")


def import_from_json():
    p = input("json file name:") + ".json"
    try:
        with open(p, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
    except FileNotFoundError:
        print("File contacts.json not found")
        return
    except json.JSONDecodeError:
        print("Invalid JSON format")
        return
    
    count = 0
    for contact in contacts:
        try:
            execute_query(
                "INSERT INTO contacts (username, email, birthday, group_id, phones) VALUES (%s, %s, %s, %s, %s)",
                (contact.get('username'), contact.get('email'), contact.get('birthday'), 
                 contact.get('group_id'), contact.get('phones'))
            )
            count += 1
        except Exception as e:
            print(f"Error inserting {contact.get('username')}: {e}")
    
    print(f"Imported {count} contacts from JSON to database")
if __name__ == "__main__":
    create_table()
    menu = {
        "1": insert_contact, 
        "2": upload_csv, 
        "3": search_contact, 
        "4": delete_contact,  
        "5": searchgmail,
        "6": sort_contact,
        "7": overview,
        "8": import_from_json,
        "9": export_to_json
    }
    
    while True:
        print("\n--- MENU ---")
        print("0: Stop, 1: Add, 2: CSV, 3: Search, 4: Delete, 5: Search by Email, 6: Sort ,7: Overview,8: import from json,9: export from json")
        cmd = input("Choice: ")
        if cmd == "0": 
            break
        action = menu.get(cmd)
        if action:
            action()
        else:
            print("Invalid choice")