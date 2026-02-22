from flask import Flask
import threading
import scraper
import os

app = Flask(__name__)

# This automatically fires your scraper in the background the exact second Render deploys
print("🚀 Auto-starting scraper in the background...")
threading.Thread(target=scraper.main, daemon=True).start()

@app.route('/')
def index():
    return """
    <h1 style='font-family: sans-serif;'>Scraper is Running! 🚀</h1>
    <p style='font-family: sans-serif;'>The scraping process started automatically in the background as soon as this server deployed.</p>
    <p style='font-family: sans-serif;'><strong>You can close this page.</strong> The CSV file will be sent directly to your Telegram when it finishes.</p>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
