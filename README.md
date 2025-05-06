# 🎬 Oscars Database Project

This project is a comprehensive database system for the Academy Awards (Oscars), designed as a university assignment. It includes end-to-end data engineering—scraping, cleaning, normalization, relational design—and full-featured interfaces for querying and reporting via both terminal and web applications.

## 📽️ Live Demo & Deployment
- 📺 [Video Walkthrough: Watch the demo on Google Drive]([#](https://drive.google.com/file/d/1agD2rOEuXquY5sSEeV-KhAegqjuWVBjq/view?usp=sharing))
- 🌐 [Live Web App: Try it out on Railway]((https://oscar-app-production.up.railway.app))

## 📌 Project Overview
- **Database**: Stores detailed Oscar data from the 10th to the 96th iteration, including movies, people, awards, nominations, and user interactions.
- **Data Scraping**: Automatically scrapes Oscar data from Wikipedia for the specified years.
- **Data Normalization**: Cleans and standardizes raw data (dates, country names, etc.) for consistency.
- **Terminal Application**: A CLI-based interface to run queries and view results.
- **Web Application**: Flask-based app with forms and reports for all major functionalities.

## ✨ Features
- 🔐 **User Registration**: Register users with name, email, and demographics.
- 📝 **User Nominations**: Submit custom nominations for movies and people.
- 👁️ **View Nominations**: View all nominations made by a user.
- 🎞️ **Top Nominated Movies**: Query top-nominated movies by year and category.
- 🧑‍🎤 **Person Statistics**: View total nominations and Oscar wins for staff (actors, directors, singers).
- 🌍 **Top Actor Birth Countries**: List the top 5 countries by number of Best Actor Oscar wins.
- 📍 **Staff by Country**: Show nominated staff by country with categories and stats.
- 🏆 **Dream Team**: Assemble the best ever living Oscar-winning cast & crew.
- 🏢 **Top Production Companies**: List top companies by Oscar wins.
- 🗣️ **Non-English Oscar Winners**: List all non-English Oscar-winning films with details.

## 🗄️ Database Schema
| Table              | Key Columns & Relationships                                                                 |
|--------------------|----------------------------------------------------------------------------------------------|
| **Movie**          | title (PK), releaseDate, language, runtime, productionCompany                               |
| **Person**         | fullName (PK), DOB (PK), COB (Country of Birth), DOD (Date of Death)                         |
| **User**           | username (PK), email, gender, birthdate, country                                            |
| **Award**          | category (PK), iteration (PK), year                                                          |
| **Nomination**     | roleNominationID (PK), title (FK), releaseDate (FK), fullName (FK), DOB (FK), role, category, iteration, won |
| **UserNomination** | userRoleNomination (PK), username (FK), title (FK), releaseDate (FK), fullName (FK), DOB (FK), role, category, iteration |

## 📄 See:
- **SQL Schema**: `/docs/database/OscarProject.sql`
- **ERD**: `/docs/database/ERD.pdf`
- **Relational Model**: `/docs/database/Project_Database Updated Relational`
- **Legacy Schema**: `/docs/database/old/`

## ⚙️ How It Works
- **Scraping**: `data/Scrapper.ipynb` scrapes Oscar data from Wikipedia.
- **Normalization**: `data/Data_cleanup.ipynb` standardizes names, dates, and countries.
- **Database Setup**: Schema in `/docs/database/OscarProject.sql`, with a dump in `/docs/freedb_OscarProject`.
- **Applications**:
  - **Terminal**: `terminal-app/main.py`
  - **Web (Flask)**: `app.py`
## How It Works

1. **Scraping**: `data/scrapper.ipynb` collects Oscar data from Wikipedia for the required years.
2. **Normalization**: `data/data_cleanup.ipynb` cleans and standardizes names, dates, and countries to ensure data integrity.
3. **Database Setup**: Schema defined in `/docs/database/OscarProject.sql`, with a sample dump available in `/docs/freedb_OscarProject`.
4. **Terminal/Web App**: `terminal-app/main.py` (and/or `app.py` for Flask) provides an interface for all queries and features.

---

## 🚀 Setup Instructions

1. **Clone the repository** and install dependencies:
`pip install -r requirements.txt`

2. **Set up the database** using the provided SQL schema and dump.
3. **Run the terminal app**:
`python main.py`

Or, **run the web app**:
`flask run`

(or use `gunicorn` for production as configured in `render.yaml`)

---

## 🛠️ Technologies Used

- Python (Flask, pandas, mysql-connector-python)
- MySQL/MariaDB
- Jupyter Notebooks for data processing
- SQL for relational database design and queries

---

## 📁 Repository Structure
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
│       │   ├──freedb_OscarProject.sql # dump of the database
|
├── templates/                    # HTML templates For the flask application at (app.py)
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
## 🧑‍🏫 Credits
This project was developed as part of the CSCE2501 – Fundamentals of Database Systems course under the instruction of Dr. Hossam Sharara.
It demonstrates full-stack data engineering skills including data scraping, normalization, relational database design, and both terminal and web application development using real-world data from the Academy Awards.
---
## 📜 License
This project is for educational use. If you wish to reuse or extend it, please contact the author or check with the university guidelines.

