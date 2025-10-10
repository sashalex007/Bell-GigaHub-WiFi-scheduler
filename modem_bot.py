import asyncio
import logging
import time
import schedule
from playwright.async_api import async_playwright

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def set_wifi_state(state: str, test):
    logging.info(f"--- Starting job to set Wi-Fi state to: {state} ---")
    
    try:
        with open("credentials.txt", "r") as f:
            lines = f.readlines()
            if len(lines) < 2:
                logging.error("'credentials.txt' must contain at least two lines (password and URL). Aborting job.")
                return
            modem_password = lines[0].strip()
            modem_url = lines[1].strip()
        if not modem_password or not modem_url:
            logging.error("Password or URL is missing from 'credentials.txt'. Aborting job.")
            return
    except FileNotFoundError:
        logging.error("'credentials.txt' not found. Please create it with the password on the first line and URL on the second. Aborting job.")
        return

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=(not test))
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(60000) 
        page.set_default_navigation_timeout(90000)

        try:
            logging.info("Attempting to navigate to modem admin page...")
            await page.goto(modem_url)

            logging.info("Clicking on 'Manage my Wi-Fi Primary' link...")
            await page.get_by_role("link", name="Manage my Wi-Fi Primary").click()

            logging.info("Entering password...")
            await page.get_by_role("textbox", name="Password:").fill(modem_password)

            logging.info("Clicking the 'Log in' button...")
            await page.get_by_role("button", name="Log in").click()
            
            logging.info("Login successful, navigating to advanced settings.")
            await page.get_by_role("button", name="Advanced settings").click()
            
            logging.info(f"Clicking buttons to set state to '{state}'...")        
            await page.get_by_text("ON", exact=True).nth(0).click()
            await page.get_by_text("ON", exact=True).nth(1).click()
            await page.get_by_text("ON", exact=True).nth(2).click()
            
            if not test:
                logging.info(f"Saving state...")
                await page.get_by_role("button", name="Save").click()
            else:
                await page.pause()
            
            await page.wait_for_timeout(2000) 
            screenshot_path = f"screenshot_success_{state}_{int(time.time())}.png"
            await page.screenshot(path=screenshot_path)
            logging.info(f"Successfully set Wi-Fi state to {state}. Screenshot saved to {screenshot_path}")
            return True
            
        except Exception as e:
            logging.error(f"An error occurred during the automation job: {e}")
            screenshot_path = f"screenshot_error_{state}_{int(time.time())}.png"
            await page.screenshot(path=screenshot_path)
            logging.warning(f"A screenshot of the error was saved to {screenshot_path}")
            return False
        finally:
            logging.info("Closing browser.")
            await context.close()
            await browser.close()
            logging.info(f"--- Job finished for state: {state} ---")

def run_job(state: str, test=False):
    #retry loop
    while True:
        success = asyncio.run(set_wifi_state(state, test))
        if success:
            logging.info(f"Job to set state to '{state}' completed successfully.")
            break # Exit the loop on success
        else:
            retry_delay = 60 # seconds
            logging.warning(f"Job failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

def main():
    # --- CONFIGURE YOUR SCHEDULE HERE ---
    #run_job(state="OFF", test=True) #UNCOMMENT TO TEST
    
    off_time = "23:00"
    on_time = "03:30"
    schedule.every().day.at(off_time).do(run_job, state="OFF")
    schedule.every().day.at(on_time).do(run_job, state="ON")
    logging.info("Scheduler started. Waiting for scheduled jobs.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
