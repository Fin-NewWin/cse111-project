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


.import data/player.db player
.import data/player_stats.db player_stats
