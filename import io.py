import requests
import time
from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = Flask(__name__)

# --- CONFIG ---
TOKEN = "token you get from import requests file"
KINDLE_WIDTH = 1072
KINDLE_HEIGHT = 1448
API_URL = "http://localhost:9863/api/v1/state"

# --- GLOBAL CACHE ---
# This prevents the 429 by remembering the song for 2 seconds
cache = {
    "data": None,
    "last_fetch": 0
}

def get_ytm_data():
    global cache
    current_time = time.time()
    
    # If we fetched less than 2 seconds ago, return the cached data
    if cache["data"] and (current_time - cache["last_fetch"] < 2):
        return cache["data"]

    try:
        headers = {"Authorization": TOKEN}
        response = requests.get(API_URL, headers=headers, timeout=2)
        
        if response.status_code == 429:
            print("RATE LIMITED! Slowing down...")
            return cache["data"] # Return old data instead of crashing

        if response.status_code == 200:
            cache["data"] = response.json()
            cache["last_fetch"] = current_time
            return cache["data"]
            
        return None
    except:
        return cache["data"]

@app.route('/now_playing.png')
def now_playing():
    data = get_ytm_data()
    img = Image.new('L', (KINDLE_WIDTH, KINDLE_HEIGHT), 255)
    draw = ImageDraw.Draw(img)

    try:
        jp_font = "C:\\Windows\\Fonts\\msgothic.ttc" 
        font_title = ImageFont.truetype(jp_font, 75)
        font_artist = ImageFont.truetype(jp_font, 45)
        font_icons = ImageFont.truetype("arial.ttf", 90)
    except:
        font_title = font_artist = font_icons = ImageFont.load_default()

    video = data.get('video') if data else None

    if video and video.get('title'):
        # ... (Metadata and Image code remains same)
        title = video.get('title', 'Unknown')
        author = video.get('author', 'Unknown')
        
        thumbnails = video.get('thumbnails', [])
        cover_img = None
        if thumbnails:
            cover_url = thumbnails[-1].get('url')
            try:
                res = requests.get(cover_url, timeout=3)
                cover_img = Image.open(BytesIO(res.content)).convert('L')
            except: pass

        if cover_img:
            cover_img = cover_img.resize((900, 900), Image.Resampling.LANCZOS)
            img.paste(cover_img, (86, 80))

        draw.text((KINDLE_WIDTH//2, 1060), title[:30], font=font_title, fill=0, anchor="mm")
        draw.text((KINDLE_WIDTH//2, 1150), author[:40], font=font_artist, fill=100, anchor="mm")
        
        # Visual Controls
        controls_y = 1310
        draw.text((KINDLE_WIDTH//2 - 250, controls_y), "⏮", font=font_icons, fill=0, anchor="mm")
        draw.text((KINDLE_WIDTH//2, controls_y), "⏸", font=font_icons, fill=0, anchor="mm")
        draw.text((KINDLE_WIDTH//2 + 250, controls_y), "⏭", font=font_icons, fill=0, anchor="mm")
    else:
        msg = "Waiting for Music..." if data else "429: Slowing Down..."
        draw.text((KINDLE_WIDTH//2, 724), msg, font=font_title, fill=0, anchor="mm")

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/status_hash')
def status_hash():
    data = get_ytm_data()
    if data and data.get('video'):
        v = data['video']
        return str(hash(v.get('title', '') + v.get('author', '')))
    return "idle"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)