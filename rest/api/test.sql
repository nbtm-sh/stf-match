SELECT `p1`.`uName` AS p1Name, `p2`.`uName` AS p2Name, uPlayer1Fighter, uPlayer2Fighter, tWinner
FROM `individualMatches`
INNER JOIN `matches` ON (`individualMatches`.`tTournament`=`matches`.`tTournament` AND `individualMatches`.`tMatch`=`matches`.`tRound`)
INNER JOIN `players` p1 ON (`matches`.`uPlayer1` = `p1`.`id`)
INNER JOIN `players` p2 ON (`matches`.`uPlayer2` = `p2`.`id`)
WHERE `uPlayer1`=15 OR `uPlayer2`=15;