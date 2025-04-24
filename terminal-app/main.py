import mysql.connector
from tabulate import tabulate

def connect_to_db():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_y_kilany",
        password="P7QNvQ?sHy$z837",
        database="freedb_OscarProject"
    )

def register_user(cursor, conn):
    print("=== Register New User ===")
    username = input("Username: ")
    email = input("Email: ")
    gender = input("Gender (Optional): ")
    birthdate = input("Birthdate (YYYY-MM-DD): ")
    country = input("Country: ")

    try:
        cursor.execute("""
            INSERT INTO user (username, email, gender, birthdate, country)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, gender or None, birthdate, country))
        conn.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def add_user_nomination(cursor, conn):
    print("=== Add User Nomination ===")
    username = input("Username: ")
    movie_title = input("Movie Title: ")
    movie_release_date = input("Release Date (YYYY-MM-DD): ")
    person_name = input("Full Name of Staff: ")
    person_dob = input("DOB of Staff (YYYY-MM-DD): ")
    role = input("Role: ")
    category = input("Category: ")
    iteration = input("Award Iteration (Year - 1927): ")

    try:
        cursor.execute("""
            INSERT INTO user_nomination (username, movie_title, movie_release_date, person_name, person_dob, role, category, iteration)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, movie_title, movie_release_date, person_name, person_dob, role, category, iteration))
        conn.commit()
        print("Nomination added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def view_user_nominations(cursor):
    print("=== View User Nominations ===")
    username = input("Username: ")
    cursor.execute("""
        SELECT movie_title, movie_release_date, person_name, person_dob, role, category, iteration
        FROM user_nomination
        WHERE username = %s
    """, (username,))
    results = cursor.fetchall()

    if not results:
        print("No nominations found for this user.")
        return

    # Process results to add 1927 to iteration
    processed_results = []
    for row in results:
        # Convert iteration to int, add 1927, and create new tuple
        processed_row = list(row)
        try:
            processed_row[6] = int(row[6]) + 1927  # Convert to actual year
        except (ValueError, TypeError):
            # In case the iteration is not a valid integer
            pass
        processed_results.append(processed_row)

    headers = ["Movie Title", "Release Date", "Person Name", "DOB", "Role", "Category", "Year"]
    print(tabulate(processed_results, headers=headers, tablefmt="grid"))

def top_nominated_movies(cursor):
    print("=== Top Nominated Movies by Users ===")
    cursor.execute("""
        SELECT movie_title, movie_release_date, category, iteration, COUNT(*) AS nomination_count
        FROM user_nomination
        GROUP BY movie_title, movie_release_date, category, iteration
        ORDER BY nomination_count DESC
        LIMIT 10
    """)
    results = cursor.fetchall()

    if not results:
        print("No nominations found.")
        return

    # Process results to add 1927 to iteration
    processed_results = []
    for row in results:
        processed_row = list(row)
        try:
            processed_row[3] = int(row[3]) + 1927  # Convert to actual year
        except (ValueError, TypeError):
            pass
        processed_results.append(processed_row)

    headers = ["Movie Title", "Release Date", "Category", "Year", "Nomination Count"]
    print(tabulate(processed_results, headers=headers, tablefmt="grid"))

def person_nominations_oscars(cursor):
    print("=== Nominations and Oscars for a Person ===")
    person_name = input("Full Name: ")
    person_dob = input("DOB (YYYY-MM-DD): ")
    cursor.execute("""
        SELECT role, COUNT(*) AS nominations,
        SUM(CASE WHEN won THEN 1 ELSE 0 END) AS oscars
        FROM nomination
        WHERE person_name = %s AND person_dob = %s
        GROUP BY role
    """, (person_name, person_dob))
    results = cursor.fetchall()

    if not results:
        print(f"No nominations found for {person_name} born on {person_dob}.")
        return

    headers = ["Role", "Nominations", "Oscars Won"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

def top_countries_best_actor(cursor):
    print("=== Top 5 Countries of Best Actor Winners ===")
    cursor.execute("""
        SELECT p.country, COUNT(*) AS win_count
        FROM nomination n
        JOIN person p ON n.person_name = p.name AND n.person_dob = p.dob
        WHERE n.category = 'Best Actor' AND n.won = TRUE
        GROUP BY p.country
        ORDER BY win_count DESC
        LIMIT 5
    """)
    results = cursor.fetchall()

    if not results:
        print("No Best Actor winners found.")
        return

    headers = ["Country", "Win Count"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

def nominated_staff_by_country(cursor):
    print("=== Nominated Staff by Country ===")
    country = input("Country: ")

    # Modified query to include categories
    cursor.execute("""
        SELECT n.person_name, n.person_dob, n.role,
               GROUP_CONCAT(DISTINCT n.category SEPARATOR ', ') AS categories,
               COUNT(*) AS nominations,
               SUM(CASE WHEN n.won THEN 1 ELSE 0 END) AS oscars
        FROM nomination n
        JOIN person p ON n.person_name = p.name AND n.person_dob = p.dob
        WHERE p.country = %s
        GROUP BY n.person_name, n.person_dob, n.role
        ORDER BY oscars DESC, nominations DESC
    """, (country,))

    results = cursor.fetchall()

    if not results:
        print(f"No nominated staff found from {country}.")
        return

    headers = ["Name", "DOB", "Role", "Categories", "Nominations", "Oscars Won"]
    print(tabulate(results, headers=headers, tablefmt="grid"))


def dream_team(cursor):
    print("=== Dream Team ===")
    categories = {'Best Directing':'Director', 'Best Actor':'Actor', 'Best Actress': 'Actress',
                  'Best Actor in a Supporting Role':'Supporting Actor',
                  'Best Actress in a Supporting Role':'Supporting Actress',
                  'Best Picture':'Producer', 'Best Music':'Composer'}

    print("\nCurrent Dream Team of Living Oscar Winners:")
    print("=" * 50)

    for (category, role) in categories.items():
        cursor.execute("""
            SELECT person_name, person_dob, COUNT(*) AS oscars
            FROM nomination
            WHERE category = %s AND won = TRUE AND (SELECT dod FROM person WHERE person.name = nomination.person_name AND person.dob = nomination.person_dob) IS NULL
            GROUP BY person_name, person_dob
            ORDER BY oscars DESC
            LIMIT 1
        """, (category,))
        result = cursor.fetchone()
        if result:
            print(f"{role}: {result[0]}")
        else:
            print(f"{role}: No living winner found")

def top_production_companies(cursor):
    print("=== Top 5 Production Companies by Oscars ===")
    cursor.execute("""
        SELECT m.production_company, COUNT(*) AS oscar_wins
        FROM nomination n
        JOIN movie m ON n.movie_title = m.title AND n.movie_release_date = m.release_date
        WHERE n.won = TRUE
        GROUP BY m.production_company
        ORDER BY oscar_wins DESC
        LIMIT 5
    """)
    results = cursor.fetchall()

    if not results:
        print("No production companies with Oscar wins found.")
        return

    headers = ["Production Company", "Oscar Wins"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

def non_english_oscar_movies(cursor):
    print("=== Non-English Oscar-Winning Movies ===")
    cursor.execute("""
        SELECT DISTINCT m.title, m.release_date, m.language
        FROM movie m
        JOIN nomination n ON m.title = n.movie_title AND m.release_date = n.movie_release_date
        WHERE m.language != 'English' AND n.won = TRUE
        ORDER BY m.release_date
    """)
    results = cursor.fetchall()

    if not results:
        print("No non-English Oscar-winning movies found.")
        return

    headers = ["Title", "Release Date", "Language"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

def main_menu():
    print("\n=== Oscar Project Menu ===")
    print("1. Register User")
    print("2. Add User Nomination")
    print("3. View User Nominations")
    print("4. Top Nominated Movies")
    print("5. Nominations & Oscars for a Person")
    print("6. Top Countries - Best Actor Winners")
    print("7. Nominated Staff by Country")
    print("8. Dream Team")
    print("9. Top Production Companies by Oscars")
    print("10. Non-English Oscar-Winning Movies")
    print("0. Exit")

def main():
    try:
        # Check if tabulate is installed, if not inform the user
        try:
            import tabulate
        except ImportError:
            print("The 'tabulate' package is required for this application.")
            print("Please install it using: pip install tabulate")
            return

        conn = connect_to_db()
        cursor = conn.cursor()

        while True:
            main_menu()
            choice = input("Select an option: ")

            if choice == '1':
                register_user(cursor, conn)
            elif choice == '2':
                add_user_nomination(cursor, conn)
            elif choice == '3':
                view_user_nominations(cursor)
            elif choice == '4':
                top_nominated_movies(cursor)
            elif choice == '5':
                person_nominations_oscars(cursor)
            elif choice == '6':
                top_countries_best_actor(cursor)
            elif choice == '7':
                nominated_staff_by_country(cursor)
            elif choice == '8':
                dream_team(cursor)
            elif choice == '9':
                top_production_companies(cursor)
            elif choice == '10':
                non_english_oscar_movies(cursor)
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()