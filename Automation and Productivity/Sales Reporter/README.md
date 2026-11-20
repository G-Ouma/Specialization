# Daily Sales Reporter

A Python-based retail sales reporting tool that reads daily sales data from a CSV file, calculates key business metrics, checks inventory levels, and emails a formatted HTML sales summary using Gmail SMTP.

## 1. Project Overview

Small retail businesses often record sales in spreadsheets or CSV files. Manually calculating daily revenue, tracking transactions, identifying best-selling products, and monitoring stock levels can be time-consuming.

This project automates that reporting process by generating and emailing a daily sales summary.

## 2. Features

- **Total Revenue:** Calculates daily revenue using quantity sold multiplied by item price.
- **Transaction Count:** Counts unique sales transactions.
- **Top-Selling Item:** Identifies the item with the highest total quantity sold.
- **Low-Stock Alerts:** Identifies products whose available stock is at or below their restock level.
- **HTML Email Reports:** Generates a formatted email containing sales metrics and inventory alerts.
- **Gmail SMTP Integration:** Sends reports using Gmail authentication and an App Password.

## 3. Project Structure

```text
Sales Reporter/
│
├── sales.csv
├── main.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 4. Technologies Used

- Python
- Pandas – CSV processing and data analysis
- python-dotenv – Environment variable management
- smtplib – Gmail SMTP email delivery
- email.message – HTML email construction

## 5. Installation

This project uses the shared virtual environment in the root of the Specialization repository.

Navigate to the repository root:

```powershell
cd "C:\Projects\Python\100 Days\Specialization"
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Navigate to the project directory:

```powershell
cd "Automation and Productivity\Sales Reporter"
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## 6. Sales CSV Format

The script reads sales records from `sales.csv`.

The CSV contains the following columns:

| Column | Description |
|---|---|
| transaction_id | Unique transaction identifier |
| item_name | Product name |
| quantity_sold | Quantity sold |
| price | Selling price per unit |
| stock_on_hand | Current available stock |
| restock_level | Minimum desired stock level |

Example:

```csv
transaction_id,item_name,quantity_sold,price,stock_on_hand,restock_level
T001,Unga,3,180,12,10
T002,Milk,2,70,8,10
T003,Bread,4,65,15,8
```

Multiple rows can contain the same transaction ID or product name.

The script aggregates product quantities when identifying the top-selling item and counts unique transaction IDs when calculating the number of transactions.

For inventory checks, the script uses the latest stock value recorded for each product in the CSV.

## 7. Gmail Configuration

The project uses Gmail SMTP with an App Password.

SMTP configuration:

- SMTP Server: `smtp.gmail.com`
- Port: `587`
- Encryption: STARTTLS

### Generate a Gmail App Password

1. Enable 2-Step Verification on your Google account.
2. Visit [Google App Passwords](https://myaccount.google.com/apppasswords).
3. Generate an App Password for this project.

### Configure environment variables

Create a `.env` file in the project directory:

```env
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com
```

The `.env` file must never be committed to GitHub.

Use `.env.example` to document the required variables without exposing credentials.

## 8. Running the Script

Ensure the cashier has updated `sales.csv`.

Run:

```powershell
python main.py
```

The script will:

1. Load Gmail credentials from `.env`.
2. Read the sales CSV.
3. Calculate total revenue and transaction count.
4. Identify the top-selling product.
5. Check for low-stock products.
6. Generate a formatted HTML email.
7. Send the report to the configured recipient.

A successful execution displays:

```text
Sales report successfully emailed!
Recipient: recipient@gmail.com
```

## 9. Sample Results

Using the sample sales dataset:

| Metric | Result |
|---|---:|
| Total Revenue | KES 5,045.00 |
| Transactions | 12 |
| Top-Selling Item | Unga |
| Quantity Sold | 12 |

Low-stock alerts:

| Item | Current Stock | Restock Level |
|---|---:|---:|
| Cooking Oil | 4 | 8 |
| Milk | 8 | 10 |
| Sugar | 6 | 10 |

The HTML email presents these metrics in a structured report with a dedicated inventory alert section.

## 10. Future Enhancement: Daily Scheduling

The current implementation requires the script to be executed manually.

A planned enhancement is to use **Windows Task Scheduler** to execute the script automatically every day at 6:00 PM.

The scheduled task will:

1. Trigger daily at 6:00 PM.
2. Execute the Python script using the existing virtual environment.
3. Read the latest sales CSV.
4. Generate and email the daily report.

This will allow the shop owner to receive daily sales summaries without manually running the script.

## 11. Email Deliverability Considerations

The project currently uses Gmail SMTP with an App Password, which is suitable for learning and small-scale testing.

However, automated emails may occasionally be delivered to recipients' spam folders, particularly when using a newly configured sender.

For more reliable production email delivery, consider:

- Using a dedicated transactional email service.
- Configuring a custom sending domain.
- Setting up SPF (Sender Policy Framework).
- Enabling DKIM (DomainKeys Identified Mail).
- Publishing a DMARC (Domain-based Message Authentication, Reporting and Conformance) policy.

These measures improve sender authentication and help establish trust with receiving email providers.

Email delivery to the inbox cannot be guaranteed, even with these configurations.

## 12. Security Considerations

- Never hardcode email credentials in Python files.
- Store Gmail App Passwords in `.env`.
- Keep `.env` excluded from Git tracking.
- Commit `.env.example` with placeholder values only.
- Never publish real credentials or App Passwords on GitHub.

## 13. Future Improvements

- Automatic daily execution.
- Weekly and monthly sales reports.
- Sales trend analysis.
- Historical sales storage.
- Graphical sales dashboards.
- Multiple recipient support.
- Improved error handling and delivery logging.

---

**Project:** Daily Sales Reporter  
**Category:** Automation and Productivity  
**Language:** Python  
**Status:** Core functionality implemented; daily scheduling planned.