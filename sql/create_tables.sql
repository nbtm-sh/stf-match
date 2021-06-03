USE `stf`;

CREATE TABLE `tournaments` (        -- Tournaments
    id INT PRIMARY KEY,
    tName TEXT,
    tLocation TEXT
);

CREATE TABLE `players` (    -- Usernames and such
    id INT PRIMARY KEY,
    uName TEXT,
    uCountry TEXT,
    uTeam TEXT
);

CREATE TABLE `roles` (
    id TEXT PRIMARY KEY,
    pManageTournament BIT,
    pManagePlayerLinks BIT,
    pManageDatabase BIT
);

CREATE TABLE `users` (
    id INT PRIMARY KEY,
    uName TEXT,
    uPasswd TEXT,
    uRole TEXT,
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

CREATE TABLE `matches` (
    id INT PRIMARY KEY,
    tTournament INT,
    tRound INT,
    tRoundGroup INT,
    tRoundNick INT,
    tFirstTo INT,
    uPlatform TEXT,
    tMatchType TEXT,
    tMatchWeight INT,
    uPlayer1 INT,
    uPlayer2 INT,

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

    CONSTRAINT `fk_match_id`
        FOREIGN KEY (tMatch) REFERENCES matches (id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    
    CONSTRAINT `fk_tournament_id_invm`
        FOREIGN KEY (tTournament) REFERENCES tournaments (id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);