# 🌐 Scraper Project

## Overview

This project is a sophisticated web scraper designed to handle 15 different formats of websites and data. It utilizes the Poetry dependency manager for Python, AWS S3 for storage, and GitHub Actions for CI/CD and running the script and made it a cli tool easy to use and manage.

## Project Structure

The project is organized into various directories for better modularity and maintainability:

- **.github/workflows**: Contains GitHub Actions workflows for CI/CD.
- **depbot**: Main directory for the scraping and processing logic.
  - **jobs**: Contains job-related tasks.
    - **base**: Base job implementations.
    - **job_format**: Specific job formats.
    - **orchestration**: Orchestration logic for managing jobs.
    - **store**: Storage-related tasks.
  - **scraper**: Core scraping logic.
    - **base**: Base scraper implementations.
    - **core**: Core scraping functionalities.
    - **format**: Formatting utilities.
    - **utils**: Utility functions.
  - **scripts**: Additional scripts for various tasks.
  - **utils**: General utility functions.
- **dist**: Distribution directory for built packages.
- **tests**: Unit tests for the project.

## Key Features

- **Abstract Classes**:
  - The project uses abstract base classes to enforce a consistent interface across different components, ensuring robust and maintainable code.

- **OOP Principles**:
  - Emphasis on Object-Oriented Programming (OOP) principles to create modular, reusable, and extensible components.

- **Data Management**:
  - Metadata management for tracking scraping status and times, enabling efficient and effective scraping operations.

- **CLI Interface**:
  - A command-line interface (CLI) for easy interaction with the scraper, allowing users to specify formats to scrape, force re-scraping, or scrape all formats.

- **Integration with AWS**:
  - Utilizes AWS S3 for storage, ensuring scalable and reliable data storage solutions.

- **GitHub Actions**:
  - Automated CI/CD pipeline using GitHub Actions, enabling seamless integration, testing, and deployment.

## Craftsmanship Highlights

- **Abstract Classes for Consistency**:
  - Use of abstract classes like `BaseJob` to provide a clear and consistent interface for job implementations, promoting code uniformity and reducing the likelihood of errors.

- **Data Classes for Simplicity**:
  - Use of Python's `dataclass` for concise and readable data structure definitions, enhancing code clarity and reducing boilerplate.

- **Metadata Handling**:
  - Efficient metadata handling with JSON, enabling tracking of scraping status and facilitating incremental updates.

- **Logging and Error Handling**:
  - Comprehensive logging and error handling mechanisms to ensure smooth operation and easy debugging.

- **Scalable Architecture**:
  - Designed with scalability in mind, leveraging AWS Lambda and S3 to handle large-scale scraping tasks within the constraints of serverless computing.

- **Testing and Quality Assurance**:
  - Rigorous unit testing to ensure code reliability and maintainability, with tests organized in a dedicated `tests` directory.

- **Modular Codebase**:
  - Well-structured and modular codebase, making it easy to extend and maintain the project.

## Setup 

### Prerequisites

- Python 3.8+
- Poetry
- AWS CLI (for S3 interaction)
- GitHub account

### Usage

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. **Install dep**:
   ```bash
   poetry install
3. **Scrape Specific Formats:**
   ```bash
   poetry run python main.py -c dp1 dp2 dp3

