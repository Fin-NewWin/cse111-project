import sqlite3

conn = sqlite3.connect('')
cursor = conn.cursor()

def display_menu():
    print("\nMenu:")
    print("1. View Player Information")
    print("2. View Team Information")
    print("3. View Season Information")
    print("4. Exit")

def view_player_information():
    cursor.execute("SELECT * FROM player")
    players = cursor.fetchall()

    print("\nPlayer Information:")
    for player in players:
        print(player)

def view_team_information():
    cursor.execute("SELECT * FROM team")
    teams = cursor.fetchall()

    print("\nTeam Information:")
    for team in teams:
        print(team)

def view_season_information():
    cursor.execute("SELECT * FROM season")
    seasons = cursor.fetchall()

    print("\nSeason Information:")
    for season in seasons:
        print(season)

while True:
    display_menu()
    choice = input("Enter the number of your choice: ")

    if choice == '1':
        view_player_information()
    elif choice == '2':
        view_team_information()
    elif choice == '3':
        view_season_information()
    elif choice == '4':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Please enter a valid number.")

conn.close()
