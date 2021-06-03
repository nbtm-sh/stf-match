USE `stf`;

CREATE TABLE `tournaments` (        -- Tournaments
    id INT NOT NULL PRIMARY KEY,
    tName TEXT NOT NULL,
    tLocation TEXT NOT NULL
);

CREATE TABLE `players` (    -- Usernames and such
    id INT NOT NULL,
    uName TEXT NOT NULL,
    uCountry TEXT NOT NULL,
    uTeam TEXT
);

CREATE TABLE `matches` (
    id NOT NULL,
    tTournament INT,
    tRound INT,
    tRoundGroup INT,
    tRoundNick INT,
    tBestOf INT,
    uPlatform TEXT,
    tMatchType TEXT,
    tMatchWeight INT
);

CREATE TABLE `individualMatches` ( -- Actual match results
    id INT NOT NULL AUTO_INREMENT,
    uPlayer1 INT,
    uPlayer2 INT,
    uPlayer1Fighter TEXT,
    uPlayer2Fighter TEXT,
    tDate DATETIME,
    tTournament INT,
    tMatch INT,
    tSeq INT,

    CONSTRAINT `fk_match_id`
        FOREIGN KEY (tMatch) REFERENCES matches(id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    
    CONSTRAINT `fk_tournament_id`
        FOREIGN KEY (tTournament) REFERENCES tournaments(id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    
    CONSTRAINT `fk_player1_id`
        FOREIGN KEY (uPlayer1) REFERENCES players(id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    
    CONSTRAINT `fk_player2_id`
        FOREIGN KEY (uPlayer2) REFERENCES players(id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
    
    CONSTRAINT `fk_match_id`
        FOREIGN KEY (tMatch) REFERENCES matches(id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);