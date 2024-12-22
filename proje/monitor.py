import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# İzlenecek dizin ve log dosyasının yolu
WATCH_DIRECTORY = "/home/ubuntu/bsm/test"
LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"

# Olayların loglanması için bir event handler
class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        change = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event.event_type,
            "file_path": event.src_path,
            "is_directory": event.is_directory
        }
        # Taşıma işlemi için ekstra bilgi
        if event.event_type == "moved":
            change["destination_path"] = event.dest_path

        # JSON'a kaydet
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                json.dump([], f)

        with open(LOG_FILE, "r+") as f:
            try:
                changes = json.load(f)
            except json.JSONDecodeError:
                changes = []
            changes.append(change)
            f.seek(0)
            json.dump(changes, f, indent=4)

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIRECTORY):
        os.makedirs(WATCH_DIRECTORY)

    # Observer ve event handler ayarları
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=True)
    observer.start()

    try:
        print(f"Monitoring changes in {WATCH_DIRECTORY}...")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
