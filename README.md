# 🌤️ ETL Weather Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Pytest](https://img.shields.io/badge/Tests-Pytest-green)
![CI](https://github.com/yourusername/etl-weather-pipeline/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-yellow)

ETL Weather Pipeline is a **Python-based ETL project** that extracts live weather data from the **OpenWeather API**,  
transforms it into a structured format, and loads it into a **PostgreSQL database** for further analysis.

The entire project runs inside **Docker Compose**, includes **Pytest tests**, **flake8 linting**,  
and a **GitHub Actions CI pipeline** for automation.

---

## ⚙️ Project Architecture

### 🧩 1. Extract (Extractor)

- Retrieves real-time weather data from [OpenWeather API](https://openweathermap.org/api)
- Uses `requests` and environment variables to securely access the API.

### 🔄 2. Transform (Transformer)

- Cleans and structures the data into a **Pandas DataFrame**.
- Adds timestamps and prepares the dataset for database insertion.

### 💾 3. Load (DB Loader)

- Creates the database table if it doesn’t exist.
- Inserts data into PostgreSQL using `psycopg2` and `execute_values` for fast batch inserts.

---

## 🐳 Docker Infrastructure

The project uses **two containers** defined in `docker-compose.yml`:

| Service        | Description                                              |
| -------------- | -------------------------------------------------------- |
| `etl_app`      | Runs the Python ETL script (extract → transform → load). |
| `etl_postgres` | Hosts the PostgreSQL database where results are stored.  |

### 🚀 Run the Project

```bash
docker-compose up --build
```

After starting:

- The **ETL container** will fetch one record and then stop automatically.
- The **PostgreSQL container** remains running so you can inspect the data.

---

## 🧠 Checking Data in the Database

Once the containers are running, you can connect to the database using `psql` or `pspg`:

```bash
docker exec -it etl_postgres psql -U postgres -d etl_demo
```

Then run:

```sql
SELECT * FROM current_temperature;
```

---

## 🧪 Testing & Linting

### Run tests locally:

```bash
pytest -v
```

### Run code linting:

```bash
flake8 app tests --max-line-length=100 --ignore=E203,W503
```

---

## ⚙️ Continuous Integration (CI)

The project includes a **GitHub Actions** workflow (`.github/workflows/ci.yml`) that:

- Runs on each `push` or `pull request`.
- Installs dependencies using `uv`.
- Executes all **pytest** tests.
- Runs **flake8** for code quality checks.

---

## 🧰 Tech Stack

| Tool                 | Purpose                   |
| -------------------- | ------------------------- |
| **Python 3.12**      | Core language             |
| **Pandas**           | Data transformation       |
| **Requests**         | API communication         |
| **Psycopg2**         | PostgreSQL integration    |
| **Docker & Compose** | Containerized environment |
| **Pytest**           | Testing framework         |
| **Flake8**           | Linting and code style    |
| **GitHub Actions**   | Continuous Integration    |

---

## 📁 Project Structure

```
.
├── app/
│   ├── extractor.py
│   ├── transformer.py
│   ├── db_loader.py
│   ├── main.py
│   └── config.py
├── tests/
│   ├── test_extractor.py
│   ├── test_transformer.py
│   └── test_db_loader.py
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env
└── README.md
```

---

## 💡 Future Improvements

- Automate data extraction on a schedule (e.g. every hour).
- Add historical weather trend visualization.
- Implement logging dashboard with Grafana & Prometheus.
- Add unit + integration coverage reports to CI.

---

## 🏁 License

This project is licensed under the **MIT License** — feel free to use and modify it.

---

Made with ❤️ by [Your Name](https://github.com/yourusername)
