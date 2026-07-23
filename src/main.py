import database.database as db
import sqlite3
import sqlalchemy
from capture.capture import Capture
from ocr.ocr import OCR
import torch
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='torch')

def main():
    
    print("cuda available:", torch.cuda.is_available())
    
    conn, cursor = db.create_connection(db.DB_PATH)
    if not conn or not cursor:
        print("Error! cannot create the database connection.")
        return

    db.init_db_tables(conn, cursor)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
        
    capture = Capture()
    screenshot = capture.capture_overwatch_screenshot()
    if screenshot:
        rows = capture.split_into_rows(screenshot)
        sections = capture.split_rows_into_sections(rows)
        print(f"Captured {len(rows)} rows and {len(sections)} sections.")
        
    ocr = OCR()
    extracted_texts = ocr.extract_text_from_sections(sections)

    # convert to pandas df
    # each row is a player, each column is a stat
    data = {}
    for key, text in extracted_texts.items():
        player_index = int(key.split("_")[2]) - 1 # player_row_1_stat -> 0
        stat_name = "_".join(key.split("_")[3:]) # player_row_1_stat -> stat
        if "hero" in key.lower():
            # TODO get hero name from image somehow
            data[player_index] = {"hero": "placeholder_hero_name"}
            continue
        if player_index not in data:
            data[player_index] = {}
        data[player_index][stat_name] = text
        
    df = pd.DataFrame.from_dict(data, orient='index')
    # df.astype({
    #     # 'name': 'str',
    #     'kills': 'int',
    #     'deaths': 'int',
    #     'assists': 'int',
    #     'damage_dealt': 'int',
    #     'healing_done': 'int',
    #     'damage_blocked': 'int'
    # }, errors='coerce')
    numeric_cols = ['kills', 'deaths', 'assists', 'damage_dealt', 'healing_done', 'damage_blocked']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True)  # Fill NaN values with 0
    df = df.astype({col: 'int' for col in numeric_cols})
    print(df.head(n=6))
    df.to_csv("data/extracted_stats.csv", index=False)
        
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()