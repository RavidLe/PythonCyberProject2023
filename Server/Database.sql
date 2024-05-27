-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: water_taps
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(45) NOT NULL,
  `details` varchar(1024) DEFAULT NULL,
  `Date` varchar(45) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
INSERT INTO `reports` VALUES (1,'בעיה בממשק המשתמש','שלום לכם אני מקווה שזה עובד! אמן\n','2024-05-15 12:13:34'),(2,'בעיה בממשק המשתמש','יש לי בעיה שהדיווח לא מתאפס וזה מעצבן מאוד \n','2024-05-15 13:27:19'),(3,'בעיה בממשק המשתמש','יש לי בעיה עם האיפוס של דף הדיווח איזה תוכנה גרועה\n','2024-05-15 13:30:03'),(4,'שם לא נאות לברזייה','לא יפה לקרוא לברזיה קקי\n','2024-05-22 14:10:14'),(5,'בעיה בממשק המשתמש','check\n','2024-05-23 10:36:33');
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taps`
--

DROP TABLE IF EXISTS `taps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `taps` (
  `idTaps` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `X_coord` float NOT NULL,
  `Y_coord` float NOT NULL,
  `Score` double NOT NULL,
  PRIMARY KEY (`idTaps`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taps`
--

LOCK TABLES `taps` WRITE;
/*!40000 ALTER TABLE `taps` DISABLE KEYS */;
INSERT INTO `taps` VALUES (4,'server try',57,23,4),(5,'Hello World!',54,34,3.4),(6,'ניסיון',32.0681,34.7787,4.7),(7,'סבידור מרכז מסוף 2000',32.085,34.7958,3.3),(8,'SQL INJECTION\'',32.1452,34.8359,0),(9,'פארק כפר סבא',32.1816,34.9249,4.3),(10,'הפארק האקולוגי',32.1335,34.892,4.5),(11,'פארק כפר סבא',32.1826,34.9221,3.2),(12,'בית הספר הדמוקרטי ע\"ש יעקוב חזן',32.1912,34.9344,5),(13,'יער קפלן',32.1931,34.9354,1.8),(14,'בן יהודה החי\"ש',32.1848,34.914,3.5),(15,'שבט רכ\"ס',32.1845,34.9133,2.5),(16,'תיכון רבין חוץ',32.1844,34.9125,4.1),(17,'מסלול גלילי',32.1855,34.9082,4.8),(18,'צומת טשרניחובסקי בן יהודה',32.1867,34.9042,3.5),(19,'ספורטק 1',32.1827,34.9298,4.5),(20,'ספורטק 2',32.183,34.9302,4.1),(21,'גן יהודה',32.0819,34.8083,3.8),(22,'בן יהודה ספורטק',32.1832,34.9285,3.5),(23,'מגרש בית הספר הדמוקרטי',32.1909,34.9343,2.2),(24,'1',1,1,1);
/*!40000 ALTER TABLE `taps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdata`
--

DROP TABLE IF EXISTS `userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdata` (
  `id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdata`
--

LOCK TABLES `userdata` WRITE;
/*!40000 ALTER TABLE `userdata` DISABLE KEYS */;
INSERT INTO `userdata` VALUES (1,'Ravid123','5dcf24cc8049c77fa5009bb470062c8311da1895a7556fc95b5868977be3d015'),(2,'1','4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8');
/*!40000 ALTER TABLE `userdata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-27 16:35:36
