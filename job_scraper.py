import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog, messagebox, scrolledtext
from reportlab.pdfgen import canvas

def scrape_jobs(query, location, pages=1):
    base_url = "https://www.rozee.pk"
    jobs = []

    for page in range(1, pages + 1):
        search = query.replace(" ", "+")
        loc = location.replace(" ", "+")
        url = f"https://www.rozee.pk/job/jsearch/q/{search}/l/{loc}/page/{page}"
        print(f"[Scraping] {url}")

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        listings = soup.find_all("li", class_="job")
        if not listings:
            break

        for job in listings:
            title = job.find("a", class_="job-title")
            company = job.find("a", class_="company-name")
            loc = job.find("span", class_="location")
            date = job.find("span", class_="job-date")

            jobs.append({
                "Title": title.text.strip() if title else "N/A",
                "Company": company.text.strip() if company else "N/A",
                "Location": loc.text.strip() if loc else "N/A",
                "Posted": date.text.strip() if date else "N/A",
                "Link": base_url + title['href'] if title else "N/A"
            })
    return jobs

def start_scrape():
    job = job_entry.get().strip()
    loc = loc_entry.get().strip()
    try:
        pages = int(pages_entry.get())
        if pages <= 0: raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Pages must be a positive number.")
        return

    result_text.delete("1.0", END)
    global scraped_data
    scraped_data = scrape_jobs(job, loc, pages)

    if scraped_data:
        for job in scraped_data:
            result_text.insert(END, f"{job['Title']} at {job['Company']}\nLocation: {job['Location']}\nPosted: {job['Posted']}\nLink: {job['Link']}\n\n")
        messagebox.showinfo("Done", f"{len(scraped_data)} jobs found.")
    else:
        result_text.insert(END, "No jobs found.\n")

def export_csv():
    if not scraped_data:
        messagebox.showwarning("No Data", "Please scrape some jobs first.")
        return
    df = pd.DataFrame(scraped_data)
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if path:
        df.to_csv(path, index=False)
        messagebox.showinfo("Exported", f"Data saved to {path}")

def export_pdf():
    if not scraped_data:
        messagebox.showwarning("No Data", "Please scrape some jobs first.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
    if path:
        c = canvas.Canvas(path)
        c.setFont("Helvetica", 12)
        y = 800
        for job in scraped_data:
            lines = [
                f"Title: {job['Title']}",
                f"Company: {job['Company']}",
                f"Location: {job['Location']}",
                f"Posted: {job['Posted']}",
                f"Link: {job['Link']}",
                "-"*90
            ]
            for line in lines:
                c.drawString(40, y, line)
                y -= 20
                if y < 40:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 800
        c.save()
        messagebox.showinfo("Exported", f"PDF saved to {path}")

# === GUI ===
app = Tk()
app.title("📄 JobFinder Pro – Python Job Scraper")
app.geometry("800x600")

Label(app, text="Job Title:").pack(pady=2)
job_entry = Entry(app, width=40); job_entry.pack()

Label(app, text="Location (optional):").pack(pady=2)
loc_entry = Entry(app, width=40); loc_entry.pack()

Label(app, text="Pages to Scrape:").pack(pady=2)
pages_entry = Entry(app, width=10)
pages_entry.insert(0, "1")
pages_entry.pack()

Button(app, text="🔍 Scrape Jobs", command=start_scrape, bg="lightgreen").pack(pady=10)

result_text = scrolledtext.ScrolledText(app, width=100, height=20)
result_text.pack(padx=10, pady=10)

btn_frame = Frame(app)
btn_frame.pack(pady=5)

Button(btn_frame, text="⬇ Export as CSV", command=export_csv).pack(side=LEFT, padx=5)
Button(btn_frame, text="⬇ Export as PDF", command=export_pdf).pack(side=LEFT, padx=5)

Label(app, text="Developed by Hasan", fg="gray").pack(pady=5)

scraped_data = []
app.mainloop()
