import sqlite3


def checkTable(cur, table: str):
    sql = f"""
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'
    """
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True


def testTable(cur, table: str):
    sql = f"""
        SELECT * FROM {table}
    """
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        print(row)


def insertData(cur, table: str):
    f = open(f"data/{table}.db", "r")
    lines = f.readlines()

    n = len(lines[0].strip().split("|"))
    s = (n * "?,")[:-1]

    for line in lines:
        line = line.strip().split("|")
        sql = f"INSERT INTO {table} VALUES({s})"
        cur.execute(sql, (list(line)))


def createTables(conn):
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
        cur.execute(sqls[table])

        if not checkTable(cur, table):
            insertData(cur, table)
        testTable(cur, table)

    conn.commit()


def main():
    conn = sqlite3.connect(r"tpch.sqlite")
    createTables(conn)
    conn.close()


# def display_menu():
#     print("\nMenu:")
#     print("1. View Player Information")
#     print("2. View Team Information")
#     print("3. View Season Information")
#     print("4. Exit")


# def view_player_information():
#     cur.execute("SELECT * FROM team")
#     players = cur.fetchall()

#     print("\nPlayer Information:")
#     for player in players:
#         print(player)


# def view_team_information():
#     cur.execute("SELECT * FROM team")
#     teams = cur.fetchall()

#     print("\nTeam Information:")
#     for team in teams:
#         print(team)


# def view_season_information():
#     cur.execute("SELECT * FROM season")
#     seasons = cur.fetchall()

#     print("\nSeason Information:")
#     for season in seasons:
#         print(season)


# while True:
#     display_menu()
#     choice = input("Enter the number of your choice: ")

#     if choice == "1":
#         view_player_information()
#     elif choice == "2":
#         view_team_information()
#     elif choice == "3":
#         view_season_information()
#     elif choice == "4":
#         print("Exiting the program. Goodbye!")
#         break
#     else:
#         print("Please enter a valid number.")


if __name__ == "__main__":
    main()
