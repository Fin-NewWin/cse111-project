import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def check_tab_exist(cur: sqlite3.Cursor, table: str):
    sql = f"""
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'
    """
    cur.execute(sql)
    rows = cur.fetchall()
    return len(rows) != 0


def check_tab_update(cur: sqlite3.Cursor, table: str):
    sql = f"SELECT * FROM {table}"

    cur.execute(sql)
    rows = cur.fetchall()

    f = open(f"./data/{table}.db", "r")
    lines = f.readlines()

    return len(rows) == len(lines)


def test_table(cur: sqlite3.Cursor, table: str):
    sql = f"SELECT * FROM {table}"
    cur.execute(sql)
    rows = cur.fetchall()

    #for row in rows:
    #   print(row)


def create_table(cur: sqlite3.Cursor, table: str, table_attr: str):
    sql = f"DROP TABLE IF EXISTS {table}"
    cur.execute(sql)
    cur.execute(table_attr)


def import_data(cur: sqlite3.Cursor, table: str):
    cur.executescript(f"import ./data/{table}.db {table}")


def insert_data(cur, table: str):
    f = open(f"data/{table}.db", "r")
    lines = f.readlines()

    n = len(lines[0].strip().split("|"))
    s = (n * "?,")[:-1]

    for line in lines:
        line = line.strip().split("|")
        sql = f"INSERT INTO {table} VALUES({s})"
        cur.execute(sql, (list(line)))


def create_tab(conn: sqlite3.Connection):
    """
    Create tables in the database and store in file tpch.sqlite
    """
    cur = conn.cursor()
    sqls = {
        "state": """
        CREATE TABLE IF NOT EXISTS state (
            state_id INTEGER PRIMARY KEY,
            state_name TEXT
        )
        """,
        "player": """
        CREATE TABLE IF NOT EXISTS player (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT,
            player_position TEXT,
            player_height INTEGER,
            player_weight INTEGER,
            player_draft TEXT,
            player_team_id INTEGER
        )
        """,
        "player_stats": """
        CREATE TABLE IF NOT EXISTS player_stats (
            ps_player_id INTEGER,
            ps_season_id INTEGER,
            ps_team_id INTEGER,
            ps_g INTEGER,
            ps_gs INTEGER,
            ps_mp DECIMAL,
            ps_fg DECIMAL,
            ps_fga DECIMAL,
            ps_fgp DECIMAL,
            ps_3p DECIMAL,
            ps_3pa DECIMAL,
            ps_3pp DECIMAL,
            ps_2p DECIMAL,
            ps_2pa DECIMAL,
            ps_2pp DECIMAL,
            ps_efg DECIMAL,
            ps_ft DECIMAL,
            ps_fta DECIMAL,
            ps_ftp DECIMAL,
            ps_orb DECIMAL,
            ps_drb DECIMAL,
            ps_trb DECIMAL,
            ps_ast DECIMAL,
            ps_stl DECIMAL,
            ps_blk DECIMAL,
            ps_tov DECIMAL,
            ps_pf DECIMAL,
            ps_pts DECIMAL
        )
        """,
        "team": """
        CREATE TABLE IF NOT EXISTS team (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT,
            team_mascot TEXT,
            team_state_id INTEGER,
            team_conference TEXT,
            team_division TEXT,
            team_coach TEXT
        )
        """,
        "team_season": """
        CREATE TABLE IF NOT EXISTS team_season (
            ts_season_id INTEGER,
            ts_team_id INTEGER,
            ts_wins INTEGER,
            ts_losses INTEGER,
            ts_wl DECIMAL,
            ts_finish TEXT,
            ts_srs DECIMAL,
            ts_pace DECIMAL,
            ts_ortg DECIMAL,
            ts_drtg DECIMAL
        )
        """,
        "season": """
        CREATE TABLE IF NOT EXISTS season (
            season_id INTEGER,
            season_mvp INTEGER,
            season_team_id INTEGER,
            season_rookie INTEGER,
            season_point INTEGER,
            season_rbs INTEGER,
            season_ast INTEGER,
            season_wins INTEGER
        )
        """,
        "game": """
        CREATE TABLE IF NOT EXISTS game (
            game_id INTEGER,
            game_season_id INTEGER,
            game_away_team_id INTEGER,
            game_away_pts INTEGER,
            game_home_team_id INTEGER,
            game_home_pts INTEGER,
            game_type TEXT
        )
        """,
        "coach": """
        CREATE TABLE IF NOT EXISTS coach (
            coach_id INTEGER,
            coach_name TEXT
        )
        """,
    }

    for table in sqls:
        # check if table doesn't exist or update
        if not check_tab_exist(cur, table) or not check_tab_update(cur, table):
            create_table(cur, table, sqls[table])
            # import_data(cur, table)
            insert_data(cur, table)
        test_table(cur, table)

    conn.commit()


def main():
    conn = sqlite3.connect(r"tpch.sqlite")
    create_tab(conn)
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()
    cur.execute("""
        SELECT player_id, player_name, player_position, player_height, 
               player_weight, player_draft, team_name
        FROM player, team
        WHERE player_team_id = team_id
    """)
    data = cur.fetchall()
    conn.close()
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
    main()
