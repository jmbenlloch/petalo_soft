-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: petalo
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ChannelConfiguration`
--

CREATE DATABASE petalo;
USE petalo;

DROP TABLE IF EXISTS `ChannelConfiguration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ChannelConfiguration` (
  `run_number` int NOT NULL COMMENT 'Run number',
  `daq_id` int NOT NULL,
  `asic_id` int NOT NULL,
  `channel_id` int NOT NULL,
  `param` varchar(100) NOT NULL,
  `value` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ChannelConfiguration`
--

LOCK TABLES `ChannelConfiguration` WRITE;
/*!40000 ALTER TABLE `ChannelConfiguration` DISABLE KEYS */;
/*!40000 ALTER TABLE `ChannelConfiguration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GlobalConfiguration`
--

DROP TABLE IF EXISTS `GlobalConfiguration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GlobalConfiguration` (
  `run_number` int NOT NULL COMMENT 'Run number',
  `daq_id` int NOT NULL,
  `asic_id` int NOT NULL,
  `param` varchar(100) NOT NULL,
  `value` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GlobalConfiguration`
--

LOCK TABLES `GlobalConfiguration` WRITE;
/*!40000 ALTER TABLE `GlobalConfiguration` DISABLE KEYS */;
/*!40000 ALTER TABLE `GlobalConfiguration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Runs`
--

DROP TABLE IF EXISTS `Runs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Runs` (
  `run_number` int NOT NULL COMMENT 'Run number',
  `date` datetime NOT NULL COMMENT 'Start time'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Run numbers';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Runs`
--

LOCK TABLES `Runs` WRITE;
/*!40000 ALTER TABLE `Runs` DISABLE KEYS */;
/*!40000 ALTER TABLE `Runs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-21 18:11:03
