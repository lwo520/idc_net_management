SET NAMES utf8mb4;


# ------------------------------------------------------------

# DROP TABLE IF EXISTS `continent`;
#
# CREATE TABLE `continent` (
#   `id` int(8) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
#   `cn_name` varchar(16) DEFAULT NULL COMMENT '中文名',
#   `en_name` varchar(16) DEFAULT NULL COMMENT '英文名',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `continent` WRITE;
/*!40000 ALTER TABLE `continent` DISABLE KEYS */;

INSERT INTO `continent` (`id`, `cn_name`, `en_name`)
VALUES
	(1,'亚洲','Asia'),
	(2,'欧洲','Europe'),
	(3,'非洲','Africa'),
	(4,'大洋洲','Oceania'),
	(5,'南极洲','Antarctica'),
	(6,'北美洲','North America'),
	(7,'南美洲','South America');

/*!40000 ALTER TABLE `continent` ENABLE KEYS */;
UNLOCK TABLES;