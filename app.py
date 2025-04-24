# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

def connect_to_db():
    # Try to get database configuration from environment variables
    # Fall back to your current hardcoded values if not available
    host = os.environ.get('DB_HOST', 'sql.freedb.tech')
    user = os.environ.get('DB_USER', 'freedb_y_kilany')
    password = os.environ.get('DB_PASSWORD', 'P7QNvQ?sHy$z837')
    database = os.environ.get('DB_NAME', 'freedb_OscarProject')
    
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        country = request.form['country']
        
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user (username, email, gender, birthdate, country)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, gender or None, birthdate, country))
            conn.commit()
            cursor.close()
            conn.close()
            flash('User registered successfully!', 'success')
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
    
    return render_template('register.html')

@app.route('/add_nomination', methods=['GET', 'POST'])
def add_nomination():
    if request.method == 'POST':
        username = request.form['username']
        movie_title = request.form['movie_title']
        movie_release_date = request.form['movie_release_date']
        person_name = request.form['person_name']
        person_dob = request.form['person_dob']
        role = request.form['role']
        category = request.form['category']
        iteration = request.form['iteration']
        
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_nomination (username, movie_title, movie_release_date, person_name, person_dob, role, category, iteration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, movie_title, movie_release_date, person_name, person_dob, role, category, iteration))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Nomination added successfully!', 'success')
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
    
    return render_template('add_nomination.html')

@app.route('/view_nominations', methods=['GET', 'POST'])
def view_nominations():
    if request.method == 'POST':
        username = request.form['username']
        try:
            conn = connect_to_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT movie_title, movie_release_date, person_name, person_dob, role, category, iteration
                FROM user_nomination
                WHERE username = %s
            """, (username,))
            nominations = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Process results to add 1927 to iteration for display
            for nomination in nominations:
                try:
                    nomination['year'] = int(nomination['iteration']) + 1927
                except (ValueError, TypeError):
                    nomination['year'] = 'Unknown'
            
            return render_template('view_nominations.html', nominations=nominations, username=username)
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
    
    return render_template('view_nominations_form.html')

@app.route('/top_movies')
def top_movies():
    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT movie_title, movie_release_date, category, iteration, COUNT(*) AS nomination_count
            FROM user_nomination
            GROUP BY movie_title, movie_release_date, category, iteration
            ORDER BY nomination_count DESC
            LIMIT 10
        """)
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Process to add year
        for movie in movies:
            try:
                movie['year'] = int(movie['iteration']) + 1927
            except (ValueError, TypeError):
                movie['year'] = 'Unknown'
        
        return render_template('top_movies.html', movies=movies)
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
        return redirect(url_for('index'))

@app.route('/person_nominations', methods=['GET', 'POST'])
def person_nominations():
    if request.method == 'POST':
        person_name = request.form['person_name']
        person_dob = request.form['person_dob']
        try:
            conn = connect_to_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT role, COUNT(*) AS nominations,
                SUM(CASE WHEN won THEN 1 ELSE 0 END) AS oscars
                FROM nomination
                WHERE person_name = %s AND person_dob = %s
                GROUP BY role
            """, (person_name, person_dob))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('person_nominations_results.html', results=results, person_name=person_name)
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
    
    return render_template('person_nominations_form.html')

@app.route('/top_countries')
def top_countries():
    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.country, COUNT(*) AS win_count
            FROM nomination n
            JOIN person p ON n.person_name = p.name AND n.person_dob = p.dob
            WHERE n.category = 'Best Actor' AND n.won = TRUE
            GROUP BY p.country
            ORDER BY win_count DESC
            LIMIT 5
        """)
        countries = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('top_countries.html', countries=countries)
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
        return redirect(url_for('index'))

@app.route('/staff_by_country', methods=['GET', 'POST'])
def staff_by_country():
    if request.method == 'POST':
        country = request.form['country']
        try:
            conn = connect_to_db()
            cursor = conn.cursor(dictionary=True)
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
            staff = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('staff_by_country_results.html', staff=staff, country=country)
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
    
    return render_template('staff_by_country_form.html')

@app.route('/dream_team')
def dream_team():
    categories = {'Best Directing':'Director', 'Best Actor':'Actor', 'Best Actress': 'Actress', 
                  'Best Actor in a Supporting Role':'Supporting Actor', 
                  'Best Actress in a Supporting Role':'Supporting Actress', 
                  'Best Picture':'Producer', 'Best Music':'Composer'}
    
    team = {}
    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        
        for category, role in categories.items():
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
                team[role] = result['person_name']
            else:
                team[role] = "No living winner found"
        
        cursor.close()
        conn.close()
        return render_template('dream_team.html', team=team)
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
        return redirect(url_for('index'))

@app.route('/top_production_companies')
def top_production_companies():
    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.production_company, COUNT(*) AS oscar_wins
            FROM nomination n
            JOIN movie m ON n.movie_title = m.title AND n.movie_release_date = m.release_date
            WHERE n.won = TRUE
            GROUP BY m.production_company
            ORDER BY oscar_wins DESC
            LIMIT 5
        """)
        companies = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('top_production_companies.html', companies=companies)
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
        return redirect(url_for('index'))

@app.route('/non_english_movies')
def non_english_movies():
    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT DISTINCT m.title, m.release_date, m.language
            FROM movie m
            JOIN nomination n ON m.title = n.movie_title AND m.release_date = n.movie_release_date
            WHERE n.category == 'Best International Feature Film' AND n.won = TRUE
            ORDER BY m.release_date
        """)
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('non_english_movies.html', movies=movies)
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)