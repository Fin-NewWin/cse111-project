.headers on

CREATE TABLE player (
    player_id INTEGER,
	player_name TEXT,
	player_position TEXT,
	player_height DECIMAL,
	player_weight DECIMAL,
    player_draft TEXT,
    player_team_id INTEGER
);

CREATE TABLE player_stats (
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
);

CREATE TABLE state (
    state_id INTEGER,
    state_name TEXT
);

CREATE TABLE team (
    team_id INTEGER,
    team_name TEXT,
    team_mascot TEXT,
    team_state_id INTEGER,
    team_conference TEXT,
    team_division TEXT,
	team_coach_id INTEGER
);

CREATE TABLE team_season (
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
);

CREATE TABLE season (
    season_id INTEGER,
    season_team_id INTEGER,
    season_mvp INTEGER,
    season_rookie INTEGER,
    season_point INTEGER,
    season_rbs INTEGER,
    season_ast INTEGER,
    season_wins INTEGER
);

CREATE TABLE game (
    game_id INTEGER,
    game_season_id INTEGER,
    game_away_team_id INTEGER,
    game_away_pts INTEGER,
    game_home_team_id INTEGER,
    game_home_pts INTEGER,
    game_type TEXT
);

CREATE TABLE coach (
	coach_id INTEGER,
	coach_name TEXT
);



.import data/player.db player
.import data/season.db season
.import data/player_stats.db player_stats
.import data/state.db state
.import data/team.db team
.import data/team_season.db team_season
.import data/game.db game
.import data/coach.db coach

-- SELECT * FROM player;

-- INSERT INTO player(player_id, player_name, player_position, player_height, player_weight, player_draft)
-- VALUES (870, 'Stephen Curry', 'Point Guard', 188, 83, 2009);

-- SELECT * FROM player;

-- UPDATE player
-- SET player_weight = 77
-- WHERE player_id = 870;

-- SELECT * FROM player;

-- DELETE FROM  player
-- WHERE player_id = 870;

-- SELECT * FROM player;
