# 📄 JobFinder Pro – Python Job Scraper GUI (Rozee.pk)

A modern job scraping tool with a graphical interface built in Python. It scrapes job listings from Rozee.pk based on a user’s search query and location, then allows exporting the results in **CSV** and **PDF** formats. Designed for both portfolio and practical use!

---

## 🎯 Features

- 🔎 Scrapes jobs from [Rozee.pk](https://www.rozee.pk)
- ✅ User input for:
  - Job Title (e.g., Python, Flutter, Cybersecurity)
  - Location (e.g., Karachi, Lahore, Remote)
  - Number of pages to scrape
- 🧾 Real-time results displayed in GUI
- 📤 Export scraped results to:
  - **CSV** using `pandas`
  - **PDF** using `reportlab`
- 💻 Built with `Tkinter` and `BeautifulSoup`
- 🌐 Uses realistic headers for scraping (avoids blocks)

---

## 🛠️ Tech Stack

- Python 3
- `requests` – for HTTP requests
- `BeautifulSoup` – for parsing HTML
- `pandas` – for CSV export
- `reportlab` – for PDF generation
- `tkinter` – for GUI interface

---

## 📦 Installation

Install required libraries using pip:

```bash
pip install requests beautifulsoup4 pandas reportlab
