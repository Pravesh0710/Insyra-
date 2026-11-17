# Insyra
### Business Data Automation Platform

**Insyra** is a Python-based business automation project designed to simplify business data management and streamline data-related workflows.

The project aims to provide a centralized platform for working with business datasets, automating repetitive tasks, and making data handling more efficient.

## Project Overview

Insyra aims to bridge the gap between raw business data and meaningful information through automation and structured data management.

The initial development focuses on establishing a reliable Python and MySQL backend, with CSV data handling and file-upload functionality as part of the planned workflow.

## Objectives

- Simplify business data management.
- Automate repetitive data-related operations.
- Support CSV file uploads and processing.
- Integrate Python applications with MySQL.
- Build a foundation for scalable business automation.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| MySQL | Database management |
| MySQL Connector | Python–MySQL connectivity |
| python-dotenv | Environment variable management |
| Pandas | CSV data processing |

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Pravesh0710/Insyra-.git
```

### 2. Navigate to the project directory

```bash
cd Insyra-
```

### 3. Install dependencies

```bash
pip install mysql-connector-python python-dotenv pandas
```

### 4. Configure MySQL

Make sure MySQL Server is installed and running.

Create a database:

```sql
CREATE DATABASE insyra;
```

### 5. Configure environment variables

Create a `credentials.env` file and add your MySQL credentials:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=insyra
```

**Important:** Never upload actual database credentials to GitHub. Add `credentials.env` to `.gitignore`.

### 6. Run the application

```bash
python main.py
```

## Development Roadmap

- [x] Initial Python project setup
- [x] MySQL database connectivity
- [x] Environment-based database configuration
- [x] CSV data validation and processing
- [x] Automated business data operations (Profiling & Cleaning)
- [x] Database activity logging
- [ ] CSV file upload functionality
- [ ] Data visualization and reporting
- [ ] Dashboard integration
- [ ] Advanced automation features

## Security

- Store credentials in environment variables.
- Never commit passwords or sensitive configuration files.
- Use appropriate database permissions.
- Validate uploaded files before processing.

## Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Submit a pull request.

## Developer

**Pravesh Pacholi**

- GitHub: [@Pravesh0710](https://github.com/Pravesh0710)

---

If you find this project interesting, consider giving the repository a star.

**Insyra — Making Business Operations Smarter Through Automation.**
