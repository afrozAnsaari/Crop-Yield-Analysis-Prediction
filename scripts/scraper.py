import csv
import time
import urllib3

import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = "https://maharain.maharashtra.gov.in/test/maharain/"
SESSION_URL = BASE + "previous_year_rain.php"
DIVISION_URL = BASE + "Handlers/divisionHandler.php"
REPORT_URL = BASE + "rpt_past_rain_reports_season_rain_district_wise.php"

STATE_CODE = "11"
START_YEAR = 1998
END_YEAR = 2022
OUTPUT_FILE = f"maharain_district_rainfall_{START_YEAR}_{END_YEAR}.csv"
TIMEOUT = 30
REQUEST_PAUSE_SECONDS = 0.2

session = requests.Session()
session.verify = False

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://maharain.maharashtra.gov.in",
    "Referer": SESSION_URL,
}


def normalize_report_html(html):
    # The site returns malformed cells such as `<td>139.3<dth>` and
    # broken row boundaries like `</tr></tr><td>`.
    html = html.replace("<dth>", "</td>")
    html = html.replace("</tr></tr><td>", "</tr><tr><td>")
    return html


def create_session():
    print("Starting session...")
    response = session.get(SESSION_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
    response.raise_for_status()


def fetch_divisions():
    print("Fetching divisions...")
    response = session.post(
        DIVISION_URL,
        data=f"getDivision=1&stateCode={STATE_CODE}",
        headers=COMMON_HEADERS,
        timeout=TIMEOUT,
    )
    response.raise_for_status()

    payload = response.json()
    divisions = payload.get("data", [])
    if not divisions:
        raise ValueError("No divisions returned by divisionHandler.php")

    return [
        (division["division_code"], division["division_name"])
        for division in divisions
    ]


def build_headers(table):
    header_rows = table.select("thead tr")
    if len(header_rows) < 3:
        raise ValueError("Unexpected header structure in report table")

    month_cells = [cell.get_text(strip=True) for cell in header_rows[1].find_all("th")]
    metric_cells = [cell.get_text(strip=True) for cell in header_rows[2].find_all("th")]

    headers = ["location_name"]
    month_names = [cell for cell in month_cells if cell != "Circle / Taluka"]
    metric_index = 0

    for month in month_names:
        month_slug = month.lower()
        for _ in range(3):
            metric_name = metric_cells[metric_index]
            metric_index += 1
            metric_slug = (
                metric_name.lower()
                .replace("%", "percent")
                .replace(" ", "_")
            )
            headers.append(f"{month_slug}_{metric_slug}")

    return headers


def parse_rows(table, headers, division_id, division_name, year):
    records = []
    for row_index, row in enumerate(table.select("tbody tr"), start=1):
        values = [cell.get_text(" ", strip=True) for cell in row.find_all("td")]
        if len(values) != len(headers):
            continue

        row_data = dict(zip(headers, values))
        record = {
            "year": year,
            "division_code": division_id,
            "division_name": division_name,
            "row_order": row_index,
            **row_data,
        }
        records.append(record)

    return records


def fetch_report_rows(division_id, division_name, year):
    payload = f"stateCode={STATE_CODE}&divisionCode={division_id}&year={year}"
    response = session.post(
        REPORT_URL,
        data=payload,
        headers=COMMON_HEADERS,
        timeout=TIMEOUT,
    )
    response.raise_for_status()

    if "<table" not in response.text:
        return []

    cleaned_html = normalize_report_html(response.text)
    soup = BeautifulSoup(cleaned_html, "html.parser")
    table = soup.find("table", id="tableID") or soup.find("table")
    if table is None:
        return []

    headers = build_headers(table)
    return parse_rows(table, headers, division_id, division_name, year)


def write_csv(rows):
    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    create_session()
    divisions = fetch_divisions()
    print("Divisions found:", divisions)

    all_rows = []
    expected_requests = (END_YEAR - START_YEAR + 1) * len(divisions)
    completed_requests = 0

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"\nYear: {year}")
        for division_id, division_name in divisions:
            completed_requests += 1
            print(f"  [{completed_requests}/{expected_requests}] Fetching: {division_name}")
            rows = fetch_report_rows(division_id, division_name, str(year))
            print(f"    Rows parsed: {len(rows)}")
            all_rows.extend(rows)
            time.sleep(REQUEST_PAUSE_SECONDS)

    print("\nSample Data:\n")
    for row in all_rows[:5]:
        print(row)

    print(f"\nTotal records: {len(all_rows)}")
    write_csv(all_rows)
    if all_rows:
        print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
