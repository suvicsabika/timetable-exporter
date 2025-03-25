# -----------------------------
# timetable_exporter/fetch_html.py
# -----------------------------

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os
import sys

def fetch_dynamic_html(url: str, output_file: str = "generated_page.html"):
    try:
        from pathlib import Path
        
        base_dir = Path(__file__).resolve().parent
        output_path = base_dir / output_file

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            print(f"Playwright client reporting: Navigating to: {url}")
            page.goto(url, wait_until="load", timeout=60000)

            html = page.content()
            browser.close()

            if not html or len(html.strip()) < 100:
                raise ValueError("Received empty or incomplete HTML content.")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)

            print(f"Playwright client reporting: HTML saved at: {os.path.abspath(output_file)}")

    except PlaywrightTimeoutError:
        print(f"Playwright client reporting: Timeout: The page took too long to load: {url}", file=sys.stderr)
    except Exception as e:
        print(f"Playwright client reporting: Unexpected error while fetching HTML:\n{e}", file=sys.stderr)
