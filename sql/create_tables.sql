USE `stf`;

CREATE TABLE `tournaments` (        -- Tournaments
    id INT NOT NULL PRIMARY KEY,
    tName TEXT NOT NULL,
    tLocation TEXT NOT NULL
);

CREATE TABLE `players` (    -- Usernames and such
    id INT NOT NULL,
    uName TEXT NOT NULL,
    uCountry TEXT NOT NULL
);

CREATE TABLE `matches` (
    id INT NOT NULL,
    uPlayer1 INT, -- NULL = DQ
    uPlayer2 INT,
    uPlayer1Fighter TEXT,
    uPlayer2Fighter TEXT,
    tDate DATETIME,
    tRound INT,
    tResult INT, -- 1 = Player 1, 2 = Player 2
    FOREIGN KEY (uPlayer1) REFERENCES players(id),
    FOREIGN KEY (uPlayer2) REFERENCES players(id)
);