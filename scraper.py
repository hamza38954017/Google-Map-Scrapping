import time
import csv
import re
import os
import requests
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

# ---------- CONFIGURATION ----------
LOCATIONS = [
    # --- USA (Extra included) ---
    "New York City, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", 
    "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", 
    "Dallas, TX", "San Jose, CA", "Austin, TX", "Jacksonville, FL", 
    "Fort Worth, TX", "Columbus, OH", "San Francisco, CA", "Seattle, WA", 
    "Denver, CO", "Washington, DC", "Boston, MA", "Miami, FL",

    # --- Canada ---
    "Toronto, ON", "Montreal, QC", "Vancouver, BC", "Calgary, AB", 
    "Edmonton, AB", "Ottawa, ON", "Winnipeg, MB", "Quebec City, QC", 
    "Hamilton, ON", "Halifax, NS",

    # --- Australia ---
    "Sydney, Australia", "Melbourne, Australia", "Brisbane, Australia", 
    "Perth, Australia", "Adelaide, Australia", "Gold Coast, Australia", 
    "Newcastle, Australia", "Canberra, Australia", "Sunshine Coast, Australia", 
    "Hobart, Australia",

    # --- New Zealand ---
    "Auckland, New Zealand", "Wellington, New Zealand", "Christchurch, New Zealand", 
    "Hamilton, New Zealand", "Tauranga, New Zealand", "Napier-Hastings, New Zealand", 
    "Dunedin, New Zealand", "Palmerston North, New Zealand", "Nelson, New Zealand", 
    "Rotorua, New Zealand",

    # --- UK (Extra included) ---
    "London, UK", "Birmingham, UK", "Manchester, UK", "Glasgow, UK", 
    "Edinburgh, UK", "Liverpool, UK", "Leeds, UK", "Bristol, UK", 
    "Sheffield, UK", "Newcastle upon Tyne, UK", "Cardiff, UK", "Belfast, UK",

    # --- Germany (Extra included) ---
    "Berlin, Germany", "Munich, Germany", "Frankfurt, Germany", 
    "Hamburg, Germany", "Cologne, Germany", "Stuttgart, Germany", 
    "Düsseldorf, Germany", "Leipzig, Germany", "Dortmund, Germany", 
    "Essen, Germany", "Bremen, Germany", "Dresden, Germany",

    # --- France (Extra included) ---
    "Paris, France", "Marseille, France", "Lyon, France", "Toulouse, France", 
    "Nice, France", "Nantes, France", "Montpellier, France", "Strasbourg, France", 
    "Bordeaux, France", "Lille, France", "Rennes, France",

    # --- Italy (Extra included) ---
    "Rome, Italy", "Milan, Italy", "Naples, Italy", "Turin, Italy", 
    "Palermo, Italy", "Genoa, Italy", "Bologna, Italy", "Florence, Italy", 
    "Bari, Italy", "Catania, Italy", "Venice, Italy",

    # --- Spain ---
    "Madrid, Spain", "Barcelona, Spain", "Valencia, Spain", "Seville, Spain", 
    "Zaragoza, Spain", "Málaga, Spain", "Murcia, Spain", "Palma, Spain", 
    "Las Palmas, Spain", "Bilbao, Spain",

    # --- Switzerland ---
    "Zurich, Switzerland", "Geneva, Switzerland", "Basel, Switzerland", 
    "Lausanne, Switzerland", "Bern, Switzerland", "Winterthur, Switzerland", 
    "Lucerne, Switzerland", "St. Gallen, Switzerland", "Lugano, Switzerland", 
    "Biel/Bienne, Switzerland",

    # --- Austria ---
    "Vienna, Austria", "Graz, Austria", "Linz, Austria", "Salzburg, Austria", 
    "Innsbruck, Austria", "Klagenfurt, Austria", "Villach, Austria", 
    "Wels, Austria", "Sankt Pölten, Austria", "Dornbirn, Austria",

    # --- Belgium ---
    "Brussels, Belgium", "Antwerp, Belgium", "Ghent, Belgium", 
    "Charleroi, Belgium", "Liège, Belgium", "Bruges, Belgium", 
    "Namur, Belgium", "Leuven, Belgium", "Mons, Belgium", "Aalst, Belgium",

    # --- Netherlands ---
    "Amsterdam, Netherlands", "Rotterdam, Netherlands", "The Hague, Netherlands", 
    "Utrecht, Netherlands", "Eindhoven, Netherlands", "Groningen, Netherlands", 
    "Tilburg, Netherlands", "Almere, Netherlands", "Breda, Netherlands", 
    "Nijmegen, Netherlands",

    # --- Sweden ---
    "Stockholm, Sweden", "Gothenburg, Sweden", "Malmö, Sweden", 
    "Uppsala, Sweden", "Västerås, Sweden", "Örebro, Sweden", 
    "Linköping, Sweden", "Helsingborg, Sweden", "Jönköping, Sweden", 
    "Norrköping, Sweden",

    # --- Norway ---
    "Oslo, Norway", "Bergen, Norway", "Trondheim, Norway", "Stavanger, Norway", 
    "Bærum, Norway", "Kristiansand, Norway", "Fredrikstad, Norway", 
    "Sandnes, Norway", "Tromsø, Norway", "Drammen, Norway",

    # --- Denmark ---
    "Copenhagen, Denmark", "Aarhus, Denmark", "Odense, Denmark", 
    "Aalborg, Denmark", "Esbjerg, Denmark", "Randers, Denmark", 
    "Kolding, Denmark", "Horsens, Denmark", "Vejle, Denmark", "Roskilde, Denmark",

    # --- Finland ---
    "Helsinki, Finland", "Espoo, Finland", "Tampere, Finland", "Vantaa, Finland", 
    "Oulu, Finland", "Turku, Finland", "Jyväskylä, Finland", "Lahti, Finland", 
    "Kuopio, Finland", "Pori, Finland",

    # --- Ireland ---
    "Dublin, Ireland", "Cork, Ireland", "Limerick, Ireland", "Galway, Ireland", 
    "Waterford, Ireland", "Drogheda, Ireland", "Dundalk, Ireland", 
    "Bray, Ireland", "Navan, Ireland", "Kilkenny, Ireland",

    # --- Japan (Extra included) ---
    "Tokyo, Japan", "Yokohama, Japan", "Osaka, Japan", "Nagoya, Japan", 
    "Sapporo, Japan", "Fukuoka, Japan", "Kobe, Japan", "Kyoto, Japan", 
    "Kawasaki, Japan", "Saitama, Japan", "Hiroshima, Japan", "Sendai, Japan",

    # --- Other Major European Cities (Not explicitly named above) ---
    "Prague, Czechia", "Warsaw, Poland", "Budapest, Hungary", 
    "Lisbon, Portugal", "Athens, Greece", "Bucharest, Romania",

    # --- Smaller Nations / City-States ---
    "Singapore, Singapore", "Jurong East, Singapore", "Woodlands, Singapore", # Singapore
    "Luxembourg City, Luxembourg", "Esch-sur-Alzette, Luxembourg", "Differdange, Luxembourg", # Luxembourg
    "Reykjavik, Iceland", "Kópavogur, Iceland", "Hafnarfjörður, Iceland", "Akureyri, Iceland" # Iceland
]
BUSINESS_TYPE = "Doctor"
OUTPUT_FILE = "businesses.csv"
OUTPUT_NO_WEBSITE = "businesses_no_website.csv"
MAX_RESULTS_PER_LOCATION = 1000
DELAY_BETWEEN_LOCATIONS = 5

# Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "8349995675:AAE9grCMm22vWOzmAjlDtpRd4iMR8IQiVgA"
TELEGRAM_CHAT_ID = "7369364451"
# -----------------------------------

def setup_driver():
    """Set up headless Chrome driver with desktop user‑agent."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=options)

def accept_cookies(driver):
    """Click the 'Accept all' cookie button if it appears."""
    try:
        accept_btn = driver.find_element(By.XPATH, "//button[contains(., 'Accept all')]")
        accept_btn.click()
        print("🍪 Accepted cookies")
        time.sleep(2)
    except:
        pass

def safe_find_text(parent, selector, default=""):
    """Safely find element and return its text."""
    try:
        return parent.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return default

def extract_card_data(card):
    """
    Extract name, address, rating, review count, price, image URL, and place link
    from a result card without clicking it.
    """
    name = safe_find_text(card, ".fontHeadlineSmall")
    if not name:
        name = safe_find_text(card, "h3")

    address = safe_find_text(card, "[class*='fontBodyMedium'] span")
    if not address:
        try:
            spans = card.find_elements(By.TAG_NAME, "span")
            for span in spans:
                text = span.text
                if re.search(r'\d+ [A-Za-z]', text) or 'Street' in text or 'Ave' in text:
                    address = text
                    break
        except:
            pass

    rating = safe_find_text(card, ".MW4etd")
    reviews = ""
    price = ""

    try:
        info_container = card.find_element(By.CSS_SELECTOR, ".e4rVHe")
        full_text = info_container.text
        match_reviews = re.search(r'\(([0-9,]+)\)', full_text)
        if match_reviews:
            reviews = match_reviews.group(1).replace(',', '')
        match_price = re.search(r'[₹$][0-9\-–]+', full_text)
        if match_price:
            price = match_price.group()
    except:
        reviews_text = safe_find_text(card, ".UY7F9")
        reviews = re.sub(r'[(),]', '', reviews_text)
        price = safe_find_text(card, ".e4rVHe span") or safe_find_text(card, "[class*='fontBodyMedium'] [aria-label*='price']")

    image_url = ""
    try:
        img = card.find_element(By.TAG_NAME, "img")
        image_url = img.get_attribute("src")
    except:
        pass
    if not image_url:
        try:
            style_div = card.find_element(By.CSS_SELECTOR, "div[style*='background-image']")
            style = style_div.get_attribute("style")
            match = re.search(r'url\("?(.*?)"?\)', style)
            if match:
                image_url = match.group(1)
        except:
            pass

    link = ""
    try:
        link_elem = card.find_element(By.CSS_SELECTOR, "a.hfpxzc")
        link = link_elem.get_attribute("href")
    except:
        pass

    return name, address, rating, reviews, price, image_url, link

def clean_phone(phone_text):
    """Remove non‑digit characters except leading + and dash, and trim."""
    if not phone_text:
        return ""
    cleaned = re.sub(r'[^\d\s\+\-]', '', phone_text)
    return cleaned.strip()

def extract_hours_from_panel(driver):
    """
    After clicking a card, extract working hours from the opened panel.
    """
    hours_parts = []
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".OqCZI table.eK4R0e"))
        )
        hours_table = driver.find_element(By.CSS_SELECTOR, ".OqCZI table.eK4R0e")
        rows = hours_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            day_cell = row.find_element(By.CSS_SELECTOR, "td.ylH6lf div")
            hours_cell = row.find_element(By.CSS_SELECTOR, "td.mxowUb ul li")
            day = day_cell.text.strip()
            hours = hours_cell.text.strip()
            if day and hours:
                hours_parts.append(f"{day}: {hours}")
    except (TimeoutException, NoSuchElementException):
        pass
    return "; ".join(hours_parts)

def extract_phone_website_hours(driver, card):
    """
    Click the card, wait for details panel, and extract phone, website, and hours.
    """
    phone = ""
    website = ""
    hours = ""

    try:
        card.click()
        time.sleep(1.5)

        phone_elem = driver.find_elements(By.CSS_SELECTOR, "button[data-item-id*='phone']")
        if phone_elem:
            phone = phone_elem[0].text.strip()
        else:
            tel_link = driver.find_elements(By.CSS_SELECTOR, "a[href^='tel:']")
            if tel_link:
                phone = tel_link[0].get_attribute('href').replace('tel:', '').strip()
        phone = clean_phone(phone)

        website_elem = driver.find_elements(By.CSS_SELECTOR, "a[data-item-id='authority']")
        if website_elem:
            website = website_elem[0].get_attribute('href')
        else:
            links = driver.find_elements(By.CSS_SELECTOR, "a[href^='http']")
            for link in links:
                href = link.get_attribute('href')
                if href and 'google.com' not in href and 'maps' not in href:
                    website = href
                    break

        hours = extract_hours_from_panel(driver)

    except StaleElementReferenceException:
        print("⚠️ Card became stale before click – skipping this entry")
    except Exception as e:
        print(f"⚠️ Error extracting details: {e}")

    return phone, website, hours

def scroll_to_load(driver, target_count, max_retries=3):
    """
    Scroll the feed until we have at least target_count cards.
    """
    feed = driver.find_element(By.CSS_SELECTOR, "[role='feed']")
    last_count = 0
    retries = 0

    while True:
        cards = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        current_count = len(cards)
        if current_count >= target_count:
            print(f"✅ Reached target: {current_count} cards")
            return current_count

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", feed)
        time.sleep(2.5)

        cards = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        new_count = len(cards)
        if new_count == last_count:
            retries += 1
            print(f"⏳ No new cards after scroll (retry {retries}/{max_retries})")
            if retries >= max_retries:
                print(f"⚠️ Stopping after {max_retries} failed scroll attempts.")
                return new_count
            time.sleep(3)
        else:
            retries = 0
            last_count = new_count
            print(f"📜 Loaded {new_count} cards so far...")

def scrape_location(driver, location):
    """
    Perform the full scraping routine for a single location.
    """
    print(f"\n📍 Scraping location: {location}")
    encoded_business = quote_plus(BUSINESS_TYPE)
    encoded_location = quote_plus(location)
    url = f"https://www.google.com/maps/search/{encoded_business}+in+{encoded_location}/?hl=en"
    driver.get(url)
    time.sleep(5)

    if "/place/" in driver.current_url:
        print(f"❌ Redirected to a place page for {location} – skipping.")
        return []

    accept_cookies(driver)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[role='feed']"))
        )
        print("✅ Found results feed")
    except TimeoutException:
        print(f"❌ Could not find results feed for {location}. Skipping.")
        return []

    scroll_to_load(driver, MAX_RESULTS_PER_LOCATION, max_retries=3)

    data_location = []
    processed = 0
    while processed < MAX_RESULTS_PER_LOCATION:
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        except:
            break
        if processed >= len(cards):
            print("⚠️ No more cards available.")
            break

        card = cards[processed]
        print(f"🔄 Processing card {processed+1}/{min(len(cards), MAX_RESULTS_PER_LOCATION)}")

        try:
            name, address, rating, reviews, price, image_url, link = extract_card_data(card)
            phone, website, hours = extract_phone_website_hours(driver, card)

            data_location.append([
                location, name, address, phone, rating, reviews, price,
                image_url, website, link, hours
            ])
            print(f"   ✅ {name} – {phone if phone else 'no phone'} – {rating}⭐ ({reviews}) – hours: {bool(hours)}")

            try:
                back_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Back']")
                back_button.click()
            except:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='feed']"))
            )
            time.sleep(1)

        except StaleElementReferenceException:
            print("⚠️ Stale element – retrying same index after refresh")
            continue
        except Exception as e:
            print(f"⚠️ Error on card {processed+1}: {e}")
            try:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[role='feed']"))
                )
            except:
                pass
        finally:
            processed += 1

    return data_location

def send_to_telegram(file_path):
    """Uploads the generated CSV file directly to the provided Telegram chat."""
    if not os.path.exists(file_path):
        print(f"⚠️ Could not find {file_path} to upload.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': TELEGRAM_CHAT_ID}
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print(f"🚀 Successfully sent {file_path} to Telegram!")
            else:
                print(f"❌ Failed to send to Telegram. Status code: {response.status_code}")
                print(response.text)
    except Exception as e:
        print(f"⚠️ Error uploading to Telegram: {e}")

def main():
    header = ["Location", "Name", "Address", "Phone", "Rating", "Reviews", "Price",
              "Image_URL", "Website", "Place_Link", "Hours"]

    try:
        with open(OUTPUT_FILE, 'x', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    except FileExistsError:
        pass

    driver = setup_driver()
    all_data = []

    try:
        for idx, location in enumerate(LOCATIONS, 1):
            print(f"\n=== Location {idx}/{len(LOCATIONS)}: {location} ===")
            location_data = scrape_location(driver, location)
            all_data.extend(location_data)

            if location_data:
                with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(location_data)
                print(f"✅ Appended {len(location_data)} rows for {location} to {OUTPUT_FILE}")

            no_website_data = [row for row in location_data if not row[8]]
            if no_website_data:
                with open(OUTPUT_NO_WEBSITE, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if f.tell() == 0:
                        writer.writerow(header)
                    writer.writerows(no_website_data)

            if idx < len(LOCATIONS):
                print(f"⏳ Waiting {DELAY_BETWEEN_LOCATIONS} seconds before next location...")
                time.sleep(DELAY_BETWEEN_LOCATIONS)

    finally:
        driver.quit()

    print(f"\n🎉 All done! Total businesses scraped: {len(all_data)}")
    print(f"📁 Combined data saved to '{OUTPUT_FILE}'")
    
    # Send files to Telegram right after scraping completes
    print("\n📤 Preparing to upload to Telegram...")
    send_to_telegram(OUTPUT_FILE)
    if os.path.exists(OUTPUT_NO_WEBSITE):
         send_to_telegram(OUTPUT_NO_WEBSITE)

if __name__ == "__main__":
    main()
