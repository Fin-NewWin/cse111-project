CREATE TABLE player (
	player_id INTEGER,
	player_name TEXT,
	player_position TEXT,
	player_height DECIMAL,
	player_weight DECIMAL,
    player_draft TEXT
);

CREATE TABLE player_stats (
    ps_player_id INTEGER,
    ps_season_id INTEGER,
    ps_team_id INTEGER,
    ps_games INTEGER,
    ps_pts DECIMAL,
    ps_trb DECIMAL,
    ps_ast DECIMAL,
    ps_fg DECIMAL,
    ps_fg3 DECIMAL,
    ps_ft DECIMAL,
    ps_efg DECIMAL
);

.import data/player.db player
.import data/player_stats.db player_stats
