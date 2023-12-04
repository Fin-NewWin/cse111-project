import sqlite3

conn = sqlite3.connect(r"tpch.sqlite")
cur = conn.cursor()

sql = """
CREATE TABLE IF NOT EXISTS state (
    state_id INTEGER PRIMARY KEY,
    state_name TEXT
)
"""
cur.execute(sql)
conn.commit

f = open("data/state.db", "r")

lines = f.readlines()

for line in lines:
    line = line.strip().split("|")
    sql = "INSERT INTO state VALUES(?,?)"
    cur.execute(sql, (list(line)))


# for row in arr:

# cur.execute(sql)
# conn.commit

sql = """
    SELECT * FROM state
"""
cur.execute(sql)
rows = cur.fetchall()

for row in rows:
    print(row)


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

conn.close()
