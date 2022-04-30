-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: projeto_redes
-- ------------------------------------------------------
-- Server version	8.0.28

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

USE Storage;

--
-- Table structure for table `produto`
--

DROP TABLE IF EXISTS `produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produto` (
  `ID_PROD` int NOT NULL,
  `Quantidade` int NOT NULL,
  `Data_fabricacao` date NOT NULL,
  `Data_vencimento` date NOT NULL,
  `lote` int NOT NULL,
  `origem` varchar(50) NOT NULL,
  `fk_Categorias_ID_CATEGORIA` int NOT NULL,
  PRIMARY KEY (`ID_PROD`),
  UNIQUE KEY `ID_PROD_UNIQUE` (`ID_PROD`),
  KEY `FK_Produto_2` (`fk_Categorias_ID_CATEGORIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (1,23,'2001-01-22','2010-10-23',17,'Nestlé Campinas',1),(2,43,'2001-01-22','2010-10-23',27,'Coca-Cola Jundiaí',2),(3,46,'2001-01-22','2010-10-23',37,'Kicaldo',3),(4,3,'2001-01-22','2010-10-23',789,'Minas Bonafonte',4),(5,23,'2001-01-22','2010-10-23',28,'Swift',5),(6,54,'2001-01-22','2010-10-23',278,'Uruguai',6),(7,23,'2001-01-22','2010-10-23',1780,'Heineken',7),(8,35,'2001-01-22','2010-10-23',2314,'Cisnei',8),(9,2,'2001-01-22','2010-10-23',35142,'Swift',9),(10,45,'2001-01-22','2010-10-23',156,'Soya',10),(11,23,'2001-01-22','2010-10-23',436,'Zulu',11),(12,23,'2001-01-22','2010-10-23',534,'Galo',12);
/*!40000 ALTER TABLE `produto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-25 22:10:45
