import pyautogui
from PIL import Image, ImageChops
import pygetwindow as gw
import time
import os
from models.gamemode import GameMode

# bottom of first row of text = 365
CAREER_PROFILE_6V6_SCOREBOARD_LEFT = 800
CAREER_PROFILE_6V6_SCOREBOARD_TOP = 315
CAREER_PROFILE_6V6_SCOREBOARD_RIGHT = 1800
CAREER_PROFILE_6V6_SCOREBOARD_ROW_HEIGHT = 80

ROW_SECTIONS = {    # left, top, right, bottom
    "hero": (0, 0, 80, 80),
    "name": (80, 0, 400, 65),
    "kills": (400, 0, 500, 80),
    "assists": (500, 0, 550, 80),
    "deaths": (550, 0, 600, 80),
    "damage_dealt": (650, 0, 750, 80),
    "healing_done": (775, 0, 850, 80),
    "damage_blocked": (900, 0, 975, 80),
}
    
class Capture:
    '''
    A class to capture screenshots of the Overwatch game.
    '''
    
    def __init__(self, window_title="Overwatch", output_dir="screenshots", gamemode=GameMode.MODE_6V6):
        self.window_title = window_title
        self.output_dir = output_dir
        self.gamemode = gamemode
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def capture_overwatch_screenshot(self) -> Image.Image | None:
        # Get the Overwatch window
        window = gw.getWindowsWithTitle(self.window_title)
        if not window:
            print(f"No window found with title: {self.window_title}")
            return
        window = window[0]
        window.activate()
        time.sleep(1)  # Wait for the window to come to the front

        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))

        rows: list[Image.Image] = []

        return screenshot
    
    def split_into_rows(self, screenshot: Image.Image) -> list[Image.Image]:
        rows: list[Image.Image] = []
        
        if self.gamemode == GameMode.MODE_6V6:
            for i in range(self.gamemode.value):
                top = CAREER_PROFILE_6V6_SCOREBOARD_TOP + i * CAREER_PROFILE_6V6_SCOREBOARD_ROW_HEIGHT
                bottom = top + CAREER_PROFILE_6V6_SCOREBOARD_ROW_HEIGHT
                player_row = screenshot.copy().crop((
                    CAREER_PROFILE_6V6_SCOREBOARD_LEFT, 
                    top, 
                    CAREER_PROFILE_6V6_SCOREBOARD_RIGHT, 
                    bottom))
                
                rows.append(player_row)
                
                # save row for debugging
                # row_path = os.path.join(self.output_dir, f"player_row_{i+1}.png")
                # player_row.save(row_path)
                
        elif self.gamemode == GameMode.MODE_5V5:
            pass
        
        screenshot.close()
        
        return rows
    
    def split_rows_into_sections(self, rows: list[Image.Image]) -> dict[str, Image.Image]:
        sections = {}
        for i, row in enumerate(rows):
            for section_name, (left, top, right, bottom) in ROW_SECTIONS.items():
                section = row.crop((left, top, right, bottom))
                # section_path = os.path.join(self.output_dir, f"player_row_{i+1}_{section_name}.png")
                # section.save(section_path)
                sections[f"player_row_{i+1}_{section_name}"] = section
        return sections

    def split_screenshot(self, screenshot_path):
        rows = self.split_into_rows(screenshot_path)
        return self.split_rows_into_sections(rows)