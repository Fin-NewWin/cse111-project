CREATE TABLE player (
	player_id INTEGER,
	player_name TEXT,
	player_position TEXT,
	player_height DECIMAL,
	player_weight DECIMAL,
    player_draft TEXT
);

.import data/player.db player
