import os
import time
import psutil
import vlc  # Make sure this is the VLC Python bindings

def is_vlc_running():
    """Check if VLC is currently running."""
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'vlc' or process.info['name'] == 'VLC':
            print("VLC is running.")
            return True
    print("VLC is not running.")
    return False

def start_vlc(playlist_path):
    """Start VLC with the specified playlist."""
    print("Starting VLC...")
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(playlist_path)
    player.set_media(media)
    player.play()
    return player

def main():
    playlist_path = 'playlist.m3u'
    print(f"Playlist path: {playlist_path}")

    player = None
    while True:
        if not is_vlc_running():
            if player:
                print("Stopping existing VLC player...")
                player.stop()
            player = start_vlc(playlist_path)
        else:
            print("VLC is already running. Waiting to recheck...")
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()