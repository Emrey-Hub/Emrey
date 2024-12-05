import re
import sqlite3
from playwright.sync_api import sync_playwright

def clean_number(value):
    if value.strip() in ['', '\xa0']:
        return None
    cleaned = re.sub(r'[^\d,.\-]', '', value)
    cleaned = cleaned.replace('.', '').replace(',', '.')
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return cleaned

def scrape_and_store_cvm_data():
    with sqlite3.connect('financial_data.db', timeout=10.0) as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "BB Ativa Plus RF" (
            Month TEXT,
            Dia TEXT,
            Quota REAL,
            Captacao_no_Dia REAL,
            Resgate_no_Dia REAL,
            Patrimonio_Liquido REAL,
            Total_da_Carteira REAL,
            No_Total_de_Cotistas INTEGER,
            Data_da_Proxima TEXT,
            PRIMARY KEY (Month, Dia)
        )
        ''')

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            url = "https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/InfDiario/CPublicaInfDiario.aspx?PK_PARTIC=219063&COMPTC="
            page.goto(url)

            page.wait_for_selector("select[name='ddComptc']")

            months = page.evaluate('''() => {
                return Array.from(document.querySelector('select[name="ddComptc"]').options)
                    .map(option => option.value);
            }''')

            for month in months:
                page.select_option("select[name='ddComptc']", month)
                page.wait_for_selector("#dgDocDiario")
                page.wait_for_function("document.querySelectorAll('#dgDocDiario tr').length > 1")

                table_selector = "#dgDocDiario"
                previous_row_count = 0
                while True:
                    page.evaluate(f"document.querySelector('{table_selector}').scrollBy(0, 1000)")
                    page.wait_for_timeout(500)

                    current_row_count = len(page.query_selector_all(f"{table_selector} tr"))
                    if current_row_count == previous_row_count:
                        break
                    previous_row_count = current_row_count

                rows = page.query_selector_all(f"{table_selector} tr")[1:]
                for row in rows:
                    cols = row.query_selector_all("td")
                    if len(cols) == 8:
                        data = [month] + [clean_number(col.inner_text()) for col in cols]
                        cursor.execute('''
                        INSERT OR REPLACE INTO "BB Ativa Plus RF"
                        (Month, Dia, Quota, Captacao_no_Dia, Resgate_no_Dia,
                         Patrimonio_Liquido, Total_da_Carteira,
                         No_Total_de_Cotistas, Data_da_Proxima)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)

                print(f"Processed {len(rows)} rows for month {month}")
                conn.commit()

            browser.close()

# Run the scraping and storing function
scrape_and_store_cvm_data()
