from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    with sync_playwright() as p:
        page_url = 'https://results.eci.gov.in/PcResultGenJune2024/index.htm'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        # Select the <tr> elements with class "tr"
        msti = page.locator('//tr[@class="tr"]')

        # Get the count of the matching elements
        count = msti.count()
        print(f'There are {count} msti.')

        msti_list = []
        for i in range(count):
            mst = msti.nth(i)
            mst_dict = {}
            mst_dict['party_name'] = mst.locator('td').nth(0).text_content().strip()
            mst_dict['win_result'] = mst.locator('td').nth(1).text_content().strip()
            mst_dict['second_column'] = mst.locator('td').nth(2).text_content().strip()
            mst_dict['third_column'] = mst.locator('td').nth(3).text_content().strip()

            msti_list.append(mst_dict)

        # Create a DataFrame and save to Excel and CSV
        df = pd.DataFrame(msti_list)
        df.to_excel('msti_list.xlsx', index=False)
        df.to_csv('msti_list.csv', index=False)

        browser.close()

if __name__ == '__main__':
    main()
