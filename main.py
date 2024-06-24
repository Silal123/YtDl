from pytube import YouTube 
import pytube
from colorama import Fore, Back, Style, init
import colorama
from datetime import datetime
from contextlib import closing
import os
import random
import signal

class Logger():
    def get_time_formated() -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def info(msg: str):
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.LIGHTBLACK_EX}] {Fore.CYAN}INFO{Fore.LIGHTBLACK_EX}: {Fore.WHITE}{msg}")
        return
    
    def warning(msg: str):
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.LIGHTBLACK_EX}] {Fore.YELLOW}WARNING{Fore.LIGHTBLACK_EX}: {Fore.WHITE}{msg}")
        return
    
    def error(msg: str):
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.LIGHTBLACK_EX}] {Fore.RED}ERROR{Fore.LIGHTBLACK_EX}: {Fore.WHITE}{msg}")
        return
    
    def success(msg: str):
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.LIGHTBLACK_EX}] {Fore.GREEN}SUCCESS{Fore.LIGHTBLACK_EX}: {Fore.WHITE}{msg}")
        return
    
    def input(msg: str):
        return input(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.LIGHTBLACK_EX}] {Fore.MAGENTA}INPUT{Fore.LIGHTBLACK_EX}! {Fore.WHITE}{msg}\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.LIGHTBLACK_EX}] >> {Fore.RESET}")

def signal_handler(signal, frame):
    Logger.warning("You pressed Ctrl+C! Exiting gracefully...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print(f"{Fore.RED}██╗░░░██╗████████╗░░░░░░██╗░░░░░░█████╗░░█████╗░██████╗░\n╚██╗░██╔╝╚══██╔══╝░░░░░░██║░░░░░██╔══██╗██╔══██╗██╔══██╗\n░╚████╔╝░░░░██║░░░█████╗██║░░░░░██║░░██║███████║██║░░██║\n░░╚██╔╝░░░░░██║░░░╚════╝██║░░░░░██║░░██║██╔══██║██║░░██║\n░░░██║░░░░░░██║░░░░░░░░░███████╗╚█████╔╝██║░░██║██████╔╝\n░░░╚═╝░░░░░░╚═╝░░░░░░░░░╚══════╝░╚════╝░╚═╝░░╚═╝╚═════╝░{Fore.RESET}\n")

path = str(Logger.input("Download folder (ENTER for Default): "))
if path == "": path = str(os.path.join(os.getcwd(), 'downloads'))
if not os.path.isdir(path): os.makedirs(path)
Logger.info(str("Download folder is now " + path))

try:
    only_audio = str(Logger.input("Only Audio Download? (true/false) [true]"))
    if only_audio.lower() != "false": only_audio = True
    if only_audio.lower() == "false": only_audio = False
except:
    only_audio = True
Logger.info("Only Audio is now " + str(only_audio))

Logger.warning("Use CTRL+C to exit!")
while True:
    vid_url = str(Logger.input("Enter the video URL:"))
    Logger.info("Loading video " + vid_url)

    try:
        yt = YouTube(vid_url)
        video = yt.streams.filter(only_audio=only_audio).first()
    except pytube.exceptions.AgeRestrictedError as e:
        Logger.error(f"Age restriction error at video {yt.title}!")
        continue
    except Exception as e:
        Logger.error(f"There was a error: {e}")
        continue

    title = yt.title
    author = yt.author

    destination = str(path)
    file_exists = os.path.exists(destination + "/" + title + ".mp4")
    file_exists = False

    if file_exists:
        destination = destination + "/.tmp"

    out_file = video.download(output_path=destination)

    if file_exists:
        destination = "/".join(list(destination.split('/')[0:-1])) 
        os.rename(out_file, str(destination + "\\" + title + "-" + str(random.randint(10000000, 99999999)) + ".mp4"))

    Logger.success(f"Downloaded {title} to {out_file}")