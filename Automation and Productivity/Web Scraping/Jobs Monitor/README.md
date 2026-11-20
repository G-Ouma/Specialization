# Web Scraping – Jobs Monitor

## 1. Project Overview

This project demonstrates how Python can be used to automate the extraction of information from public websites and save the collected data in CSV format.

The project uses [Quotes to Scrape](https://quotes.toscrape.com/) as a practice target because it provides a website specifically designed for learning web scraping.

The exercise simulates a potential business use case where HR managers at mid-sized companies in Nairobi monitor competitor job postings to identify:

- Skills and qualifications in demand.
- Job titles and emerging roles.
- Salary ranges offered by competitors.
- Changes in recruitment trends.

**Note:** The current implementation scrapes quotes rather than actual job advertisements. It demonstrates the extraction, pagination and CSV-export techniques that could be adapted for an authorised jobs board.

## 2. Project Objectives

- Establish an HTTP connection to a public website.
- Parse HTML content using BeautifulSoup.
- Extract multiple fields from individual website listings.
- Navigate multiple pages automatically through pagination.
- Export extracted information into a structured CSV file.
- Understand how web scraping can support business intelligence.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Requests | Retrieve webpage HTML |
| BeautifulSoup4 | Parse HTML and extract information |
| CSV | Store extracted information |
| VS Code | Development environment |

## 4. Project Structure

```text
Jobs Monitor/
│
├── scraper.py
├── scraped_quotes.csv
├── requirements.txt
└── README.md
```

## 5. Installation and Setup

### Prerequisites

- Python 3 installed.
- A Python virtual environment.
- Visual Studio Code or another Python editor.

### Install dependencies

Activate the existing virtual environment and install the required packages:


```bash
pip install -r requirements.txt
```

### Run the scraper

Execute:

```bash
python scraper.py
```

The script connects to Quotes to Scrape, extracts information from all available pages and saves the results in `scraped_quotes.csv`.

## 6. Data Extraction

The scraper extracts four fields from each quote:

| Field | Description |
|---|---|
| Quote | The actual text of the quote |
| Author | Name of the person attributed to the quote |
| Tags | Categories associated with the quote |
| Source URL | URL of the page containing the quote |

The scraper uses the following HTML selectors:

| HTML selector | Extracted information |
|---|---|
| `div.quote` | Individual quote container |
| `span.text` | Quote text |
| `small.author` | Author |
| `a.tag` | Associated tags |

### Pagination

The website displays ten quotes per page.

The script uses a `while` loop to navigate successive pages until it encounters an unsuccessful HTTP response or a page without quote containers.

This allows the scraper to collect all 100 available quotes without manually visiting individual pages.

## 7. CSV Export

The extracted records are saved in:

`scraped_quotes.csv`

The CSV file contains four columns corresponding to the extracted fields.

The script uses UTF-8 with BOM (`utf-8-sig`) to improve compatibility when opening the CSV file in Microsoft Excel.

The file is opened in write mode (`w`). Consequently, each execution creates a fresh dataset and overwrites the previous CSV contents.

For a production monitoring application, historical records should instead be preserved using unique identifiers, timestamps and duplicate detection.

## 8. Adapting the Scraper for a Live Jobs Board

For a client who has authorised access to a live jobs board, the existing script could be adapted to extract recruitment information rather than quotes.

### Step 1: Confirm access and inspect the website

Obtain the client's written authorisation and identify the permitted pages or endpoints.

Inspect the website's HTML structure to determine the elements containing job information.

### Step 2: Identify the relevant fields

The extraction logic could be modified to collect:

| Field | Description |
|---|---|
| Job Title | Advertised position |
| Company | Recruiting organisation |
| Location | Job location |
| Salary Range | Advertised salary, where available |
| Required Skills | Skills and qualifications requested |
| Employment Type | Full-time, part-time or contract |
| Date Posted | Original advertisement date |
| Job URL | Link to the original advertisement |
| Date Collected | Date the scraper collected the listing |

Fields should only be collected where they are available and permitted by the client.

### Step 3: Update the HTML selectors

Replace the existing quote selectors with selectors matching the jobs board.

For example, a hypothetical jobs board might contain:

```html
<div class="job-listing">
    <h2 class="job-title">Data Analyst</h2>
    <span class="company">ABC Company</span>
    <span class="location">Nairobi</span>
    <span class="salary">KES 80,000 - 120,000</span>
</div>
```

The corresponding extraction logic could look like:

```python
job_title = listing.find(
    "h2", class_="job-title"
).get_text(strip=True)

company = listing.find(
    "span", class_="company"
).get_text(strip=True)

location = listing.find(
    "span", class_="location"
).get_text(strip=True)

salary = listing.find(
    "span", class_="salary"
).get_text(strip=True)
```

These selectors are illustrative. Actual selectors must be identified from the client's website.

### Step 4: Adapt pagination

The existing pagination logic can be modified to follow the jobs board's pagination links.

Some websites use numbered pages, while others use a Next button, cursor-based pagination or an authorised API.

The scraper should follow the pagination method supported by the client.

### Step 5: Preserve historical data

Unlike the practice scraper, a real recruitment monitoring application should not simply overwrite previous records.

It could introduce:

- Unique job identifiers.
- Duplicate detection using job URLs or a combination of job attributes.
- Collection timestamps.
- First-seen and last-seen dates.
- Detection of removed or updated advertisements.

This would allow HR managers to monitor recruitment trends over time.

### Step 6: Analyse recruitment trends

Once the data has been collected, Python libraries such as Pandas could be introduced to analyse:

- Most frequently requested technical skills.
- Salary ranges across competing organisations.
- Most advertised job positions.
- Recruitment activity by location.
- Changes in demand for particular qualifications.

The resulting information could be presented through charts or a dashboard.

## 9. Ethical and Legal Considerations

Before scraping a live jobs board, the following considerations should be reviewed.

### 9.1 Authorisation and Website Terms

- Obtain written permission from the client specifying the permitted scraping activities.
- Review the website's terms of service and applicable access restrictions.
- Confirm that the client's authorisation covers the specific pages, data and intended use.
- Check whether the website provides an official API or another approved data-access method.
- Do not assume that publicly accessible information is automatically free to collect or reuse.

### 9.2 Robots.txt and Website Policies

Review the website's `robots.txt` file to understand its published crawling preferences.

Respect applicable crawling restrictions and obtain clarification where necessary.

A robots.txt file is not, by itself, legal permission to scrape a website or a substitute for reviewing its terms and obtaining authorisation.

### 9.3 Respectful Scraping

- Make requests at reasonable intervals.
- Avoid excessive traffic that could affect website performance.
- Use appropriate request timeouts.
- Identify the scraper appropriately where required.
- Stop scraping if access is withdrawn or the website owner requests that collection cease.
- Do not bypass CAPTCHAs, authentication controls, rate limits or other access restrictions.

### 9.4 Data Protection in Kenya

The **Data Protection Act, 2019** is particularly relevant where the scraper collects personal information.

Before collecting information, consider:

- Whether the information qualifies as personal data.
- Whether there is a lawful basis for processing it.
- Whether the collection purpose is specific and legitimate.
- Whether the collected information is necessary and proportionate.
- How long the information will be retained.
- How the information will be secured and who can access it.
- Whether information is transferred outside Kenya and what safeguards are required.

Avoid collecting unnecessary personal information such as individual recruiters' personal contact details.

The organisation should also establish whether registration obligations, data protection impact assessments or additional safeguards apply to the proposed processing activity.

Relevant legislation and guidance:

- [Kenya Data Protection Act, 2019 – Office of the Data Protection Commissioner](https://odpc.go.ke/wp-content/uploads/2024/02/TheDataProtectionAct__No24of2019.pdf)
- [Office of the Data Protection Commissioner – Data Protection Laws](https://www.odpc.go.ke/data-protection-laws-kenya/)

### 9.5 Cybersecurity and Unauthorised Access

The Computer Misuse and Cybercrimes Act, 2018 addresses unauthorised access to computer systems and unauthorised interference.

The scraper must only access systems and information within the scope of the client's permission.

Do not attempt to access restricted databases, private accounts or protected endpoints without appropriate authorisation.

Reference:

[Computer Misuse and Cybercrimes Act, 2018 – Kenya Law](https://new.kenyalaw.org/akn/ke/act/2018/5/eng%402018-05-18/source)

### 9.6 Copyright and Commercial Use

Review copyright restrictions and contractual conditions before reproducing, storing or distributing website content.

Collecting factual information for analysis does not automatically grant permission to reproduce entire job advertisements or redistribute protected content.

Where possible, retain factual fields and links to the original advertisements rather than republishing full descriptions.

### 9.7 Professional Responsibility

The client should understand:

- What information is being collected.
- Why the information is being collected.
- How the information will be used.
- Where the information will be stored.
- Who will have access to the results.

Legal and compliance requirements should be reviewed with the client's legal or data protection team before deployment.

## 10. Limitations

The current implementation is a learning prototype.

Its limitations include:

- It only supports the HTML structure of Quotes to Scrape.
- It does not extract actual job advertisements.
- It does not use a database.
- It does not maintain historical records.
- It does not perform automated skill or salary analysis.
- It does not include a dashboard.
- It does not implement production-level retry handling or scheduled execution.

## 11. Future Improvements

Potential improvements include:

1. Adapt the scraper to an authorised live jobs board.
2. Introduce Pandas for data cleaning and analysis.
3. Use SQLite or PostgreSQL to maintain historical records.
4. Implement duplicate detection and job update tracking.
5. Introduce scheduled scraping.
6. Develop a dashboard for HR managers.
7. Analyse frequently requested skills and advertised salary ranges.

## 12. Conclusion

This project demonstrates how Python can automate website data collection through HTTP requests, HTML parsing and pagination.

Although the practice implementation extracts quotes, its underlying techniques provide a foundation for developing an authorised recruitment intelligence tool.

Such a tool could help HR managers reduce manual research, monitor competitor recruitment activity and make more informed decisions about skills demand and compensation trends.

**Important:** The live jobs-board implementation would require a separate review of the website's access permissions, contractual requirements, applicable laws and data protection obligations before deployment.
