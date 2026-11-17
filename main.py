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
            conn.close()
    except Exception as e:
        print("Status: MySQL Offline or Connection Failed.")
        print("Detail:", e)
    print("-----------------------\n")


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
        print(f"Removed {result['rows_removed']} rows in total.\n")


def main():
    print("=" * 55)
    print("   Welcome to Insyra - Business Automation Tool")
    print("=" * 55)

    while True:
        print("Select an option:")
        print(" 1. Profile Dataset (Inspect quality & anomalies)")
        print(" 2. Clean Dataset (Fix nulls, strip spaces, drop duplicates)")
        print(" 3. Check Database Connection")
        print(" 4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            run_profiler_flow()
        elif choice == "2":
            run_cleaner_flow()
        elif choice == "3":
            check_db_connection()
        elif choice == "4":
            print("\nExiting Insyra. Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()
