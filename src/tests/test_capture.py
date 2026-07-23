import os
import pytest
from capture.capture import Capture
import subprocess

TMP_SCREENSHOTS_DIR = "C:\\Users\\alden\\Documents\\OWStats\\src\\tests\\test_screenshots"
CMD_CLEAR_TMP_SCREENSHOTS_DIR = f'Remove-Item -Path "{TMP_SCREENSHOTS_DIR}\\*" -Recurse -Force'

def clear_tmp_screenshots():
    # Clear the temporary screenshots directory before each test
    subprocess.run(["powershell", "-Command", CMD_CLEAR_TMP_SCREENSHOTS_DIR], check=True)

def test_capture_overwatch_screenshot():
    print(os.getcwd())
    capture = Capture(window_title="Overwatch", output_dir=TMP_SCREENSHOTS_DIR)
    capture.capture_overwatch_screenshot()
    # Check if the screenshot file exists
    assert len(os.listdir(TMP_SCREENSHOTS_DIR)) > 0

def test_split_screenshot():
    capture = Capture(window_title="Overwatch", output_dir=TMP_SCREENSHOTS_DIR)
    screenshot = capture.capture_overwatch_screenshot()
    capture.split_screenshot(screenshot)
    # Check if the player row files exist
    assert len(os.listdir(TMP_SCREENSHOTS_DIR)) > 0