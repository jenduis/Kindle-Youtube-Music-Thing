#!/bin/sh
# --- CONFIGURATION ---
SERVER_IP="192.168.1.30" # Swap with your Windows PC's exact local IP
PORT="5000"

LAST_HASH=""

# Clear screen initialization and format FBInk settings
fbink -q -c

while true; do
  # 1. Snatch the lightweight track identifier string
  CURRENT_HASH=$(wget -q -O - http://$SERVER_IP:$PORT/status_hash)
  
  # 2. Check if the hash has changed compared to last evaluation loop
  if [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
    LAST_HASH=$CURRENT_HASH
    
    # Pull down the compiled bitmap image to local temporary storage
    wget -q -O /tmp/music.png http://$SERVER_IP:$PORT/now_playing.png
    
    # Render layout image directly into frame buffer device node mapping
    # -g enforces immediate visual graphic pipeline updates
    fbink -q -g file=/tmp/music.png,w=0,h=0
  fi
  
  # Cycle timing interval (adjust lower if you want faster track feedback updates)
  sleep 3
done