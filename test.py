import sqlite3
from flask import Flask, render_template, request, redirect, url_for

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

    # for row in rows:
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
            season_team_id INTEGER,
            season_mvp INTEGER,
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


def execute_query(sql, values=None, fetchone=False):
    conn = sqlite3.connect("tpch.sqlite")
    cur = conn.cursor()

    if values:
        cur.execute(sql, values)
    else:
        cur.execute(sql)

    if fetchone:
        result = cur.fetchone()
    else:
        result = cur.fetchall()

    conn.commit()
    conn.close()

    return result


def main():
    conn = sqlite3.connect(r"tpch.sqlite")
    create_tab(conn)
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()
    cur.execute(
        """
        SELECT player_id, player_name, player_position, player_height,
               player_weight, player_draft, team_id, team_name
        FROM player, team
        WHERE player_team_id = team_id
    """
    )
    data = cur.fetchall()
    cur.execute("SELECT team_id, team_name FROM team")
    teams = cur.fetchall()
    conn.close()
    return render_template("index.html", data=data, teams=teams)


@app.route("/player_sort/<category>/<int:sort>")
def player_sort(category, sort):
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()
    if sort == 1:
        s = "ASC"
    else:
        s = "DESC"
    cur.execute(
        f"""
        SELECT player_id, player_name, player_position, player_height,
               player_weight, player_draft, team_id, team_name
        FROM player, team
        WHERE player_team_id = team_id
        ORDER BY {category} {s}
    """
    )
    data = cur.fetchall()
    cur.execute("SELECT team_id, team_name FROM team")
    teams = cur.fetchall()
    conn.close()
    return render_template(
        "index.html", data=data, sign=sort, cat=category, teams=teams
    )


@app.route("/player_stats/<int:player_id>/<player_name>")
def player_stats(player_id, player_name):
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *, team_name
        FROM player_stats, team
        WHERE ps_team_id = team_id
              AND ps_player_id = ?
    """,
        (player_id,),
    )
    player_stats_data = cur.fetchall()

    conn.close()

    return render_template(
        "player_stats.html",
        player_stats_data=player_stats_data,
        player_name=player_name,
        player_id=player_id,
    )


@app.route("/player_stats_sort/<int:player_id>/<player_name>/<category>/<int:sort>")
def player_stats_sort(player_id, player_name, category, sort):
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()
    if sort == 1:
        s = "ASC"
    else:
        s = "DESC"
    cur.execute(
        f"""
        SELECT *, team_name
        FROM player_stats, team
        WHERE ps_team_id = team_id
              AND ps_player_id = {player_id}
        ORDER BY {category} {s}
        """
    )

    player_stats_data = cur.fetchall()

    conn.close()
    return render_template(
        "player_stats.html",
        player_stats_data=player_stats_data,
        player_name=player_name,
        player_id=player_id,
        sign=sort,
        cat=category,
    )


@app.route("/team_info/<int:team_id>")
def team_info(team_id):
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()

    # Fetch basic team information with coach name
    cur.execute(
        """
        SELECT *, coach_name, state_name
        FROM team, coach, state
        WHERE team.team_coach = coach_id
            AND team_state_id = state_id
            AND team_id = ?
    """,
        (team_id,),
    )
    team_info_data = cur.fetchone()

    # Fetch team_season data
    cur.execute(
        """
        SELECT * FROM team_season
        WHERE ts_team_id = ?
    """,
        (team_id,),
    )
    team_season_data = cur.fetchall()

    conn.close()

    return render_template(
        "team_info.html",
        team_info_data=team_info_data,
        team_season_data=team_season_data,
        team_id=team_id,
        team_name=team_info_data[1],
    )


@app.route("/team_info_sort/<team_id>/<team_name>/<category>/<int:sort>")
def team_info_sort(team_id, team_name, category, sort):
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()

    # Fetch basic team information with coach name
    if sort == 1:
        s = "ASC"
    else:
        s = "DESC"
    cur.execute(
        """
        SELECT *, coach_name, state_name
        FROM team, coach, state
        WHERE team.team_coach = coach_id
            AND team_state_id = state_id
            AND team_id = ?
    """,
        (team_id,),
    )
    team_info_data = cur.fetchone()

    if category in [
        "ts_season_id",
        "ts_wins",
        "ts_losses",
        "ts_wl",
        "ts_finish",
        "ts_srs",
        "ts_pace",
        "ts_ortg",
        "ts_drtg",
    ]:
        # Fetch team_season data
        cur.execute(
            f"""
            SELECT * FROM team_season
            WHERE ts_team_id = {team_id}
            ORDER BY {category} {s}
        """
        )
    else:
        cur.execute(
            f"""
            SELECT * FROM team_season
            WHERE ts_team_id = {team_id}
        """
        )
    team_season_data = cur.fetchall()

    conn.close()

    return render_template(
        "team_info.html",
        team_info_data=team_info_data,
        team_season_data=team_season_data,
        team_id=team_id,
        team_name=team_info_data[1],
        sign=sort,
        cat=category,
    )


@app.route("/season_accolades/<int:season_id>")
def season_accolades(season_id):
    conn = sqlite3.connect(r"tpch.sqlite")
    cur = conn.cursor()

    # Fetch accolades for the selected season including player names and team names
    cur.execute(
        """
        SELECT season.*,
               team_champion.team_name AS champion_name,
               mvp.player_name AS mvp_name,
               rookie.player_name AS rookie_name,
               points_leader.player_name AS points_leader_name,
               rebounds_leader.player_name AS rebounds_leader_name,
               assists_leader.player_name AS assists_leader_name,
               win_share.player_name AS win_share_name
        FROM season
        LEFT JOIN team AS team_champion ON season.season_team_id = team_champion.team_id
        LEFT JOIN player AS mvp ON season.season_mvp = mvp.player_id
        LEFT JOIN player AS rookie ON season.season_rookie = rookie.player_id
        LEFT JOIN player AS points_leader ON season.season_point = points_leader.player_id
        LEFT JOIN player AS rebounds_leader ON season.season_rbs = rebounds_leader.player_id
        LEFT JOIN player AS assists_leader ON season.season_ast = assists_leader.player_id
        LEFT JOIN player AS win_share ON season.season_wins = win_share.player_id
        WHERE season_id = ?
    """,
        (season_id,),
    )
    season_accolades_data = cur.fetchone()

    conn.close()

    return render_template(
        "season_accolades.html", season_accolades_data=season_accolades_data
    )


@app.route("/add_player", methods=["GET", "POST"])
def add_player_route():
    if request.method == "POST":
        player_name = request.form.get("playerName")
        player_position = request.form.get("playerPosition")
        player_height = request.form.get("playerHeight")
        player_weight = request.form.get("playerWeight")
        player_draft = request.form.get("playerDraft")
        team_id = request.form.get("teamId")

        # Insert player data into the 'player' table
        sql = "INSERT INTO player (player_name, player_position, player_height, player_weight, player_draft, player_team_id) VALUES (?, ?, ?, ?, ?, ?)"
        values = (
            player_name,
            player_position,
            player_height,
            player_weight,
            player_draft,
            team_id,
        )
        execute_query(sql, values)

        # Redirect to the index
        return redirect(url_for("index"))

    # Render the form with the team dropdown options
    return render_template("index.html")


if __name__ == "__main__":
    main()
    app.run(debug=True)
