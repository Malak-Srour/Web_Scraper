# Al Mayadeen Article Scraper

This repository contains a set of tools designed to scrape articles from Al Mayadeen's website via their sitemap XML files and analyze the volume of articles collected each month. The scraped articles are stored in JSON format, which can be easily accessed for further analysis or data processing.

## Project Components

- `web_scraper.py`: Main script for scraping articles from Al Mayadeen's sitemap and saving them as JSON.
- `nb.py`: A utility script to count and display the number of articles stored in each JSON file.
- `requirements.txt`: Specifies the Python packages required to run the scripts.

## Setup

Follow these steps to get your development environment set up:

### Prerequisites

Ensure Python 3.6+ is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://your-repository-link.git
   cd your-project-directory

2. **Install Required Python Libraries**:
   ```bash
    pip install -r requirements.txt

3. **Usage**:
    Running the Scraper:
    To scrape articles from the website, run
   ```bash
    python web_scraper.py

4. **Analyzing Extracted Data**:
    To count and report how many articles are in each JSON file:
   ```bash
    python nb.py
