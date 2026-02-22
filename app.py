from flask import Flask, send_file
import threading
import scraper  # This imports your script
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Google Maps Scraper on Render</h1>
    <a href='/run' style='padding: 10px; background: blue; color: white; text-decoration: none; border-radius: 5px;'>1. Start Scraper</a>
    <br><br>
    <a href='/download' style='padding: 10px; background: green; color: white; text-decoration: none; border-radius: 5px;'>2. Download businesses.csv</a>
    """

@app.route('/run')
def run_scraper():
    # Runs your scraper in the background so the web page doesn't time out
    thread = threading.Thread(target=scraper.main)
    thread.start()
    return "<h3>Scraper started in background!</h3><p>Check the Render deployment logs to see its progress.</p><a href='/'>Go Back</a>"

@app.route('/download')
def download():
    # Checks if your script has created the CSV yet
    if os.path.exists('businesses.csv'):
        return send_file('businesses.csv', as_attachment=True)
    return "CSV not found yet. Ensure you started the scraper and let it finish."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
