import os
from shutil import move
from os.path import splitext, exists, join
import logging
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Formats to check each file 
audioFormats = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".alac", ".aiff", ".wma", ".opus", ".m4a"]
videoFormats = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp", ".ogv"]
zipFormats = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"]
docFormats = [".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".html", ".xml", ".json"]
imageFormats = [".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".heif", ".raw"]
programFormats = [".exe", ".app", ".bin", ".bat", ".apk", ".dmg", ".pkg", ".jar", ".js", ".py"]

# Destinations and Source directories
source_dir = "/Users/kishg/Downloads"
dest_audios = "/Users/kishg/Downloads/Music"
dest_videos = "/Users/kishg/Downloads/Video"
dest_zips = "/Users/kishg/Downloads/Compressed"
dest_documents = "/Users/kishg/Downloads/Documents"
dest_images = "/Users/kishg/Downloads/Images"
dest_programs = "/Users/kishg/Downloads/Programs"

class MoveHandler(FileSystemEventHandler):
    def check_audios(self, entry, name):
        for extension in audioFormats:
            if name.endswith(extension) or name.endswith(extension.upper()):
                dest = dest_audios
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_videos(self, entry, name):
        for extension in videoFormats:
            if name.endswith(extension) or name.endswith(extension.upper()):
                dest = dest_videos
                move_file(dest, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_zips(self, entry, name):
        for extension in zipFormats:
            if name.endswith(extension) or name.endswith(extension.upper()):
                dest = dest_zips
                move_file(dest, entry, name)
                logging.info(f"Moved zip file: {name}")

    def check_documents(self, entry, name):
        for extension in docFormats:
            if name.endswith(extension) or name.endswith(extension.upper()):
                dest = dest_documents
                move_file(dest, entry, name)
                logging.info(f"Moved document: {name}")

    def check_images(self, entry, name):
        for extension in imageFormats:
            if name.endswith(extension) or name.endswith(extension.upper()):
                dest = dest_images
                move_file(dest, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_programs(self, entry, name):
        for extension in programFormats:
            if name.endswith(extension) or name.endswith(extension.upper()):
                dest = dest_programs
                move_file(dest, entry, name)
                logging.info(f"Moved program file: {name}")

    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audios(entry, name)
                self.check_videos(entry, name)
                self.check_zips(entry, name)
                self.check_documents(entry, name)
                self.check_images(entry, name)
                self.check_programs(entry, name)


# Checking whether file already exists, if exists then rename it by adding a number to it
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        os.rename(oldName, newName)
    move(entry, dest)

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
