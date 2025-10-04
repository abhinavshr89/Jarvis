import webbrowser
import os
import pyautogui
import datetime
import urllib.parse

def open_youtube(query: str = ""):
    """Searches YouTube with the given query"""
    if query:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        webbrowser.open(search_url)
        return f"Searched YouTube for: {query}"
    else:
        webbrowser.open("https://www.youtube.com")
        return "Opened YouTube homepage."


def search_google(query: str = ""):
    """Searches Google with the given query"""
    import urllib.parse
    if query:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(search_url)
        return f"Searched Google for: {query}"
    else:
        return "No query provided."

def get_time(query: str = ""):
    """Tells the current system time"""
    return datetime.datetime.now().strftime("Current time is %H:%M:%S")

def mute_volume(query: str = ""):
    """Mutes the system volume"""
    pyautogui.press("volumemute")
    return "Muted system volume."



def open_notepad(query: str = ""):
    """Opens Notepad on the system"""
    os.system("notepad")
    return "Opened Notepad."



def take_screenshot(query: str = ""):
    """Takes a screenshot and saves it to the screenshots folder"""
    # Ensure screenshots folder exists
    os.makedirs("screenshots", exist_ok=True)
    
    # File name with timestamp
    filename = datetime.datetime.now().strftime("screenshots/screenshot_%Y%m%d_%H%M%S.png")
    
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    
    return f"Screenshot saved to {filename}"

def end_program(query: str = ""):
    """Ends the assistant program"""
    return "END_PROGRAM"
