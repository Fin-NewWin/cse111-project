
-- 1. Show all state with a count of teams
SELECT 
    state_name as state, 
    COUNT(team_id) as cnt 
FROM 
    state, 
    team 
WHERE 
    state_id = team_state_id 
GROUP BY state_id;

-- 2. Show team total wins(up to 2004)
SELECT
    team_name as team,
    COUNT(DISTINCT season_id) as wins
FROM
    team,
    season
WHERE team_id = season_team_id
GROUP BY team_name;

-- 3. Show player avg stats in all season per in team
SELECT
    player_name as player,
    team_name as team,
    AVG(ps_g) as height,
    AVG(ps_fg) as weight
FROM
    player,
    player_stats,
    team
WHERE
    player_id = ps_player_id
    AND team_id = ps_team_id
GROUP BY
    player_name,
    team_name;

-- 4. Show how long players have been in team
SELECT
    player_name as player,
    team_name as team,
    COUNT(DISTINCT ps_season_id) as years
FROM
    player,
    player_stats,
    team
WHERE
    player_id = ps_player_id
    AND team_id = ps_team_id
GROUP BY
    player_name,
    team_name;

-- 5. Shows team avg stats
SELECT
    team_name as team,
    AVG(ts_wins) as wins,
    AVG(ts_losses) as losses,
    AVG(ts_wl) as win_loss_ratio
FROM
    team,
    team_season
WHERE
    team_id = ts_team_id
GROUP BY
    team_name;

-- 6. Show which team doesn't have a mascot
SELECT
    team_name as mascotless_team
FROM
    team
WHERE
    team_mascot = '';

-- 7. Show team best performance in wins
SELECT
    team_name as team,
    ts_season_id as season,
    MAX(ts_wins) as wins
FROM
    team,
    team_season
WHERE
    team_id = ts_team_id
GROUP BY
    team_name
ORDER BY
    ts_wins DESC;


-- 8. Show state with no team
SELECT
    state_name as state
FROM
    state,
    team
WHERE
    state_id NOT IN (
        SELECT
            team_state_id
        FROM
            team)
GROUP BY state_name;

-- 9. Show players who are above avg NBA height
SELECT
    player_name as player,
    player_height as height
FROM
    player
WHERE
    player_height > (
        SELECT
            AVG(player_height)
        FROM
            player)
GROUP BY
    player_name;

-- 10. Show players with total games played
SELECT
    player_name as player,
    SUM(ps_g) as games
FROM
    player,
    player_stats
WHERE
    player_id = ps_player_id
GROUP BY
    player_name;

-- 11. Get all stats of player searched
SELECT
    *
FROM
    player,
    player_stats
WHERE
    player_name = 'Lebron James'
    AND 
    player_id = ps_player_id;

-- 12. Player with avg higher in each season

SELECT
    player_name as player,
    ps_season_id as season,
    ps_pts,
    ps_blk
FROM
    player,
    player_stats,
    (SELECT AVG(ps_pts) as avg_pts FROM player_stats),
    (SELECT AVG(ps_blk) as avg_blk FROM player_stats)
WHERE
    player_id = ps_player_id
    AND
    ps_pts > avg_pts
    AND
    ps_blk > avg_blk
GROUP BY 
    player_name,
    ps_season_id;

-- 13. Retrieve All Triple-Doubles in a Season:
SELECT
    player_name as player,
    ps_season_id as season
FROM
    player,
    player_stats
WHERE
    player_id = ps_player_id
    AND
    ps_pts >= 10
    AND
    ps_ast >= 10
    AND
    ps_trb >= 10
GROUP BY
    player_name,
    ps_season_id;

-- 14. Show all player who played the most
SELECT
    player_name as player,
    ps_season_id as season,
    MAX(ps_pts) as pts
FROM
    player,
    player_stats
WHERE
    player_id = ps_player_id
GROUP BY
    player_name,
    ps_season_id;

-- 15. Show player with best points/minute
SELECT
    player_name as player,
    ps_season_id as season,
    MAX(ps_pts/ps_mp) as pts_per_min
FROM
    player,
    player_stats
WHERE
    player_id = ps_player_id
GROUP BY
    player_name,
    ps_season_id;

-- 16. Show player with the most mvp
SELECT
    player_name as player,
    COUNT(season_id) as mvp
FROM
    player,
    season
WHERE
    player_id = season_mvp
GROUP BY
    player_name
ORDER BY
    mvp DESC;

-- 17. Show player with the most rookie
SELECT
    player_name as player,
    COUNT(season_id) as rookie
FROM
    player,
    season
WHERE
    player_id = season_rookie
GROUP BY
    player_name
ORDER BY
    rookie DESC;

-- 18. Show player as point leader
SELECT
    player_name as player,
    COUNT(season_id) as point
FROM
    player,
    season
WHERE
    player_id = season_point
GROUP BY
    player_name
ORDER BY
    point DESC;

-- 19. Which game did the home team won
SELECT
    game_id as game,
    game_home_pts as pts
FROM
    game
WHERE
    game_home_pts > game_away_pts
GROUP BY
    game_id
ORDER BY
    pts DESC;
-- 20. Show player with a quad-double
SELECT
    player_name as player,
    ps_season_id as season
FROM
    player,
    player_stats
WHERE
    player_id = ps_player_id
    AND
    ps_pts >= 10
    AND
    ps_ast >= 10
    AND
    ps_trb >= 10
    AND
    (ps_stl >= 10 OR ps_blk >= 10)
GROUP BY
    player_name,
    ps_season_id;
