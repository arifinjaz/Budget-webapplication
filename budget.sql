CREATE DATABASE  IF NOT EXISTS `budget` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `budget`;
-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: budget
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `CATEGORYID` int NOT NULL AUTO_INCREMENT,
  `CATEGORY` varchar(100) DEFAULT NULL,
  `USERID` int DEFAULT NULL,
  PRIMARY KEY (`CATEGORYID`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'TEST',1),(2,'TEST',1),(3,'TEST1',1),(4,'TEST2',1),(5,'TEST3',1),(30,'Testing',3),(31,'Important',3),(35,'Repayment',3),(37,'GENERAL',3),(38,'HOME',3);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `expensesid` int NOT NULL AUTO_INCREMENT,
  `AMOUNT` int NOT NULL,
  `FIXEDEXPENSEID` int NOT NULL,
  `CATEGORYID` int NOT NULL,
  `SUBCATID` int NOT NULL,
  `expensesdescription` varchar(100) NOT NULL,
  `USERID` int DEFAULT NULL,
  `CreationDate` date NOT NULL,
  PRIMARY KEY (`expensesid`),
  KEY `CATEGORYID` (`CATEGORYID`),
  KEY `SUBCATID` (`SUBCATID`),
  KEY `FIXEDEXPENSEID` (`FIXEDEXPENSEID`),
  KEY `USERID` (`USERID`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`CATEGORYID`) REFERENCES `category` (`CATEGORYID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`SUBCATID`) REFERENCES `subcat` (`SUBCATID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `expenses_ibfk_3` FOREIGN KEY (`FIXEDEXPENSEID`) REFERENCES `fixedexpenses` (`FIXEDEXPENSEID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `expenses_ibfk_4` FOREIGN KEY (`USERID`) REFERENCES `users` (`USERID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (18,200,6,35,11,'Testing',3,'0000-00-00'),(20,200,12,37,34,'aa',3,'2021-01-26'),(22,200,9,38,35,'Fuel',3,'2021-01-27'),(24,100,9,38,35,'car',3,'2021-01-27'),(25,200,12,37,34,'vegetable',3,'2021-02-13'),(26,3500,9,38,36,'Maid salary',3,'2021-02-14'),(27,12000,6,35,37,'Ayesha Personal Loan',3,'2021-02-14'),(28,800,9,38,35,'Gas',3,'2021-02-14'),(29,350,9,38,35,'Car wash',3,'2021-02-14'),(30,10000,9,38,35,'testing overspent',3,'2021-02-14');
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fixed_expenses`
--

DROP TABLE IF EXISTS `fixed_expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fixed_expenses` (
  `FIXEDEXPENSEID` int NOT NULL AUTO_INCREMENT,
  `AMOUNT` int NOT NULL,
  `CATEGORYID` int NOT NULL,
  `FIXEDEXPENSES` varchar(100) NOT NULL,
  PRIMARY KEY (`FIXEDEXPENSEID`),
  KEY `CATEGORYID` (`CATEGORYID`),
  CONSTRAINT `fixed_expenses_ibfk_1` FOREIGN KEY (`CATEGORYID`) REFERENCES `category` (`CATEGORYID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fixed_expenses`
--

LOCK TABLES `fixed_expenses` WRITE;
/*!40000 ALTER TABLE `fixed_expenses` DISABLE KEYS */;
/*!40000 ALTER TABLE `fixed_expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fixedexpenses`
--

DROP TABLE IF EXISTS `fixedexpenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fixedexpenses` (
  `FIXEDEXPENSEID` int NOT NULL AUTO_INCREMENT,
  `AMOUNT` int NOT NULL,
  `CATEGORYID` int NOT NULL,
  `USERID` int NOT NULL,
  `COMMENTS` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`FIXEDEXPENSEID`),
  KEY `CATEGORYID` (`CATEGORYID`),
  KEY `USERID` (`USERID`),
  CONSTRAINT `fixedexpenses_ibfk_1` FOREIGN KEY (`CATEGORYID`) REFERENCES `category` (`CATEGORYID`),
  CONSTRAINT `fixedexpenses_ibfk_2` FOREIGN KEY (`USERID`) REFERENCES `users` (`USERID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fixedexpenses`
--

LOCK TABLES `fixedexpenses` WRITE;
/*!40000 ALTER TABLE `fixedexpenses` DISABLE KEYS */;
INSERT INTO `fixedexpenses` VALUES (6,25000,35,3,'Loans'),(9,8000,38,3,'home'),(12,50000,37,3,'TESTING');
/*!40000 ALTER TABLE `fixedexpenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcat`
--

DROP TABLE IF EXISTS `subcat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcat` (
  `SUBCATID` int NOT NULL AUTO_INCREMENT,
  `AMOUNT` int NOT NULL,
  `CATEGORYID` int NOT NULL,
  `SUBCATNAME` varchar(100) NOT NULL,
  `USERID` int DEFAULT NULL,
  PRIMARY KEY (`SUBCATID`),
  KEY `CATEGORYID` (`CATEGORYID`),
  KEY `USERID` (`USERID`),
  KEY `idx_subcat_SUBCATNAME` (`SUBCATNAME`),
  CONSTRAINT `subcat_ibfk_1` FOREIGN KEY (`CATEGORYID`) REFERENCES `category` (`CATEGORYID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `subcat_ibfk_2` FOREIGN KEY (`CATEGORYID`) REFERENCES `fixedexpenses` (`CATEGORYID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `subcat_ibfk_3` FOREIGN KEY (`USERID`) REFERENCES `users` (`USERID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcat`
--

LOCK TABLES `subcat` WRITE;
/*!40000 ALTER TABLE `subcat` DISABLE KEYS */;
INSERT INTO `subcat` VALUES (11,2000,35,'toi',3),(34,20000,37,'General',3),(35,2000,38,'home',3),(36,3500,38,'Maid',3),(37,18500,35,'Personal Loans',3),(38,4200,35,'Bike Loan',3);
/*!40000 ALTER TABLE `subcat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `USERID` int NOT NULL AUTO_INCREMENT,
  `FIRSTNAME` varchar(100) NOT NULL,
  `LASTNAME` varchar(100) NOT NULL,
  `EMAIL` varchar(100) NOT NULL,
  `USERNAME` varchar(100) NOT NULL,
  `PASSWORD` text NOT NULL,
  PRIMARY KEY (`USERID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'aa','aa','aa','aa','pbkdf2:sha256:150000$nbDXsspL$9f9dbe863fa34f17407cd9947038b62af3e8e5438a84e441908ba5b4b56f0e56'),(4,'aw','aw','aw','aw','pbkdf2:sha256:150000$Uy4QKiH1$89b3697c592338218902eb15eb63a789bd6edff59abbfc5d3b683b3673b049ee'),(5,'ese','ese','ese','ese','pbkdf2:sha256:150000$xTuhYJoc$58ee9be89ef634a841e1272af9b865c047718b6cc7b804dcc32699b8cde4ac2f'),(6,'red','rder','gfedr','rdr','pbkdf2:sha256:150000$6yqCKvFm$f4117014943a141918d643ed54c36b23fbc6061fb30319bc9b4841ad0f49948e'),(7,'Arif','Shaikh','arif.injaz@gmail.com','arif','pbkdf2:sha256:150000$6VXn7aaJ$857415de97c3b9bd23580a0550de0d8f8a20c699f736b23fc0f7231acbc1b9a0'),(8,'test','test','arif.inaz@gmail.com','hsgh','pbkdf2:sha256:150000$PCjOENWa$1dfd488f4a55bc5f5704699e8499848e6b63275a43c9f3774eeb3817d702e219');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'budget'
--

--
-- Dumping routines for database 'budget'
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_ALL_SUBCAT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GET_ALL_SUBCAT`(IN USERID INT)
BEGIN

SELECT S.CATEGORY,SUBCATNAME,AMOUNT,USERNAME FROM 
SUBCAT SU 
INNER JOIN CATEGORY S ON S.CATEGORYID = SU.CATEGORYID
INNER JOIN USERS U ON U.USERID = SU.USERID
WHERE SU.USERID = USERID;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `INS_EXPENSES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `INS_EXPENSES`(
IN CATNAME varchar(100),
IN SUBCATNAME varchar(100),
IN AMOUNT INT,
IN USERID INT,
IN DESCRIPTIONS varchar(100),
IN CREATIONDATE date
)
BEGIN

SET @FEXPID = (SELECT FIXEDEXPENSEID FROM fixedexpenses WHERE CATEGORYID IN (SELECT CATEGORYID FROM CATEGORY WHERE CATEGORY = CATNAME) LIMIT 1);
SET @CATID = (SELECT CATEGORYID FROM CATEGORY WHERE CATEGORY = CATNAME LIMIT 1);
SET @SUBCATID = (SELECT SUBCATID FROM SUBCAT WHERE SUBCAT.SUBCATNAME = SUBCATNAME LIMIT 1); #WHERE SUBCATNAME IN (SUBCATNAME) LIMIT 1);

INSERT INTO EXPENSES (AMOUNT, FIXEDEXPENSEID, CATEGORYID, SUBCATID, expensesdescription, USERID,CREATIONDATE) VALUES (AMOUNT,@FEXPID,@CATID,@SUBCATID,DESCRIPTIONS,USERID,CREATIONDATE);

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `INS_SUBCAT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `INS_SUBCAT`(
IN CATNAME varchar(100),
IN SUBCATNAME varchar(100),
IN AMOUNT INT,
IN USERID INT
)
BEGIN

DECLARE CATID INT DEFAULT 0;
SET CATID = (SELECT CATEGORYID FROM CATEGORY WHERE CATEGORY = CATNAME);

INSERT INTO SUBCAT (AMOUNT,SUBCATNAME,CATEGORYID,USERID) VALUES (AMOUNT,SUBCATNAME,CATID,USERID);

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-14 18:34:10
