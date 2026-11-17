import os
from server.profiler import generate_profile_report, print_profile_summary
from server.cleaner import clean_dataset
import database.database as db


def check_db_connection():
    print("\n--- Database Status ---")
    try:
        conn = db.get_conn()
        if conn.is_connected():
            print("Status: Connected to MySQL successfully!")
            db.init_database()
            conn.close()
    except Exception as e:
        print("Status: MySQL Offline or Connection Failed.")
        print("Detail:", e)
    print("-----------------------\n")


def view_history_flow():
    print("\n--- Recent Dataset Cleaning History ---")
    logs = db.get_dataset_logs(limit=10)
    if not logs:
        print("No logs found (or MySQL is currently offline).\n")
        return

    print(f"{'ID':<4} | {'File Name':<30} | {'Before':<7} | {'After':<7} | {'Date/Time'}")
    print("-" * 75)
    for row in logs:
        file_name = os.path.basename(row['file_name'])[:28]
        created = str(row['created_at'])[:19]
        print(f"{row['id']:<4} | {file_name:<30} | {row['original_rows']:<7} | {row['cleaned_rows']:<7} | {created}")
    print("-" * 75 + "\n")


def run_profiler_flow():
    default_path = "server/netflix_customer_churn.csv"
    user_path = input(f"Enter CSV file path (Press Enter for default: '{default_path}'): ").strip()
    file_path = user_path if user_path else default_path

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist!\n")
        return

    print("\nAnalyzing dataset... Please wait.")
    report = generate_profile_report(file_path)

    if report:
        print_profile_summary(report)
        print()


def run_cleaner_flow():
    default_path = "server/netflix_customer_churn.csv"
    user_path = input(f"Enter CSV file path (Press Enter for default: '{default_path}'): ").strip()
    file_path = user_path if user_path else default_path

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist!\n")
        return

    print("\nStarting cleaning process...")
    result = clean_dataset(file_path)

    if result:
        print("\n[SUCCESS] Dataset cleaned and saved to:", result["cleaned_file"])
        print(f"Removed {result['rows_removed']} rows in total.")

        # Log action to MySQL database
        db.log_dataset_action(
            file_name=result["original_file"],
            original_rows=result["rows_before"],
            cleaned_rows=result["rows_after"],
            rows_removed=result["rows_removed"],
            saved_path=result["cleaned_file"]
        )
        print()


def main():
    print("=" * 55)
    print("   Welcome to Insyra - Business Automation Tool")
    print("=" * 55)

    # try initializing tables if DB is online
    db.init_database()

    while True:
        print("Select an option:")
        print(" 1. Profile Dataset (Inspect quality & anomalies)")
        print(" 2. Clean Dataset (Fix nulls, strip spaces, drop duplicates & log)")
        print(" 3. View Processing History (MySQL Logs)")
        print(" 4. Check Database Connection")
        print(" 5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            run_profiler_flow()
        elif choice == "2":
            run_cleaner_flow()
        elif choice == "3":
            view_history_flow()
        elif choice == "4":
            check_db_connection()
        elif choice == "5":
            print("\nExiting Insyra. Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please enter 1-5.\n")


if __name__ == "__main__":
    main()
