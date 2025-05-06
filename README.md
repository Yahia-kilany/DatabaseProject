# Oscars Database Project

This project is a comprehensive database system for the Academy Awards (Oscars), designed as a university assignment. It covers data collection, normalization, database design, and a terminal application for Oscar-related queries.

---

## Project Overview

- **Database**: Stores detailed Oscar data from the 10th to the 96th iteration, including movies, people, awards, nominations, and user interactions.
- **Data Scraping**: Automatically scrapes Oscar data from Wikipedia for the specified years.
- **Data Normalization**: Cleans and standardizes raw data (dates, country names, etc.) for database consistency.
- **Terminal Application**: Allows users to interact with the database and execute complex queries from the command line.
- **Web Application (Optional)**: Flask-based interface for the same queries (see `app.py`).

---

## Features

- **User Registration**: Register new users with personal information.
- **User Nominations**: Add nominations for staff members (actors, directors, etc.) for specific movies.
- **View Nominations**: See all nominations made by a user.
- **Top Nominated Movies**: View the most-nominated movies by users, filtered by category and year.
- **Person Statistics**: See total nominations and Oscars for any director, actor, or singer.
- **Top Actor Birth Countries**: List the top 5 countries by number of Best Actor Oscar wins.
- **Staff by Country**: Show all nominated staff from a given country, with categories, nomination counts, and Oscar wins.
- **Dream Team**: Automatically assemble a hypothetical "best ever" movie cast and crew from living Oscar winners.
- **Top Production Companies**: List the top 5 companies by number of Oscars won.
- **Non-English Oscar Winners**: List all non-English movies that won an Oscar, with year and details.

---

## Database Schema

The normalized schema includes:

| Table          | Key Columns & Relationships                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| Movie          | title (PK), releaseDate, language, runtime, productionCompany                                                  |
| Person         | fullName (PK), DOB (PK), COB (Country of Birth), DOD (Date of Death)                                          |
| User           | username (PK), email, gender, birthdate, country                                                              |
| Award          | category (PK), iteration (PK), year                                                                           |
| Nomination     | roleNominationID (PK), title (FK), releaseDate (FK), fullName (FK), DOB (FK), role, category, iteration, won  |
| UserNomination | userRoleNomination (PK), username (FK), title (FK), releaseDate (FK), fullName (FK), DOB (FK), role, category, iteration |

---
- **See the Schema at `/docs/database/OscarProject.sql`**
- **ERD at `/docs/database/ERD.pdf`**
- **Relational Datamodel at `/docs/database/Project_Database Updated Relational`**
- **Additionally, there is an older attempt at the database schema stored in the folder:`docs/database/old/`**
## How It Works

1. **Scraping**: `data/scrapper.ipynb` collects Oscar data from Wikipedia for the required years.
2. **Normalization**: `data/data_cleanup.ipynb` cleans and standardizes names, dates, and countries to ensure data integrity.
3. **Database Setup**: Schema defined in `/docs/database/OscarProject.sql`, with a sample dump available in `/docs/freedb_OscarProject`.
4. **Terminal/Web App**: `terminal-app/main.py` (and/or `app.py` for Flask) provides an interface for all queries and features.

---

## Setup Instructions

1. **Clone the repository** and install dependencies:
`pip install -r requirements.txt`

2. **Set up the database** using the provided SQL schema and dump.
3. **Run the terminal app**:
`python main.py`

Or, **run the web app**:
`flask run`

text
(or use `gunicorn` for production as configured in `render.yaml`)

---

## Technologies Used

- Python (Flask, pandas, mysql-connector-python)
- MySQL/MariaDB
- Data scraping and cleaning scripts
- SQL for relational database design

---

## Repository Structure
```
.
├── data/                                 # Data scraping and cleanup notebooks
│   ├── Scrapper.ipynb                    # Jupyter notebook for scraping Oscar data from Wikipedia
│   └── Data_cleanup.ipynb                # Jupyter notebook for cleaning and normalizing the scraped data
|
├── docs/                          # Documentation files
│   └── Database/                 
│       ├── old/                  # Legacy or previous versions of database files
│       │   ├── OscarProject.sql  # Database Schema
│       │   ├── Project_Database Updated Rel... # Relational Model
│       │   └── Update ERD.pdf    # Entity-Relationship Diagram (updated)
│       └── dump/                 
│       │   ├──freedb_OscarProject.sql # dymp of the database
|
├── templates/                    # HTML templates For the falsk application at (app.py)
│   ├── add_nomination.html              # Form to add user nominations
│   ├── base.html                        # Base template for layout inheritance
│   ├── dream_team.html                  # Page showing a dream team (custom analysis)
│   ├── index.html                       # Home/landing page
│   ├── non_english_movies.html          # Report for non-English films
│   ├── person_nominations_form.html     # Form to query person nominations
│   ├── person_nominations_results.html  # Results for person nominations
│   ├── register.html                    # User registration form
│   ├── staff_by_country_form.html       # Form to filter staff by country
│   ├── staff_by_country_results.html    # Results of staff by country query
│   ├── top_countries.html               # Analytics on countries with most Oscars
│   ├── top_movies.html                  # Top Oscar-winning/nominated movies
│   ├── top_production_companies.html    # Leading production companies
│   ├── view_nominations.html            # Display all user nominations
│   ├── view_nominations_form.html       # Form to select nominations to view
|
├── terminal-app/               # Terminal-based client application
│   ├── build/main/               # Build artifacts for the terminal app
│   ├── main.exe                  # Executable file (generated via PyInstaller)
│   ├── main.py                   # Main script for launching the terminal app
│   ├── main.spec                 # PyInstaller spec file
|
├──app.py                        # Flask web application (optional interface)
├── render.yaml                  # Deployment configuration for Render or similar platform
├── requirements.txt             # Python dependencies
├── runtime.txt                  # Runtime environment (e.g., Python version for deployment)
```
---

## Credits

Developed as a university project for  to demonstrate full-stack data engineering, normalization, and application development with real-world data.
