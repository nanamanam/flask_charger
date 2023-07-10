-- --------------------------------------------------------
-- Host:                         35.247.144.180
-- Server version:               8.0.31-google - (Google)
-- Server OS:                    Linux
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for charger_db
-- CREATE DATABASE IF NOT EXISTS `charger_db` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `nanaagri_charger`;

-- Dumping structure for table charger_db.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  `attemp` int NOT NULL DEFAULT '0',
  `lock_status` int NOT NULL DEFAULT '0',
  `line_id` varchar(255) NOT NULL DEFAULT '0',
  `line_regis` int NOT NULL DEFAULT '0',
  `group_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;

-- Dumping data for table charger_db.auth_user: ~3 rows (approximately)
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` (`id`, `username`, `password`, `status`, `attemp`, `lock_status`, `line_id`, `line_regis`, `group_id`) VALUES
	(22, 'test', '1ad698aa44c1e89d5f0bdd92d77b3fdce809fd0708f81447a3808fa8', 1, 0, 0, '0', 0, 0),
	(23, 'admin', '60942afe35dfce41119951f497068500f624f86f86ede4d055db8f18', 1, 0, 0, 'Ucd590c2a81b67c8074448c617fd89a91', 2, 0);
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;

-- Dumping structure for table charger_db.charger_point
CREATE TABLE IF NOT EXISTS `charger_point` (
  `point_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `uptime` varchar(255) DEFAULT NULL,
  `downtime` varchar(255) DEFAULT NULL,
  `plug1` float DEFAULT '0',
  `plug2` float DEFAULT '0',
  `max_volt1` float DEFAULT '0',
  `max_volt2` float DEFAULT '0',
  `max_a1` float DEFAULT '0',
  `max_a2` float DEFAULT '0',
  `emer_stat` float DEFAULT '0',
  `plug1_type` varchar(50) DEFAULT NULL,
  `plug2_type` varchar(50) DEFAULT NULL,
  `zone` int DEFAULT NULL,
  PRIMARY KEY (`point_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;



-- Dumping structure for table charger_db.error_log
CREATE TABLE IF NOT EXISTS `error_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Time` varchar(50) NOT NULL DEFAULT '0',
  `point_id` int DEFAULT '0',
  `log` varchar(50) DEFAULT '0',
  `status` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;

-- Dumping data for table charger_db.error_log: ~0 rows (approximately)
/*!40000 ALTER TABLE `error_log` DISABLE KEYS */;
INSERT INTO `error_log` (`id`, `Time`, `point_id`, `log`, `status`) VALUES
	(1, '2023-07-06 11:00', 5, '10221', 0),
	(2, '2023-07-06 11:00', 2, '10221', 0),
	(3, '2023-07-06 11:00', 9, '10221', 0),
	(4, '2023-07-06 11:10', 9, '10222', 0),
	(5, '2023-07-06 11:00', 1, '10221', 0),
	(6, '2023-07-06 11:01', 1, '10222', 0);
/*!40000 ALTER TABLE `error_log` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
