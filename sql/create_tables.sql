USE `stf`;

CREATE TABLE `tournaments` (        -- Tournaments
    id INT PRIMARY KEY,
    tName TEXT,
    tLocation TEXT,
    tDate DATE
);

CREATE TABLE `players` (    -- Usernames and such
    id INT PRIMARY KEY,
    uName TEXT,
    uCountry TEXT,
    uTeam TEXT,
    uJoinDate DATE,
    uIgnore BIT
);

CREATE TABLE `roles` (
    id VARCHAR(16) PRIMARY KEY,
    pManageTournament BIT,
    pManagePlayerLinks BIT,
    pManageDatabase BIT
);

CREATE TABLE `users` (
    id INT PRIMARY KEY,
    uName TEXT,
    uPasswd TEXT,
    uRole VARCHAR(16),
    uLinkedPlayer INT,

    CONSTRAINT `fk_linked_player`
        FOREIGN KEY (uLinkedPlayer) REFERENCES players (id)
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    
    CONSTRAINT `fk_roles`
        FOREIGN KEY (uRole) REFERENCES roles (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE `entrants` (
    id INT PRIMARY KEY,
    uPlayerId INT,
    tTournament INT,

    CONSTRAINT `fk_player_entrants`
        FOREIGN KEY (uPlayerId) REFERENCES players(id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    
    CONSTRAINT `fk_tournament_entrants`
        FOREIGN KEY (tTournament) REFERENCES tournaments(id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE `playerScoresCache` (
    id INT PRIMARY KEY,
    uPlayerId INT,
    uScore FLOAT,
    tTournament INT, -- NULL or other invalid value for overall score

    CONSTRAINT `fk_player_score`
        FOREIGN KEY (uPlayerId) REFERENCES players(id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE `matches` (
    id INT PRIMARY KEY,
    tTournament INT,
    tRound INT,
    tRoundGroup INT,
    tRoundNick TEXT,
    tFirstTo INT,
    uPlatform TEXT,
    tMatchType TEXT,
    tMatchWeight INT,
    uPlayer1 INT,
    uPlayer2 INT,
    uDq INT, -- 0=No one, 1=Player1, 2=Player2, 3=Both
    tBracket TEXT, -- Loosers, Winners, None

    CONSTRAINT `fk_tournament_id_match`
        FOREIGN KEY (tTournament) REFERENCES tournaments (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    
    CONSTRAINT `fk_player1_id`
        FOREIGN KEY (uPlayer1) REFERENCES players (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    
    CONSTRAINT `fk_player2_id`
        FOREIGN KEY (uPlayer2) REFERENCES players (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE `individualMatches` ( -- Actual match results
    id INT PRIMARY KEY,
    uPlayer1Fighter TEXT,
    uPlayer2Fighter TEXT,
    tDate DATETIME,
    tTournament INT,
    tMatch INT,
    tSeq INT,
    tWinner INT,
    tMatchTime INT,

    CONSTRAINT `fk_match_id`
        FOREIGN KEY (tMatch) REFERENCES matches (id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    
    CONSTRAINT `fk_tournament_id_invm`
        FOREIGN KEY (tTournament) REFERENCES tournaments (id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE `ignore` ( -- Players to ignore from official rankings because they have been disqualified or otherwise
    id INT PRIMARY KEY,
    uPlayerId INT,

    CONSTRAINT `fk_player_ignore`
        FOREIGN KEY (uPlayerId) REFERENCES players(id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);