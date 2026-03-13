/*
SQLyog Community v13.2.1 (64 bit)
MySQL - 8.0.31 : Database - h2o_packing_data_base_tables
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`h2o_packing_data_base_tables` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `h2o_packing_data_base_tables`;

/*Table structure for table `bundle` */

DROP TABLE IF EXISTS `bundle`;

CREATE TABLE `bundle` (
  `bundle_id` int NOT NULL AUTO_INCREMENT,
  `SKU_Id` int NOT NULL,
  `active_flag` enum('Yes','No') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Yes',
  `deleted_flag` enum('No','Yes') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'No',
  `size` varchar(255) DEFAULT NULL,
  `LENGTH` varchar(255) DEFAULT NULL,
  `pcs_lift` varchar(255) DEFAULT NULL,
  `ft_lift` varchar(255) DEFAULT NULL,
  `lifts_load` varchar(255) DEFAULT NULL,
  `load_percentage` varchar(255) DEFAULT NULL,
  `ft_load` varchar(255) DEFAULT NULL,
  `SOURCE` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`bundle_id`),
  KEY `SKU_Id` (`SKU_Id`)
) ENGINE=MyISAM AUTO_INCREMENT=429 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `bundle` */

insert  into `bundle`(`bundle_id`,`SKU_Id`,`active_flag`,`deleted_flag`,`size`,`LENGTH`,`pcs_lift`,`ft_lift`,`lifts_load`,`load_percentage`,`ft_load`,`SOURCE`) values 
(1,1,'Yes','No','14','20','9','180','8','12.5','1440','jme_CIODLoadingChart'),
(360,292,'Yes','No','16','20','6','120','4','10.0','1200','jme_SolvetWeldLoadingChart_0'),
(359,291,'Yes','No','14','20','9','180','4','10.7','1680','jme_SolvetWeldLoadingChart_0'),
(4,4,'Yes','No','10','20','16','320','8','12.5','2560','jme_CIODLoadingChart'),
(5,5,'Yes','No','8 DR 14','20','15','300','12','8.3','3600','jme_CIODLoadingChart'),
(358,290,'Yes','No','12 (West)*','20','6','120','8','5.4','2240','jme_SolvetWeldLoadingChart_0'),
(7,7,'Yes','No','6','20','28','560','12','8.3','6720','jme_CIODLoadingChart'),
(8,8,'Yes','No','4','20','60','1200','12','8.3','14400','jme_CIODLoadingChart'),
(9,9,'Yes','No','48','14','2','28','3','33.3','84','jme_GravitySewerLoadingChart'),
(10,10,'Yes','No','42','14','2','28','6','16.7','168','jme_GravitySewerLoadingChart'),
(11,11,'Yes','No','36','14','2','28','6','16.7','168','jme_GravitySewerLoadingChart'),
(12,12,'Yes','No','30 (West)*','14','3','42','9','11.1','378','jme_GravitySewerLoadingChart'),
(13,13,'Yes','No','30','14','3','42','6','16.7','252','jme_GravitySewerLoadingChart'),
(14,14,'Yes','No','27','14','3','42','9','11.1','378','jme_GravitySewerLoadingChart'),
(15,15,'Yes','No','24 (West)*','14','4','56','12','8.3','672','jme_GravitySewerLoadingChart'),
(357,289,'Yes','No','12','20','6','120','6','7.1','1680','jme_SolvetWeldLoadingChart_0'),
(17,17,'Yes','No','21','14','4','56','12','8.3','672','jme_GravitySewerLoadingChart'),
(356,227,'Yes','No','20','20','2','40','4','5.0','800','jme_20FTIrrigationLoadingChart'),
(19,19,'Yes','No','15','14','9','126','12','8.3','1512','jme_GravitySewerLoadingChart'),
(20,20,'Yes','No','12 (West)*','14','16','224','12','8.3','2688','jme_GravitySewerLoadingChart'),
(355,226,'Yes','No','18','20','4','80','4','8.0','1000','jme_20FTIrrigationLoadingChart'),
(354,225,'Yes','No','18','20','2','40','2','4.0','1000','jme_20FTIrrigationLoadingChart'),
(23,23,'Yes','No','8 (West)*','14','36','504','12','8.3','6048','jme_GravitySewerLoadingChart'),
(353,224,'Yes','No','15','20','3','60','4','3.9','1520','jme_20FTIrrigationLoadingChart'),
(25,25,'Yes','No','6','14','40','560','18','5.6','10080','jme_GravitySewerLoadingChart'),
(26,26,'Yes','No','4','14','84','1176','18','5.6','21168','jme_GravitySewerLoadingChart'),
(27,27,'Yes','No','48','20','2','40','2','50.0','80','jme_GravitySewerLoadingChart'),
(28,28,'Yes','No','36','20','2','40','4','25.0','160','jme_GravitySewerLoadingChart'),
(29,29,'Yes','No','42','20','2','40','4','25.0','160','jme_GravitySewerLoadingChart'),
(30,30,'Yes','No','30 (West)*','20','3','60','6','16.7','360','jme_GravitySewerLoadingChart'),
(31,31,'Yes','No','30','20','3','60','4','25.0','240','jme_GravitySewerLoadingChart'),
(32,32,'Yes','No','27','20','3','60','6','16.7','360','jme_GravitySewerLoadingChart'),
(33,33,'Yes','No','24 (West)*','20','4','80','8','12.5','640','jme_GravitySewerLoadingChart'),
(352,223,'Yes','No','12','20','8','160','6','7.0','2280','jme_20FTIrrigationLoadingChart'),
(35,35,'Yes','No','21','20','4','80','8','12.5','640','jme_GravitySewerLoadingChart'),
(351,218,'Yes','No','24','20','2','40','4','8.3','480','jme_20FTIrrigationLoadingChart'),
(37,37,'Yes','No','15','20','9','180','8','12.5','1440','jme_GravitySewerLoadingChart'),
(38,38,'Yes','No','12 (West)*','20','16','320','8','12.5','2560','jme_GravitySewerLoadingChart'),
(350,216,'Yes','No','18','20','6','120','2','12.0','1000','jme_20FTIrrigationLoadingChart'),
(349,215,'Yes','No','18','20','4','80','2','8.0','1000','jme_20FTIrrigationLoadingChart'),
(41,41,'Yes','No','8 (West)*','20','36','720','8','12.5','5760','jme_GravitySewerLoadingChart'),
(348,212,'Yes','No','10','20','12','240','6','7.4','3240','jme_20FTIrrigationLoadingChart'),
(43,43,'Yes','No','6','20','40','800','12','8.3','9600','jme_GravitySewerLoadingChart'),
(44,44,'Yes','No','4','20','84','1680','12','8.3','20160','jme_GravitySewerLoadingChart'),
(347,207,'Yes','No','24','22','2','44','4','8.3','528','jme_22FTIrrigationPIPLoadingChart'),
(346,205,'Yes','No','18','22','6','132','2','12.0','1100','jme_22FTIrrigationPIPLoadingChart'),
(47,47,'Yes','No','10','20','8','160','16','6.3','2560','jme_IPSPressureLoadingChart'),
(345,204,'Yes','No','18','22','4','88','2','8.0','1100','jme_22FTIrrigationPIPLoadingChart'),
(344,201,'Yes','No','10','22','12','264','6','7.4','3564','jme_22FTIrrigationPIPLoadingChart'),
(343,182,'Yes','No','16','20','6','120','2','12.0','1000','jme_CIODLoadingChart'),
(51,51,'Yes','No','10','20','12','240','12','8.3','2880','jme_IPSPressureLoadingChart'),
(52,52,'Yes','No','8','20','15','300','12','8.3','3600','jme_IPSPressureLoadingChart'),
(342,181,'Yes','No','16','20','4','80','2','8.0','1000','jme_CIODLoadingChart'),
(54,54,'Yes','No','1 1/2','20','270','5400','16','6.3','86400','jme_IPSPressureLoadingChart'),
(55,55,'Yes','No','2','20','185','3700','16','6.3','59200','jme_IPSPressureLoadingChart'),
(56,56,'Yes','No','2 1/2','20','73','1460','28','3.6','40880','jme_IPSPressureLoadingChart'),
(341,180,'Yes','No','12','20','6','120','6','6.1','1960','jme_CIODLoadingChart'),
(58,58,'Yes','No','5 (West)*','20','38','760','16','6.3','12160','jme_IPSPressureLoadingChart'),
(340,178,'Yes','No','8 CL150','20','25','500','4','11.4','4400','jme_CIODLoadingChart'),
(60,60,'Yes','No','2','40','185','7400','8','12.5','59200','jme_IPSPressureLoadingChart'),
(339,177,'Yes','No','6','20','28','560','4','7.1','7840','jme_CIODLoadingChart'),
(62,62,'Yes','No','5','20','38','760','12','8.3','9120','jme_IPSPressureLoadingChart'),
(63,63,'Yes','No','4 (West)*','20','48','960','20','5.0','19200','jme_IPSPressureLoadingChart'),
(64,64,'Yes','No','4','20','76','1520','12','8.3','18240','jme_IPSPressureLoadingChart'),
(65,65,'Yes','No','3 (West)*','20','75','1500','20','5.0','30000','jme_IPSPressureLoadingChart'),
(66,66,'Yes','No','3','20','75','1500','16','6.3','24000','jme_IPSPressureLoadingChart'),
(338,169,'Yes','No','18','20','4','80','4','10.0','800','jme_CIODLoadingChart'),
(337,168,'Yes','No','16','20','6','120','2','12.0','1000','jme_CIODLoadingChart'),
(336,167,'Yes','No','16','20','4','80','2','8.0','1000','jme_CIODLoadingChart'),
(335,166,'Yes','No','12 (West)*','20','6','120','8','5.4','2240','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(71,71,'Yes','No','6 (West)*','20','26','520','16','6.3','8320','jme_IPSPressureLoadingChart'),
(334,120,'Yes','No','12','20','6','120','6','7.1','1680','jme_YellowGasSleeveLoadingChart'),
(73,73,'Yes','No','3','40','100','4000','6','16.7','24000','jme_IPSPressureLoadingChart'),
(333,110,'Yes','No','12','20','6','120','6','7.1','1680','jme_YellowGasSleeveLoadingChart'),
(75,75,'Yes','No','4','20','60','1200','12','8.3','14400','LoadingChart C900_2-3-2017'),
(76,76,'Yes','No','6','20','28','560','12','8.3','6720','LoadingChart C900_2-3-2017'),
(332,99,'Yes','No','16','20','6','120','2','12.0','1000','LoadingChart C900_2-3-2017'),
(78,78,'Yes','No','8 DR 14','20','15','300','12','8.3','3600','LoadingChart C900_2-3-2017'),
(79,79,'Yes','No','10','20','16','320','8','12.5','2560','LoadingChart C900_2-3-2017'),
(331,98,'Yes','No','16','20','4','80','2','8.0','1000','LoadingChart C900_2-3-2017'),
(330,97,'Yes','No','12','20','6','120','6','6.1','1960','LoadingChart C900_2-3-2017'),
(329,95,'Yes','No','8 CL150','20','25','500','4','11.4','4400','LoadingChart C900_2-3-2017'),
(83,83,'Yes','No','14','20','9','180','8','12.5','1440','LoadingChart C900_2-3-2017'),
(328,94,'Yes','No','6','20','28','560','4','7.1','7840','LoadingChart C900_2-3-2017'),
(327,86,'Yes','No','18','20','4','80','4','10.0','800','LoadingChart C900_2-3-2017'),
(326,85,'Yes','No','16','20','6','120','2','12.0','1000','LoadingChart C900_2-3-2017'),
(87,87,'Yes','No','20','20','4','80','8','12.5','640','LoadingChart C900_2-3-2017'),
(88,88,'Yes','No','24','20','3','60','6','16.7','360','LoadingChart C900_2-3-2017'),
(89,89,'Yes','No','30','20','3','60','4','25.0','240','LoadingChart C900_2-3-2017'),
(90,90,'Yes','No','30 (West)*','20','3','60','6','16.7','360','LoadingChart C900_2-3-2017'),
(91,91,'Yes','No','36','20','2','40','4','25.0','160','LoadingChart C900_2-3-2017'),
(92,92,'Yes','No','42','20','2','40','4','25.0','160','LoadingChart C900_2-3-2017'),
(93,93,'Yes','No','48','20','2','40','2','50.0','80','LoadingChart C900_2-3-2017'),
(325,84,'Yes','No','16','20','4','80','2','8.0','1000','LoadingChart C900_2-3-2017'),
(324,82,'Yes','No','12 DR 14','20','6','120','6','7.1','1680','LoadingChart C900_2-3-2017'),
(96,96,'Yes','No','10','20','8','160','16','6.3','2560','LoadingChart C900_2-3-2017'),
(323,81,'Yes','No','12 DR 18','20','9','180','2','9.2','1960','LoadingChart C900_2-3-2017'),
(322,80,'Yes','No','12 DR 18','20','6','120','4','6.1','1960','LoadingChart C900_2-3-2017'),
(321,77,'Yes','No','8 DR 18','20','15','300','8','7.5','4000','LoadingChart C900_2-3-2017'),
(100,100,'Yes','No','1','20','275','5500','32','3.13','176000','jme_YellowGasSleeveLoadingChart'),
(101,101,'Yes','No','1 1/2','20','168','3360','32','3.13','107520','jme_YellowGasSleeveLoadingChart'),
(102,102,'Yes','No','2','20','105','2100','28','3.57','58800','jme_YellowGasSleeveLoadingChart'),
(103,103,'Yes','No','2 (PTA)*','20','140','2800','20','5.00','56000','jme_YellowGasSleeveLoadingChart'),
(104,104,'Yes','No','3','20','60','1200','24','4.17','28800','jme_YellowGasSleeveLoadingChart'),
(105,105,'Yes','No','3 (PTA)*','20','88','1760','16','6.25','28160','jme_YellowGasSleeveLoadingChart'),
(106,106,'Yes','No','4','20','57','1140','16','6.25','18240','jme_YellowGasSleeveLoadingChart'),
(107,107,'Yes','No','6','20','26','520','16','6.25','8320','jme_YellowGasSleeveLoadingChart'),
(108,108,'Yes','No','8','20','15','300','16','6.25','4800','jme_YellowGasSleeveLoadingChart'),
(109,109,'Yes','No','10','20','12','240','12','8.33','2880','jme_YellowGasSleeveLoadingChart'),
(320,74,'Yes','No','12','20','12','240','2','12.2','1960','jme_IPSPressureLoadingChart'),
(111,111,'Yes','No','1','20','275','5500','32','3.13','176000','jme_YellowGasSleeveLoadingChart'),
(112,112,'Yes','No','1 1/4','20','196','3920','32','3.13','125440','jme_YellowGasSleeveLoadingChart'),
(113,113,'Yes','No','1 1/2','20','151','3020','32','3.13','96640','jme_YellowGasSleeveLoadingChart'),
(114,114,'Yes','No','2','20','105','2100','28','3.57','58800','jme_YellowGasSleeveLoadingChart'),
(115,115,'Yes','No','3','20','60','1200','24','4.17','28800','jme_YellowGasSleeveLoadingChart'),
(116,116,'Yes','No','4','20','57','1140','16','6.25','18240','jme_YellowGasSleeveLoadingChart'),
(117,117,'Yes','No','6','20','26','520','16','6.25','8320','jme_YellowGasSleeveLoadingChart'),
(118,118,'Yes','No','8','20','15','300','16','6.25','4800','jme_YellowGasSleeveLoadingChart'),
(119,119,'Yes','No','10','20','12','240','12','8.33','2880','jme_YellowGasSleeveLoadingChart'),
(319,72,'Yes','No','8','40','10','400','4','10.0','4000','jme_IPSPressureLoadingChart'),
(121,121,'Yes','No','10','10','48','480','32','3.13','15360','jme_YellowGasSleeveLoadingChart'),
(122,122,'Yes','No','6','10','26','260','32','3.13','8320','jme_YellowGasSleeveLoadingChart'),
(123,123,'Yes','No','1','20','400','8000','20','5.00','160000','jme_UtilityDuctLoadingChart'),
(124,124,'Yes','No','1 1/2','20','225','4500','20','5.00','90000','jme_UtilityDuctLoadingChart'),
(125,125,'Yes','No','2','20','140','2800','20','5.00','56000','jme_UtilityDuctLoadingChart'),
(126,126,'Yes','No','2 1/2','20','131','2620','16','6.25','41920','jme_UtilityDuctLoadingChart'),
(127,127,'Yes','No','3','20','100','2000','12','8.33','24000','jme_UtilityDuctLoadingChart'),
(128,128,'Yes','No','3 (West)*','20','100','2000','16','6.25','32000','jme_UtilityDuctLoadingChart'),
(129,129,'Yes','No','3 1/2','20','63','1260','16','6.25','20160','jme_UtilityDuctLoadingChart'),
(130,130,'Yes','No','4','20','57','1140','12','8.33','13680','jme_UtilityDuctLoadingChart'),
(131,131,'Yes','No','4 (West)*','20','57','1140','16','6.25','18240','jme_UtilityDuctLoadingChart'),
(132,132,'Yes','No','5','20','38','760','12','8.33','9120','jme_UtilityDuctLoadingChart'),
(133,133,'Yes','No','5 (West)*','20','38','760','16','6.25','12160','jme_UtilityDuctLoadingChart'),
(134,134,'Yes','No','6','20','26','520','12','8.33','6240','jme_UtilityDuctLoadingChart'),
(135,135,'Yes','No','6 (West)*','20','26','520','16','6.25','8320','jme_UtilityDuctLoadingChart'),
(136,136,'Yes','No','2','10','234','2340','32','3.13','74880','jme_UtilityDuctLoadingChart'),
(137,137,'Yes','No','3','10','100','1000','32','3.13','32000','jme_UtilityDuctLoadingChart'),
(138,138,'Yes','No','4','10','63','630','32','3.13','20160','jme_UtilityDuctLoadingChart'),
(139,139,'Yes','No','2','20','234','4680','16','6.25','74880','jme_UtilityDuctLoadingChart'),
(140,140,'Yes','No','3','20','100','2000','16','6.25','32000','jme_UtilityDuctLoadingChart'),
(141,141,'Yes','No','4','20','63','1260','16','6.25','20160','jme_UtilityDuctLoadingChart'),
(142,142,'Yes','No','4','20','63','1260','16','6.25','20160','jme_UtilityDuctLoadingChart'),
(143,143,'Yes','No','1','20','250','5000','36','2.78','180000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(144,144,'Yes','No','1 1/4','20','200','4000','28','3.57','112000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(145,145,'Yes','No','1 1/2','20','150','3000','28','3.57','84000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(146,146,'Yes','No','2','20','100','2000','28','3.57','56000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(147,147,'Yes','No','1','20','120','2400','40','2.50','96000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(148,148,'Yes','No','1 1/4','20','100','2000','40','2.50','80000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(149,149,'Yes','No','1 1/2','20','90','1800','40','2.50','72000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(150,150,'Yes','No','2','20','53','1060','40','2.50','42400','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(151,151,'Yes','No','1','20','120','2400','40','2.50','96000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(152,152,'Yes','No','1 1/4','20','100','2000','40','2.50','80000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(153,153,'Yes','No','1 1/2','20','90','1800','40','2.50','72000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(154,154,'Yes','No','2','20','53','1060','40','2.50','42400','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(155,155,'Yes','No','2','20','105','2100','28','3.6','58800','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(156,156,'Yes','No','4','20','57','1140','12','8.3','13680','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(157,157,'Yes','No','4 (West)*','20','29','580','28','3.6','16240','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(158,158,'Yes','No','4 1/2','20','26','520','24','4.2','12480','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(159,159,'Yes','No','5','20','23','460','20','5.0','9200','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(160,160,'Yes','No','5 (West)*','20','23','460','24','4.2','11040','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(161,161,'Yes','No','6','20','20','400','16','6.3','6400','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(162,162,'Yes','No','6 (West)*','20','20','400','20','5.0','8000','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(163,163,'Yes','No','8','20','15','300','12','8.3','3600','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(164,164,'Yes','No','8 (West)*','20','20','400','12','8.3','4800','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(165,165,'Yes','No','10','20','12','240','12','8.3','2880','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(318,70,'Yes','No','8','20','25','500','4','11.4','4400','jme_IPSPressureLoadingChart'),
(317,69,'Yes','No','8 (West)*','20','20','400','6','7.6','5280','jme_IPSPressureLoadingChart'),
(316,68,'Yes','No','10','20','16','320','4','11.1','2880','jme_IPSPressureLoadingChart'),
(315,67,'Yes','No','12','20','9','180','2','9.1','1960','jme_IPSPressureLoadingChart'),
(170,170,'Yes','No','20','20','4','80','8','12.5','640','jme_CIODLoadingChart'),
(171,171,'Yes','No','24','20','3','60','6','16.7','360','jme_CIODLoadingChart'),
(172,172,'Yes','No','30','20','3','60','4','25.0','240','jme_CIODLoadingChart'),
(173,173,'Yes','No','30 (West)*','20','3','60','6','16.7','360','jme_CIODLoadingChart'),
(174,174,'Yes','No','36','20','2','40','4','25.0','160','jme_CIODLoadingChart'),
(175,175,'Yes','No','42','20','2','40','4','25.0','160','jme_CIODLoadingChart'),
(176,176,'Yes','No','48','20','2','40','2','50.0','80','jme_CIODLoadingChart'),
(314,61,'Yes','No','12 / 16','20','12','240','2','12.2','1960','jme_IPSPressureLoadingChart'),
(313,59,'Yes','No','6','40','28','1120','2','14.3','7840','jme_IPSPressureLoadingChart'),
(179,179,'Yes','No','10','20','8','160','16','6.3','2560','jme_CIODLoadingChart'),
(312,57,'Yes','No','6','20','28','560','4','7.1','7840','jme_IPSPressureLoadingChart'),
(311,53,'Yes','No','4','40','38','1520','2','9.1','16720','jme_IPSPressureLoadingChart'),
(310,50,'Yes','No','12','20','6','120','6','7.1','1680','jme_IPSPressureLoadingChart'),
(183,183,'Yes','No','1 1/2','10','180','1800','48','2.1','86400','jme_ABSLoadingChart'),
(184,184,'Yes','No','2','10','105','1050','48','2.1','50400','jme_ABSLoadingChart'),
(185,185,'Yes','No','3','10','75','750','32','3.1','24000','jme_ABSLoadingChart'),
(186,186,'Yes','No','4','10','57','570','32','3.1','18240','jme_ABSLoadingChart'),
(187,187,'Yes','No','4 (West)*','10','57','570','24','4.2','13680','jme_ABSLoadingChart'),
(188,188,'Yes','No','6','10','26','260','24','4.2','6240','jme_ABSLoadingChart'),
(189,189,'Yes','No','6 (West)*','10','26','260','32','3.1','8320','jme_ABSLoadingChart'),
(190,190,'Yes','No','1 1/2','20','180','3600','24','4.2','86400','jme_ABSLoadingChart'),
(191,191,'Yes','No','2','20','105','2100','24','4.2','50400','jme_ABSLoadingChart'),
(192,192,'Yes','No','3','20','75','1500','16','6.3','24000','jme_ABSLoadingChart'),
(193,193,'Yes','No','4','20','57','1140','12','8.3','13680','jme_ABSLoadingChart'),
(194,194,'Yes','No','4 (West)*','20','57','1140','16','6.3','18240','jme_ABSLoadingChart'),
(195,195,'Yes','No','5','20','38','760','16','6.3','12160','jme_ABSLoadingChart'),
(196,196,'Yes','No','5 (West)*','20','38','760','12','8.3','9120','jme_ABSLoadingChart'),
(197,197,'Yes','No','6','20','26','520','12','8.3','6240','jme_ABSLoadingChart'),
(198,198,'Yes','No','6 (West)*','20','26','520','16','6.3','8320','jme_ABSLoadingChart'),
(199,199,'Yes','No','6','22','40','880','12','8.3','10560','jme_22FTIrrigationPIPLoadingChart'),
(200,200,'Yes','No','8','22','36','792','8','12.5','6336','jme_22FTIrrigationPIPLoadingChart'),
(309,49,'Yes','No','6','20','28','560','4','7.1','7840','jme_IPSPressureLoadingChart'),
(202,202,'Yes','No','12','22','16','352','8','12.5','2816','jme_22FTIrrigationPIPLoadingChart'),
(203,203,'Yes','No','15','22','9','198','8','12.5','1584','jme_22FTIrrigationPIPLoadingChart'),
(308,48,'Yes','No','8','20','25','500','4','11.4','4400','jme_IPSPressureLoadingChart'),
(307,46,'Yes','No','12','20','6','120','4','6.1','1960','jme_IPSPressureLoadingChart'),
(206,206,'Yes','No','21','22','4','88','8','12.5','704','jme_22FTIrrigationPIPLoadingChart'),
(306,45,'Yes','No','12','20','9','180','2','9.2','1960','jme_IPSPressureLoadingChart'),
(208,208,'Yes','No','24','22','4','88','8','12.5','704','jme_22FTIrrigationPIPLoadingChart'),
(209,209,'Yes','No','27','22','3','66','6','16.7','396','jme_22FTIrrigationPIPLoadingChart'),
(210,210,'Yes','No','6','20','40','800','12','8.3','9600','jme_20FTIrrigationLoadingChart'),
(211,211,'Yes','No','8','20','36','720','8','12.5','5760','jme_20FTIrrigationLoadingChart'),
(305,42,'Yes','No','8','20','30','600','4','11.4','5280','jme_GravitySewerLoadingChart'),
(213,213,'Yes','No','12','20','16','320','8','12.5','2560','jme_20FTIrrigationLoadingChart'),
(214,214,'Yes','No','15','20','9','180','8','12.5','1440','jme_20FTIrrigationLoadingChart'),
(304,40,'Yes','No','10','20','12','240','6','7.4','3240','jme_GravitySewerLoadingChart'),
(303,39,'Yes','No','12','20','12','240','4','10.7','2240','jme_GravitySewerLoadingChart'),
(217,217,'Yes','No','21','20','4','80','8','12.5','640','jme_20FTIrrigationLoadingChart'),
(302,36,'Yes','No','18','20','4','80','2','8.0','1000','jme_GravitySewerLoadingChart'),
(219,219,'Yes','No','24 (West)*','20','4','80','8','12.5','640','jme_20FTIrrigationLoadingChart'),
(220,220,'Yes','No','27','20','3','60','6','16.7','360','jme_20FTIrrigationLoadingChart'),
(221,221,'Yes','No','8','20','14','280','16','6.3','4480','jme_20FTIrrigationLoadingChart'),
(222,222,'Yes','No','10','20','11','220','12','8.3','2640','jme_20FTIrrigationLoadingChart'),
(301,34,'Yes','No','24','20','2','40','4','8.3','480','jme_GravitySewerLoadingChart'),
(300,24,'Yes','No','8','14','30','420','6','7.5','5544','jme_GravitySewerLoadingChart'),
(299,22,'Yes','No','10','14','12','168','9','4.9','3402','jme_GravitySewerLoadingChart'),
(298,21,'Yes','No','12','14','12','168','6','7.1','2352','jme_GravitySewerLoadingChart'),
(297,18,'Yes','No','18','14','4','56','3','5.3','1050','jme_GravitySewerLoadingChart'),
(228,228,'Yes','No','1/2','10','300','3000','80','1.25','240000','ElectricalConduitLoadingChart_0'),
(229,229,'Yes','No','3/4','10','220','2200','80','1.25','176000','ElectricalConduitLoadingChart_0'),
(230,230,'Yes','No','1','10','180','1800','80','1.25','144000','ElectricalConduitLoadingChart_0'),
(231,231,'Yes','No','1 1/4','10','90','900','80','1.25','72000','ElectricalConduitLoadingChart_0'),
(232,232,'Yes','No','1 1/2','10','90','900','80','1.25','72000','ElectricalConduitLoadingChart_0'),
(233,233,'Yes','No','2','10','70','700','72','1.39','50400','ElectricalConduitLoadingChart_0'),
(234,234,'Yes','No','2 1/2','10','50','500','56','1.79','28000','ElectricalConduitLoadingChart_0'),
(235,235,'Yes','No','2 1/2 (West)*','10','50','500','64','1.56','32000','ElectricalConduitLoadingChart_0'),
(236,236,'Yes','No','3','10','50','500','48','2.08','24000','ElectricalConduitLoadingChart_0'),
(237,237,'Yes','No','1/2','10','600','6000','72','1.39','432000','ElectricalConduitLoadingChart_0'),
(238,238,'Yes','No','3/4','10','440','4400','56','1.79','246400','ElectricalConduitLoadingChart_0'),
(239,239,'Yes','No','1','10','360','3600','48','2.08','172800','ElectricalConduitLoadingChart_0'),
(240,240,'Yes','No','1 1/4','10','330','3300','40','2.50','132000','ElectricalConduitLoadingChart_0'),
(241,241,'Yes','No','1 1/2','10','225','2250','40','2.50','90000','ElectricalConduitLoadingChart_0'),
(242,242,'Yes','No','2','10','140','1400','40','2.50','56000','ElectricalConduitLoadingChart_0'),
(243,243,'Yes','No','2 1/2','10','93','930','40','2.50','37200','ElectricalConduitLoadingChart_0'),
(244,244,'Yes','No','3','10','88','880','32','3.13','28160','ElectricalConduitLoadingChart_0'),
(245,245,'Yes','No','3 1/2','10','63','630','32','3.13','20160','ElectricalConduitLoadingChart_0'),
(246,246,'Yes','No','4','10','57','570','24','4.17','13680','ElectricalConduitLoadingChart_0'),
(247,247,'Yes','No','4 (West)*','10','57','570','32','3.13','18240','ElectricalConduitLoadingChart_0'),
(248,248,'Yes','No','5','10','38','380','24','4.17','9120','ElectricalConduitLoadingChart_0'),
(249,249,'Yes','No','6','10','26','260','24','4.17','6240','ElectricalConduitLoadingChart_0'),
(250,250,'Yes','No','6 (West)*','10','26','260','32','3.13','8320','ElectricalConduitLoadingChart_0'),
(251,251,'Yes','No','1/2','10','300','3000','104','0.96','312000','jme_SolvetWeldLoadingChart_0'),
(252,252,'Yes','No','1/2 (West)*','10','300','3000','112','0.89','336000','jme_SolvetWeldLoadingChart_0'),
(253,253,'Yes','No','3/4','10','220','2200','88','1.1','193600','jme_SolvetWeldLoadingChart_0'),
(254,254,'Yes','No','3/4 (West)*','10','220','2200','96','1.0','211200','jme_SolvetWeldLoadingChart_0'),
(255,255,'Yes','No','1','10','180','1800','80','1.3','144000','jme_SolvetWeldLoadingChart_0'),
(256,256,'Yes','No','1 (West)*','10','180','1800','88','1.1','158400','jme_SolvetWeldLoadingChart_0'),
(257,257,'Yes','No','1 1/4','10','90','900','88','1.1','79200','jme_SolvetWeldLoadingChart_0'),
(258,258,'Yes','No','1 1/4 (West)*','10','90','900','96','1.0','86400','jme_SolvetWeldLoadingChart_0'),
(259,259,'Yes','No','1 1/2','10','90','900','80','1.3','72000','jme_SolvetWeldLoadingChart_0'),
(260,260,'Yes','No','2','10','105','1050','48','2.1','50400','jme_SolvetWeldLoadingChart_0'),
(261,261,'Yes','No','2 1/2','10','73','730','48','2.1','35040','jme_SolvetWeldLoadingChart_0'),
(262,262,'Yes','No','3','10','75','750','32','3.1','24000','jme_SolvetWeldLoadingChart_0'),
(263,263,'Yes','No','3 (West)*','10','75','750','40','2.5','30000','jme_SolvetWeldLoadingChart_0'),
(264,264,'Yes','No','4','10','57','570','24','4.2','13680','jme_SolvetWeldLoadingChart_0'),
(265,265,'Yes','No','4 (West)*','10','57','570','32','3.1','18240','jme_SolvetWeldLoadingChart_0'),
(266,266,'Yes','No','6','10','26','260','24','4.2','6240','jme_SolvetWeldLoadingChart_0'),
(267,267,'Yes','No','6 (West)*','10','26','260','32','3.1','8320','jme_SolvetWeldLoadingChart_0'),
(268,268,'Yes','No','1/2','20','360','7200','36','2.8','259200','jme_SolvetWeldLoadingChart_0'),
(269,269,'Yes','No','1/2 (West)*','20','360','7200','40','2.5','288000','jme_SolvetWeldLoadingChart_0'),
(270,270,'Yes','No','3/4','20','400','8000','24','4.2','192000','jme_SolvetWeldLoadingChart_0'),
(271,271,'Yes','No','3/4 (West)*','20','400','8000','28','3.6','224000','jme_SolvetWeldLoadingChart_0'),
(272,272,'Yes','No','1','20','280','5600','20','5.0','112000','jme_SolvetWeldLoadingChart_0'),
(273,273,'Yes','No','1 (West)*','20','280','5600','24','4.2','134400','jme_SolvetWeldLoadingChart_0'),
(274,274,'Yes','No','1 1/4','20','220','4400','24','4.2','105600','jme_SolvetWeldLoadingChart_0'),
(275,275,'Yes','No','1 1/4 (West)*','20','220','4400','28','3.6','123200','jme_SolvetWeldLoadingChart_0'),
(276,276,'Yes','No','1 1/2','20','180','3600','24','4.2','86400','jme_SolvetWeldLoadingChart_0'),
(277,277,'Yes','No','2','20','105','2100','24','4.2','50400','jme_SolvetWeldLoadingChart_0'),
(278,278,'Yes','No','2 1/2','20','73','1460','24','4.2','35040','jme_SolvetWeldLoadingChart_0'),
(279,279,'Yes','No','3','20','75','1500','16','6.3','24000','jme_SolvetWeldLoadingChart_0'),
(280,280,'Yes','No','4','20','57','1140','12','8.3','13680','jme_SolvetWeldLoadingChart_0'),
(281,281,'Yes','No','4 (West)*','20','57','1140','16','6.3','18240','jme_SolvetWeldLoadingChart_0'),
(282,282,'Yes','No','5','20','38','760','12','8.3','9120','jme_SolvetWeldLoadingChart_0'),
(283,283,'Yes','No','5 (West)*','20','38','760','16','6.3','12160','jme_SolvetWeldLoadingChart_0'),
(284,284,'Yes','No','6','20','26','520','12','8.3','6240','jme_SolvetWeldLoadingChart_0'),
(285,285,'Yes','No','6 (West)*','20','26','520','16','6.3','8320','jme_SolvetWeldLoadingChart_0'),
(286,286,'Yes','No','8','20','15','300','12','8.3','3600','jme_SolvetWeldLoadingChart_0'),
(287,287,'Yes','No','8 (West)*','20','20','400','12','8.3','4800','jme_SolvetWeldLoadingChart_0'),
(288,288,'Yes','No','10','20','12','240','12','8.3','2880','jme_SolvetWeldLoadingChart_0'),
(296,16,'Yes','No','24','14','2','28','6','5.6','504','jme_GravitySewerLoadingChart'),
(295,6,'Yes','No','8 DR 18','20','15','300','8','7.5','4000','jme_CIODLoadingChart'),
(294,3,'Yes','No','12 DR 18','20','6','120','4','6.1','1960','jme_CIODLoadingChart'),
(293,2,'Yes','No','12 DR 14','20','6','120','6','7.1','1680','jme_CIODLoadingChart'),
(361,2,'Yes','No','12 DR 14','20','8','160','6','9.5','1680','jme_CIODLoadingChart'),
(362,3,'Yes','No',' 25','20','8','160','4','8.2','1960','jme_CIODLoadingChart'),
(363,6,'Yes','No',' 25','20','20','400','4','10.0','4000','jme_CIODLoadingChart'),
(364,16,'Yes','No','24','14','4','56','6','11.1','504','jme_GravitySewerLoadingChart'),
(365,18,'Yes','No','18','14','6','84','3','8.0','1050','jme_GravitySewerLoadingChart'),
(366,21,'Yes','No','12','14','16','224','6','9.5','2352','jme_GravitySewerLoadingChart'),
(367,22,'Yes','No','10','14','15','210','9','6.2','3402','jme_GravitySewerLoadingChart'),
(368,24,'Yes','No','8','14','36','504','6','9.1','5544','jme_GravitySewerLoadingChart'),
(369,34,'Yes','No','24','20','4','80','4','16.7','480','jme_GravitySewerLoadingChart'),
(370,36,'Yes','No','18','20','6','120','2','12.0','1000','jme_GravitySewerLoadingChart'),
(371,39,'Yes','No','12','20','16','320','4','14.3','2240','jme_GravitySewerLoadingChart'),
(372,40,'Yes','No','10','20','15','300','6','9.3','3240','jme_GravitySewerLoadingChart'),
(373,42,'Yes','No','8','20','36','720','4','13.6','5280','jme_GravitySewerLoadingChart'),
(374,45,'Yes','No','12','20','12','240','2','12.2','1960','jme_IPSPressureLoadingChart'),
(375,46,'Yes','No','12','20','8','160','4','8.2','1960','jme_IPSPressureLoadingChart'),
(376,48,'Yes','No','8','20','30','600','4','13.6','4400','jme_IPSPressureLoadingChart'),
(377,49,'Yes','No','6','20','35','700','8','8.9','7840','jme_IPSPressureLoadingChart'),
(378,50,'Yes','No','12','20','8','160','6','9.5','1680','jme_IPSPressureLoadingChart'),
(379,53,'Yes','No','4','40','57','2280','6','13.6','16720','jme_IPSPressureLoadingChart'),
(380,57,'Yes','No','6','20','35','700','8','8.9','7840','jme_IPSPressureLoadingChart'),
(381,59,'Yes','No','6','40','35','1400','4','17.9','7840','jme_IPSPressureLoadingChart'),
(382,61,'Yes','No','12 / 16','20','16','320','2','16.3','1960','jme_IPSPressureLoadingChart'),
(383,67,'Yes','No','12','20','12','240','2','12.2','1960','jme_IPSPressureLoadingChart'),
(384,68,'Yes','No','10','20','20','400','4','13.9','2880','jme_IPSPressureLoadingChart'),
(385,69,'Yes','No','8 (West)*','20','24','480','6','9.1','5280','jme_IPSPressureLoadingChart'),
(386,70,'Yes','No','8','20','30','600','4','13.6','4400','jme_IPSPressureLoadingChart'),
(387,72,'Yes','No','8','40','15','600','4','15.0','4000','jme_IPSPressureLoadingChart'),
(388,74,'Yes','No','12','20','16','320','2','16.3','1960','jme_IPSPressureLoadingChart'),
(389,77,'Yes','No',' 25','20','20','400','4','10.0','4000','LoadingChart C900_2-3-2017'),
(390,80,'Yes','No',' 25','20','8','160','4','8.2','1960','LoadingChart C900_2-3-2017'),
(391,81,'Yes','No',' 25','20','12','240','2','12.2','1960','LoadingChart C900_2-3-2017'),
(392,82,'Yes','No','12 DR 14','20','8','160','6','9.5','1680','LoadingChart C900_2-3-2017'),
(393,84,'Yes','No','16','20','6','120','2','12.0','1000','LoadingChart C900_2-3-2017'),
(394,85,'Yes','No','16','20','9','180','2','18.0','1000','LoadingChart C900_2-3-2017'),
(395,86,'Yes','No','18','20','6','120','4','15.0','800','LoadingChart C900_2-3-2017'),
(396,94,'Yes','No','6','20','35','700','8','8.9','7840','LoadingChart C900_2-3-2017'),
(397,95,'Yes','No','8 CL150','20','30','600','4','13.6','4400','LoadingChart C900_2-3-2017'),
(398,97,'Yes','No','12','20','8','160','6','8.2','1960','LoadingChart C900_2-3-2017'),
(399,98,'Yes','No','16','20','6','120','2','12.0','1000','LoadingChart C900_2-3-2017'),
(400,99,'Yes','No','16','20','9','180','2','18.0','1000','LoadingChart C900_2-3-2017'),
(401,110,'Yes','No','12','20','8','160','6','9.5','1680','jme_YellowGasSleeveLoadingChart'),
(402,120,'Yes','No','12','20','8','160','6','9.5','1680','jme_YellowGasSleeveLoadingChart'),
(403,166,'Yes','No','12 (West)*','20','8','160','8','7.1','2240','jme_ThreadedDropPipe-WellCasingLaodingChart'),
(404,167,'Yes','No','16','20','6','120','2','12.0','1000','jme_CIODLoadingChart'),
(405,168,'Yes','No','16','20','9','180','2','18.0','1000','jme_CIODLoadingChart'),
(406,169,'Yes','No','18','20','6','120','4','15.0','800','jme_CIODLoadingChart'),
(407,177,'Yes','No','6','20','35','700','8','8.9','7840','jme_CIODLoadingChart'),
(408,178,'Yes','No','8 CL150','20','30','600','4','13.6','4400','jme_CIODLoadingChart'),
(409,180,'Yes','No','12','20','8','160','6','8.2','1960','jme_CIODLoadingChart'),
(410,181,'Yes','No','16','20','6','120','2','12.0','1000','jme_CIODLoadingChart'),
(411,182,'Yes','No','16','20','9','180','2','18.0','1000','jme_CIODLoadingChart'),
(412,201,'Yes','No','10','22','15','330','6','9.3','3564','jme_22FTIrrigationPIPLoadingChart'),
(413,204,'Yes','No','18','22','6','132','2','12.0','1100','jme_22FTIrrigationPIPLoadingChart'),
(414,205,'Yes','No','18','22','9','198','2','18.0','1100','jme_22FTIrrigationPIPLoadingChart'),
(415,207,'Yes','No','24','22','4','88','4','16.7','528','jme_22FTIrrigationPIPLoadingChart'),
(416,212,'Yes','No','10','20','15','300','6','9.3','3240','jme_20FTIrrigationLoadingChart'),
(417,215,'Yes','No','18','20','6','120','2','12.0','1000','jme_20FTIrrigationLoadingChart'),
(418,216,'Yes','No','18','20','9','180','2','18.0','1000','jme_20FTIrrigationLoadingChart'),
(419,218,'Yes','No','24','20','4','80','4','16.7','480','jme_20FTIrrigationLoadingChart'),
(420,223,'Yes','No','12','20','11','220','6','9.6','2280','jme_20FTIrrigationLoadingChart'),
(421,224,'Yes','No','15','20','8','160','8','10.5','1520','jme_20FTIrrigationLoadingChart'),
(422,225,'Yes','No','18','20','3','60','2','6.0','1000','jme_20FTIrrigationLoadingChart'),
(423,226,'Yes','No','18','20','6','120','4','12.0','1000','jme_20FTIrrigationLoadingChart'),
(424,227,'Yes','No','20','20','4','80','8','10.0','800','jme_20FTIrrigationLoadingChart'),
(425,289,'Yes','No','12','20','8','160','6','9.5','1680','jme_SolvetWeldLoadingChart_0'),
(426,290,'Yes','No','12 (West)*','20','8','160','8','7.1','2240','jme_SolvetWeldLoadingChart_0'),
(427,291,'Yes','No','14','20','12','240','4','14.3','1680','jme_SolvetWeldLoadingChart_0'),
(428,292,'Yes','No','16','20','9','180','4','15.0','1200','jme_SolvetWeldLoadingChart_0');

/*Table structure for table `product_type` */

DROP TABLE IF EXISTS `product_type`;

CREATE TABLE `product_type` (
  `product_type_id` int NOT NULL AUTO_INCREMENT,
  `active_flag` enum('Yes','No') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Yes',
  `deleted_flag` enum('No','Yes') NOT NULL DEFAULT 'No',
  `product_type` varchar(100) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_last_updated` timestamp NULL DEFAULT NULL,
  `date_deleted` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`product_type_id`),
  UNIQUE KEY `product_type` (`product_type`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `product_type` */

insert  into `product_type`(`product_type_id`,`active_flag`,`deleted_flag`,`product_type`,`date_created`,`date_last_updated`,`date_deleted`) values 
(1,'No','No','AWWA C905 PVC','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(2,'Yes','No','AWWA C900 PVC','2024-06-12 12:30:00','2024-06-12 16:16:39',NULL),
(3,'Yes','No','GRAVITY SEWER','2024-06-12 12:30:00','2024-06-12 16:16:47',NULL),
(4,'No','No','ULTRA-BLUE RT IPS PVCO','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(5,'No','No','SE/RT IPS 63 PSI 20','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(6,'No','No','RT IPS','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(7,'No','No','ULTRA BLUE AWWA C909 PVCO','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(8,'No','No','YELLOW GAS SLEEVE SCH40','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(9,'No','No','YELLOW GAS SLEEVE CL160/CL200','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(10,'No','No','YELLOW GAS SLEEVE CL160','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(11,'No','No','EB/DB DUCT','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(12,'No','No','CSA DB2 10\' LENGTH','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(13,'No','No','CSA DB2 20\' LENGTH','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(14,'No','No','TYPE C DUCT','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(15,'No','No','DROP PIPE SCH80 PHA* 20’ LENGTH','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(16,'No','No','DROP PIPE SCH80 PSU* 20’ LENGTH','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(17,'No','No','DEEP DROP PIPE SCH120 SCH120 20’ LENGTH','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(18,'No','No','PVC WELL CASING (INCLUDES EAGLE LOC) 20’ LENGTH','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(19,'No','No','ABS ACH40/DWV','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(20,'No','No','ABS SCH40/DWV','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(21,'No','No','PIP IRRIGATION','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(22,'No','No','LOW HEAD (100-FT HD) PIP/IP','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(23,'No','No','SCH40/SCH80 CONDUIT UL 651 NEMA TC-2','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(24,'No','No','SE IPS SCH40/DWV SOLID WALL PVC PLAIN OR BELL END','2024-06-12 12:30:00','2024-06-12 16:16:14',NULL),
(25,'Yes','No','SE IPS SCH40/DWV SOLID WALL PVC PLAIN OR BELLED END','2024-06-12 12:30:00','2024-06-12 16:16:53',NULL);

/*Table structure for table `sku` */

DROP TABLE IF EXISTS `sku`;

CREATE TABLE `sku` (
  `SKU_Id` int NOT NULL AUTO_INCREMENT,
  `product_type_id` int DEFAULT NULL,
  `active_flag` enum('No','Yes') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'No',
  `deleted_flag` enum('No','Yes') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'No',
  `size` varchar(255) DEFAULT NULL,
  `LENGTH` varchar(255) DEFAULT NULL,
  `pcs_lift` varchar(255) DEFAULT NULL,
  `ft_lift` varchar(255) DEFAULT NULL,
  `lifts_load` varchar(255) DEFAULT NULL,
  `load_percentage` varchar(255) DEFAULT NULL,
  `ft_load` varchar(255) DEFAULT NULL,
  `popularity_score` int NOT NULL DEFAULT '1000',
  `SOURCE` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`SKU_Id`),
  KEY `product_type_id` (`product_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=294 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `sku` */

insert  into `sku`(`SKU_Id`,`product_type_id`,`active_flag`,`deleted_flag`,`size`,`LENGTH`,`pcs_lift`,`ft_lift`,`lifts_load`,`load_percentage`,`ft_load`,`popularity_score`,`SOURCE`) values 
(1,1,'No','No','14','20','9','180','8','12.5%','1440',1000,'jme_CIODLoadingChart'),
(2,2,'No','No','12 DR 14','20','6 / 8','120 / 160','6 / 6','7.1 / 9.5%','1680',1000,'jme_CIODLoadingChart'),
(3,2,'No','No','12 DR 18, 25','20','6 / 8','120 / 160','4 / 4','6.1 / 8.2%','1960',1000,'jme_CIODLoadingChart'),
(4,2,'No','No','10','20','16','320','8','12.5%','2560',1000,'jme_CIODLoadingChart'),
(5,2,'No','No','8 DR 14','20','15','300','12','8.3%','3600',1000,'jme_CIODLoadingChart'),
(6,2,'No','No','8 DR 18, 25','20','15 / 20','300 / 400','8 / 4','7.5 / 10.0%','4000',1000,'jme_CIODLoadingChart'),
(7,2,'No','No','6','20','28','560','12','8.3%','6720',1000,'jme_CIODLoadingChart'),
(8,2,'No','No','4','20','60','1200','12','8.3%','14400',1000,'jme_CIODLoadingChart'),
(9,3,'No','No','48','14','2','28','3','33.3%','84',1000,'jme_GravitySewerLoadingChart'),
(10,3,'No','No','42','14','2','28','6','16.7%','168',1000,'jme_GravitySewerLoadingChart'),
(11,3,'No','No','36','14','2','28','6','16.7%','168',1000,'jme_GravitySewerLoadingChart'),
(12,3,'No','No','30 (West)*','14','3','42','9','11.1%','378',1000,'jme_GravitySewerLoadingChart'),
(13,3,'No','No','30','14','3','42','6','16.7%','252',1000,'jme_GravitySewerLoadingChart'),
(14,3,'No','No','27','14','3','42','9','11.1%','378',1000,'jme_GravitySewerLoadingChart'),
(15,3,'No','No','24 (West)*','14','4','56','12','8.3%','672',1000,'jme_GravitySewerLoadingChart'),
(16,3,'No','No','24','14','2 / 4','28 / 56','6 / 6','5.6 / 11.1%','504',1000,'jme_GravitySewerLoadingChart'),
(17,3,'No','No','21','14','4','56','12','8.3%','672',1000,'jme_GravitySewerLoadingChart'),
(18,3,'No','No','18','14','4 / 6','56 / 84','3 / 3','5.3 / 8.0%','1050',1000,'jme_GravitySewerLoadingChart'),
(19,3,'No','No','15','14','9','126','12','8.3%','1512',1000,'jme_GravitySewerLoadingChart'),
(20,3,'No','No','12 (West)*','14','16','224','12','8.3%','2688',1000,'jme_GravitySewerLoadingChart'),
(21,3,'Yes','No','12','14','12 / 16','168 / 224','6 / 6','7.1 / 9.5%','2352',2,'jme_GravitySewerLoadingChart'),
(22,3,'Yes','No','10','14','12 / 15','168 / 210','9 / 9','4.9 / 6.2%','3402',7,'jme_GravitySewerLoadingChart'),
(23,3,'No','No','8 (West)*','14','36','504','12','8.3%','6048',1000,'jme_GravitySewerLoadingChart'),
(24,3,'Yes','No','8','14','30 / 36','420 / 504','6 / 6','7.5 / 9.1%','5544',2,'jme_GravitySewerLoadingChart'),
(25,3,'Yes','No','6','14','40','560','18','5.6%','10080',2,'jme_GravitySewerLoadingChart'),
(26,3,'Yes','No','4','14','84','1176','18','5.6%','21168',2,'jme_GravitySewerLoadingChart'),
(27,3,'No','No','48','20','2','40','2','50.0%','80',1000,'jme_GravitySewerLoadingChart'),
(28,3,'No','No','36','20','2','40','4','25.0%','160',1000,'jme_GravitySewerLoadingChart'),
(29,3,'No','No','42','20','2','40','4','25.0%','160',1000,'jme_GravitySewerLoadingChart'),
(30,3,'No','No','30 (West)*','20','3','60','6','16.7%','360',1000,'jme_GravitySewerLoadingChart'),
(31,3,'No','No','30','20','3','60','4','25.0%','240',1000,'jme_GravitySewerLoadingChart'),
(32,3,'No','No','27','20','3','60','6','16.7%','360',1000,'jme_GravitySewerLoadingChart'),
(33,3,'No','No','24 (West)*','20','4','80','8','12.5%','640',1000,'jme_GravitySewerLoadingChart'),
(34,3,'No','No','24','20','2 / 4','40 / 80','4 / 4','8.3 / 16.7%','480',1000,'jme_GravitySewerLoadingChart'),
(35,3,'No','No','21','20','4','80','8','12.5%','640',1000,'jme_GravitySewerLoadingChart'),
(36,3,'No','No','18','20','4 / 6','80 / 120','2 / 2','8.0 / 12.0%','1000',1000,'jme_GravitySewerLoadingChart'),
(37,3,'No','No','15','20','9','180','8','12.5%','1440',1000,'jme_GravitySewerLoadingChart'),
(38,3,'No','No','12 (West)*','20','16','320','8','12.5%','2560',1000,'jme_GravitySewerLoadingChart'),
(39,3,'Yes','No','12','20','12 / 16','240 / 320','4 / 4','10.7 / 14.3%','2240',1,'jme_GravitySewerLoadingChart'),
(40,3,'Yes','No','10','20','12 / 15','240 / 300','6 / 6','7.4 / 9.3%','3240',4,'jme_GravitySewerLoadingChart'),
(41,3,'No','No','8 (West)*','20','36','720','8','12.5%','5760',1000,'jme_GravitySewerLoadingChart'),
(42,3,'Yes','No','8','20','30 / 36','600 / 720','4 / 4','11.4 / 13.6%','5280',4,'jme_GravitySewerLoadingChart'),
(43,3,'No','No','6','20','40','800','12','8.3%','9600',1000,'jme_GravitySewerLoadingChart'),
(44,3,'Yes','No','4','20','84','1680','12','8.3%','20160',7,'jme_GravitySewerLoadingChart'),
(45,4,'No','No','12','20','9 / 12','180 / 240','2 / 2','9.2 / 12.2%','1960',1000,'jme_IPSPressureLoadingChart'),
(46,4,'No','No','12','20','6 / 8','120 / 160','4 / 4','6.1 / 8.2%','1960',1000,'jme_IPSPressureLoadingChart'),
(47,4,'No','No','10','20','8','160','16','6.3%','2560',1000,'jme_IPSPressureLoadingChart'),
(48,4,'No','No','8','20','25 / 30','500 / 600','4 / 4','11.4 / 13.6%','4400',1000,'jme_IPSPressureLoadingChart'),
(49,4,'No','No','6','20','28 / 35','560 / 700','4 / 8','7.1 / 8.9%','7840',1000,'jme_IPSPressureLoadingChart'),
(50,5,'No','No','12','20','6 / 8','120 / 160','6 / 6','7.1 / 9.5%','1680',1000,'jme_IPSPressureLoadingChart'),
(51,5,'No','No','10','20','12','240','12','8.3%','2880',1000,'jme_IPSPressureLoadingChart'),
(52,5,'No','No','8','20','15','300','12','8.3%','3600',1000,'jme_IPSPressureLoadingChart'),
(53,6,'No','No','4','40','38 / 57','1520 / 2280','2 / 6','9.1 / 13.6%','16720',1000,'jme_IPSPressureLoadingChart'),
(54,6,'No','No','1 1/2','20','270','5400','16','6.3%','86400',1000,'jme_IPSPressureLoadingChart'),
(55,6,'No','No','2','20','185','3700','16','6.3%','59200',1000,'jme_IPSPressureLoadingChart'),
(56,6,'No','No','2 1/2','20','73','1460','28','3.6%','40880',1000,'jme_IPSPressureLoadingChart'),
(57,6,'No','No','6','20','28 / 35','560 / 700','4 / 8','7.1 / 8.9%','7840',1000,'jme_IPSPressureLoadingChart'),
(58,6,'No','No','5 (West)*','20','38','760','16','6.3%','12160',1000,'jme_IPSPressureLoadingChart'),
(59,6,'No','No','6','40','28 / 35','1120 / 1400','2 / 4','14.3 / 17.9%','7840',1000,'jme_IPSPressureLoadingChart'),
(60,6,'No','No','2','40','185','7400','8','12.5%','59200',1000,'jme_IPSPressureLoadingChart'),
(61,6,'No','No','12 / 16','20','12 / 16','240 / 320','2 / 2','12.2 / 16.3%','1960',1000,'jme_IPSPressureLoadingChart'),
(62,6,'No','No','5','20','38','760','12','8.3%','9120',1000,'jme_IPSPressureLoadingChart'),
(63,6,'No','No','4 (West)*','20','48','960','20','5.0%','19200',1000,'jme_IPSPressureLoadingChart'),
(64,6,'No','No','4','20','76','1520','12','8.3%','18240',1000,'jme_IPSPressureLoadingChart'),
(65,6,'No','No','3 (West)*','20','75','1500','20','5.0%','30000',1000,'jme_IPSPressureLoadingChart'),
(66,6,'No','No','3','20','75','1500','16','6.3%','24000',1000,'jme_IPSPressureLoadingChart'),
(67,6,'No','No','12','20','9 / 12','180 / 240','2 / 2','9.1 / 12.2%','1960',1000,'jme_IPSPressureLoadingChart'),
(68,6,'No','No','10','20','16 / 20','320 / 400','4 / 4','11.1 / 13.9%','2880',1000,'jme_IPSPressureLoadingChart'),
(69,6,'No','No','8 (West)*','20','20 / 24','400 / 480','6 / 6','7.6 / 9.1%','5280',1000,'jme_IPSPressureLoadingChart'),
(70,6,'No','No','8','20','25 / 30','500 / 600','4 / 4','11.4 / 13.6%','4400',1000,'jme_IPSPressureLoadingChart'),
(71,6,'No','No','6 (West)*','20','26','520','16','6.3%','8320',1000,'jme_IPSPressureLoadingChart'),
(72,6,'No','No','8','40','10 / 15','400 / 600','4 / 4','10.0 / 15.0%','4000',1000,'jme_IPSPressureLoadingChart'),
(73,6,'No','No','3','40','100','4000','6','16.7%','24000',1000,'jme_IPSPressureLoadingChart'),
(74,6,'No','No','12','20','12 / 16','240 / 320','2 / 2','12.2 / 16.3%','1960',1000,'jme_IPSPressureLoadingChart'),
(75,2,'Yes','No','4','20','60','1200','12','8.3%','14400',8,'LoadingChart C900_2-3-2017'),
(76,2,'Yes','No','6','20','28','560','12','8.3%','6720',9,'LoadingChart C900_2-3-2017'),
(77,2,'Yes','No','8 DR 18, 25','20','15 / 20','300 / 400','8 / 4','7.5 / 10.0%','4000',5,'LoadingChart C900_2-3-2017'),
(78,2,'Yes','No','8 DR 14','20','15','300','12','8.3%','3600',8,'LoadingChart C900_2-3-2017'),
(79,2,'Yes','No','10','20','16','320','8','12.5%','2560',8,'LoadingChart C900_2-3-2017'),
(80,2,'Yes','No','12 DR 18, 25','20','6 / 8','120 / 160','4 / 4','6.1 / 8.2','1960',10,'LoadingChart C900_2-3-2017'),
(81,2,'Yes','No','12 DR 18, 25','20','9 / 12','180 / 240','2 / 2','9.2 / 12.2%','1960',6,'LoadingChart C900_2-3-2017'),
(82,2,'Yes','No','12 DR 14','20','6 / 8','120 / 160','6 / 6','7.1 / 9.5%','1680',6,'LoadingChart C900_2-3-2017'),
(83,2,'Yes','No','14','20','9','180','8','12.5%','1440',6,'LoadingChart C900_2-3-2017'),
(84,2,'No','No','16','20','4 / 6','80 / 120','2 / 2','8.0 / 12.0','1000',1000,'LoadingChart C900_2-3-2017'),
(85,2,'No','No','16','20','6 / 9','120 / 180','2 / 2','12.0 / 18.0%','1000',1000,'LoadingChart C900_2-3-2017'),
(86,2,'No','No','18','20','4 / 6','80 / 120','4 / 4','10.0 / 15.0%','800',1000,'LoadingChart C900_2-3-2017'),
(87,2,'No','No','20','20','4','80','8','12.5%','640',1000,'LoadingChart C900_2-3-2017'),
(88,2,'No','No','24','20','3','60','6','16.7%','360',1000,'LoadingChart C900_2-3-2017'),
(89,2,'No','No','30','20','3','60','4','25.0%','240',1000,'LoadingChart C900_2-3-2017'),
(90,2,'No','No','30 (West)*','20','3','60','6','16.7%','360',1000,'LoadingChart C900_2-3-2017'),
(91,2,'No','No','36','20','2','40','4','25.0%','160',1000,'LoadingChart C900_2-3-2017'),
(92,2,'No','No','42','20','2','40','4','25.0%','160',1000,'LoadingChart C900_2-3-2017'),
(93,2,'No','No','48','20','2','40','2','50.0%','80',1000,'LoadingChart C900_2-3-2017'),
(94,7,'No','No','6','20','28 / 35','560 / 700','4 / 8','7.1 / 8.9%','7840',1000,'LoadingChart C900_2-3-2017'),
(95,7,'No','No','8 CL150','20','25 / 30','500 / 600','4 / 4','11.4 / 13.6%','4400',1000,'LoadingChart C900_2-3-2017'),
(96,7,'No','No','10','20','8','160','16','6.3%','2560',1000,'LoadingChart C900_2-3-2017'),
(97,7,'No','No','12','20','6 / 8','120 / 160','6 / 6','6.1 / 8.2','1960',1000,'LoadingChart C900_2-3-2017'),
(98,7,'No','No','16','20','4 / 6','80 / 120','2 / 2','8.0 / 12.0','1000',1000,'LoadingChart C900_2-3-2017'),
(99,7,'No','No','16','20','6 / 9','120 / 180','2 / 2','12.0 / 18.0%','1000',1000,'LoadingChart C900_2-3-2017'),
(100,8,'No','No','1','20','275','5500','32','3.13%','176000',1000,'jme_YellowGasSleeveLoadingChart'),
(101,8,'No','No','1 1/2','20','168','3360','32','3.13%','107520',1000,'jme_YellowGasSleeveLoadingChart'),
(102,8,'No','No','2','20','105','2100','28','3.57%','58800',1000,'jme_YellowGasSleeveLoadingChart'),
(103,8,'No','No','2 (PTA)*','20','140','2800','20','5.00%','56000',1000,'jme_YellowGasSleeveLoadingChart'),
(104,8,'No','No','3','20','60','1200','24','4.17%','28800',1000,'jme_YellowGasSleeveLoadingChart'),
(105,8,'No','No','3 (PTA)*','20','88','1760','16','6.25%','28160',1000,'jme_YellowGasSleeveLoadingChart'),
(106,8,'No','No','4','20','57','1140','16','6.25%','18240',1000,'jme_YellowGasSleeveLoadingChart'),
(107,8,'No','No','6','20','26','520','16','6.25%','8320',1000,'jme_YellowGasSleeveLoadingChart'),
(108,8,'No','No','8','20','15','300','16','6.25%','4800',1000,'jme_YellowGasSleeveLoadingChart'),
(109,8,'No','No','10','20','12','240','12','8.33%','2880',1000,'jme_YellowGasSleeveLoadingChart'),
(110,8,'No','No','12','20','6 / 8','120 / 160','6 / 6','7.1 / 9.5%','1680',1000,'jme_YellowGasSleeveLoadingChart'),
(111,9,'No','No','1','20','275','5500','32','3.13%','176000',1000,'jme_YellowGasSleeveLoadingChart'),
(112,9,'No','No','1 1/4','20','196','3920','32','3.13%','125440',1000,'jme_YellowGasSleeveLoadingChart'),
(113,9,'No','No','1 1/2','20','151','3020','32','3.13%','96640',1000,'jme_YellowGasSleeveLoadingChart'),
(114,9,'No','No','2','20','105','2100','28','3.57%','58800',1000,'jme_YellowGasSleeveLoadingChart'),
(115,9,'No','No','3','20','60','1200','24','4.17%','28800',1000,'jme_YellowGasSleeveLoadingChart'),
(116,9,'No','No','4','20','57','1140','16','6.25%','18240',1000,'jme_YellowGasSleeveLoadingChart'),
(117,9,'No','No','6','20','26','520','16','6.25%','8320',1000,'jme_YellowGasSleeveLoadingChart'),
(118,9,'No','No','8','20','15','300','16','6.25%','4800',1000,'jme_YellowGasSleeveLoadingChart'),
(119,9,'No','No','10','20','12','240','12','8.33%','2880',1000,'jme_YellowGasSleeveLoadingChart'),
(120,9,'No','No','12','20','6 / 8','120 / 160','6 / 6','7.1 / 9.5%','1680',1000,'jme_YellowGasSleeveLoadingChart'),
(121,10,'No','No','10','10','48','480','32','3.13%','15360',1000,'jme_YellowGasSleeveLoadingChart'),
(122,10,'No','No','6','10','26','260','32','3.13%','8320',1000,'jme_YellowGasSleeveLoadingChart'),
(123,11,'No','No','1','20','400','8000','20','5.00%','160000',1000,'jme_UtilityDuctLoadingChart'),
(124,11,'No','No','1 1/2','20','225','4500','20','5.00%','90000',1000,'jme_UtilityDuctLoadingChart'),
(125,11,'No','No','2','20','140','2800','20','5.00%','56000',1000,'jme_UtilityDuctLoadingChart'),
(126,11,'No','No','2 1/2','20','131','2620','16','6.25%','41920',1000,'jme_UtilityDuctLoadingChart'),
(127,11,'No','No','3','20','100','2000','12','8.33%','24000',1000,'jme_UtilityDuctLoadingChart'),
(128,11,'No','No','3 (West)*','20','100','2000','16','6.25%','32000',1000,'jme_UtilityDuctLoadingChart'),
(129,11,'No','No','3 1/2','20','63','1260','16','6.25%','20160',1000,'jme_UtilityDuctLoadingChart'),
(130,11,'No','No','4','20','57','1140','12','8.33%','13680',1000,'jme_UtilityDuctLoadingChart'),
(131,11,'No','No','4 (West)*','20','57','1140','16','6.25%','18240',1000,'jme_UtilityDuctLoadingChart'),
(132,11,'No','No','5','20','38','760','12','8.33%','9120',1000,'jme_UtilityDuctLoadingChart'),
(133,11,'No','No','5 (West)*','20','38','760','16','6.25%','12160',1000,'jme_UtilityDuctLoadingChart'),
(134,11,'No','No','6','20','26','520','12','8.33%','6240',1000,'jme_UtilityDuctLoadingChart'),
(135,11,'No','No','6 (West)*','20','26','520','16','6.25%','8320',1000,'jme_UtilityDuctLoadingChart'),
(136,12,'No','No','2','10','234','2340','32','3.13%','74880',1000,'jme_UtilityDuctLoadingChart'),
(137,12,'No','No','3','10','100','1000','32','3.13%','32000',1000,'jme_UtilityDuctLoadingChart'),
(138,12,'No','No','4','10','63','630','32','3.13%','20160',1000,'jme_UtilityDuctLoadingChart'),
(139,13,'No','No','2','20','234','4680','16','6.25%','74880',1000,'jme_UtilityDuctLoadingChart'),
(140,13,'No','No','3','20','100','2000','16','6.25%','32000',1000,'jme_UtilityDuctLoadingChart'),
(141,13,'No','No','4','20','63','1260','16','6.25%','20160',1000,'jme_UtilityDuctLoadingChart'),
(142,14,'No','No','4','20','63','1260','16','6.25%','20160',1000,'jme_UtilityDuctLoadingChart'),
(143,15,'No','No','1','20','250','5000','36','2.78%','180000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(144,15,'No','No','1 1/4','20','200','4000','28','3.57%','112000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(145,15,'No','No','1 1/2','20','150','3000','28','3.57%','84000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(146,15,'No','No','2','20','100','2000','28','3.57%','56000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(147,16,'No','No','1','20','120','2400','40','2.50%','96000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(148,16,'No','No','1 1/4','20','100','2000','40','2.50%','80000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(149,16,'No','No','1 1/2','20','90','1800','40','2.50%','72000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(150,16,'No','No','2','20','53','1060','40','2.50%','42400',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(151,17,'No','No','1','20','120','2400','40','2.50%','96000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(152,17,'No','No','1 1/4','20','100','2000','40','2.50%','80000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(153,17,'No','No','1 1/2','20','90','1800','40','2.50%','72000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(154,17,'No','No','2','20','53','1060','40','2.50%','42400',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(155,18,'No','No','2','20','105','2100','28','3.6%','58800',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(156,18,'No','No','4','20','57','1140','12','8.3%','13680',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(157,18,'No','No','4 (West)*','20','29','580','28','3.6%','16240',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(158,18,'No','No','4 1/2','20','26','520','24','4.2%','12480',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(159,18,'No','No','5','20','23','460','20','5.0%','9200',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(160,18,'No','No','5 (West)*','20','23','460','24','4.2%','11040',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(161,18,'No','No','6','20','20','400','16','6.3%','6400',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(162,18,'No','No','6 (West)*','20','20','400','20','5.0%','8000',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(163,18,'No','No','8','20','15','300','12','8.3%','3600',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(164,18,'No','No','8 (West)*','20','20','400','12','8.3%','4800',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(165,18,'No','No','10','20','12','240','12','8.3%','2880',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(166,18,'No','No','12 (West)*','20','6 / 8','120 / 160','8 / 8','5.4 / 7.1%','2240',1000,'jme_ThreadedDropPipe-WellCasingLaodingChart'),
(167,1,'No','No','16','20','4 / 6','80 / 120','2 / 2','8.0 / 12.0%','1000',1000,'jme_CIODLoadingChart'),
(168,1,'No','No','16','20','6 / 9','120 / 180','2 / 2','12.0 / 18.0%','1000',1000,'jme_CIODLoadingChart'),
(169,1,'No','No','18','20','4 / 6','80 / 120','4 / 4','10.0 / 15.0%','800',1000,'jme_CIODLoadingChart'),
(170,1,'No','No','20','20','4','80','8','12.5%','640',1000,'jme_CIODLoadingChart'),
(171,1,'No','No','24','20','3','60','6','16.7%','360',1000,'jme_CIODLoadingChart'),
(172,1,'No','No','30','20','3','60','4','25.0%','240',1000,'jme_CIODLoadingChart'),
(173,1,'No','No','30 (West)*','20','3','60','6','16.7%','360',1000,'jme_CIODLoadingChart'),
(174,1,'No','No','36','20','2','40','4','25.0%','160',1000,'jme_CIODLoadingChart'),
(175,1,'No','No','42','20','2','40','4','25.0%','160',1000,'jme_CIODLoadingChart'),
(176,1,'No','No','48','20','2','40','2','50.0%','80',1000,'jme_CIODLoadingChart'),
(177,7,'No','No','6','20','28 / 35','560 / 700','4 / 8','7.1 / 8.9%','7840',1000,'jme_CIODLoadingChart'),
(178,7,'No','No','8 CL150','20','25 / 30','500 / 600','4 / 4','11.4 / 13.6%','4400',1000,'jme_CIODLoadingChart'),
(179,7,'No','No','10','20','8','160','16','6.3%','2560',1000,'jme_CIODLoadingChart'),
(180,7,'No','No','12','20','6 / 8','120 / 160','6 / 6','6.1 / 8.2%','1960',1000,'jme_CIODLoadingChart'),
(181,7,'No','No','16','20','4 / 6','80 / 120','2 / 2','8.0 / 12.0%','1000',1000,'jme_CIODLoadingChart'),
(182,7,'No','No','16','20','6 / 9','120 / 180','2 / 2','12.0 / 18.0%','1000',1000,'jme_CIODLoadingChart'),
(183,19,'No','No','1 1/2','10','180','1800','48','2.1%','86400',1000,'jme_ABSLoadingChart'),
(184,19,'No','No','2','10','105','1050','48','2.1%','50400',1000,'jme_ABSLoadingChart'),
(185,19,'No','No','3','10','75','750','32','3.1%','24000',1000,'jme_ABSLoadingChart'),
(186,19,'No','No','4','10','57','570','32','3.1%','18240',1000,'jme_ABSLoadingChart'),
(187,19,'No','No','4 (West)*','10','57','570','24','4.2%','13680',1000,'jme_ABSLoadingChart'),
(188,19,'No','No','6','10','26','260','24','4.2%','6240',1000,'jme_ABSLoadingChart'),
(189,19,'No','No','6 (West)*','10','26','260','32','3.1%','8320',1000,'jme_ABSLoadingChart'),
(190,20,'No','No','1 1/2','20','180','3600','24','4.2%','86400',1000,'jme_ABSLoadingChart'),
(191,20,'No','No','2','20','105','2100','24','4.2%','50400',1000,'jme_ABSLoadingChart'),
(192,20,'No','No','3','20','75','1500','16','6.3%','24000',1000,'jme_ABSLoadingChart'),
(193,20,'No','No','4','20','57','1140','12','8.3%','13680',1000,'jme_ABSLoadingChart'),
(194,20,'No','No','4 (West)*','20','57','1140','16','6.3%','18240',1000,'jme_ABSLoadingChart'),
(195,20,'No','No','5','20','38','760','16','6.3%','12160',1000,'jme_ABSLoadingChart'),
(196,20,'No','No','5 (West)*','20','38','760','12','8.3%','9120',1000,'jme_ABSLoadingChart'),
(197,20,'No','No','6','20','26','520','12','8.3%','6240',1000,'jme_ABSLoadingChart'),
(198,20,'No','No','6 (West)*','20','26','520','16','6.3%','8320',1000,'jme_ABSLoadingChart'),
(199,21,'No','No','6','22','40','880','12','8.3%','10560',1000,'jme_22FTIrrigationPIPLoadingChart'),
(200,21,'No','No','8','22','36','792','8','12.5%','6336',1000,'jme_22FTIrrigationPIPLoadingChart'),
(201,21,'No','No','10','22','12 / 15','264 / 330','6 / 6','7.4 / 9.3%','3564',1000,'jme_22FTIrrigationPIPLoadingChart'),
(202,21,'No','No','12','22','16','352','8','12.5%','2816',1000,'jme_22FTIrrigationPIPLoadingChart'),
(203,21,'No','No','15','22','9','198','8','12.5%','1584',1000,'jme_22FTIrrigationPIPLoadingChart'),
(204,21,'No','No','18','22','4 / 6','88 / 132','2 / 2','8.0 / 12.0%','1100',1000,'jme_22FTIrrigationPIPLoadingChart'),
(205,21,'No','No','18','22','6 / 9','132 / 198','2 / 2','12.0 / 18.0%','1100',1000,'jme_22FTIrrigationPIPLoadingChart'),
(206,21,'No','No','21','22','4','88','8','12.5%','704',1000,'jme_22FTIrrigationPIPLoadingChart'),
(207,21,'No','No','24','22','2 / 4','44 / 88','4 / 4','8.3 / 16.7%','528',1000,'jme_22FTIrrigationPIPLoadingChart'),
(208,21,'No','No','24','22','4','88','8','12.5%','704',1000,'jme_22FTIrrigationPIPLoadingChart'),
(209,21,'No','No','27','22','3','66','6','16.7%','396',1000,'jme_22FTIrrigationPIPLoadingChart'),
(210,21,'No','No','6','20','40','800','12','8.3%','9600',1000,'jme_20FTIrrigationLoadingChart'),
(211,21,'No','No','8','20','36','720','8','12.5%','5760',1000,'jme_20FTIrrigationLoadingChart'),
(212,21,'No','No','10','20','12 / 15','240 / 300','6 / 6','7.4 / 9.3%','3240',1000,'jme_20FTIrrigationLoadingChart'),
(213,21,'No','No','12','20','16','320','8','12.5%','2560',1000,'jme_20FTIrrigationLoadingChart'),
(214,21,'No','No','15','20','9','180','8','12.5%','1440',1000,'jme_20FTIrrigationLoadingChart'),
(215,21,'No','No','18','20','4 / 6','80 / 120','2 / 2','8.0 / 12.0%','1000',1000,'jme_20FTIrrigationLoadingChart'),
(216,21,'No','No','18','20','6 / 9','120 / 180','2 / 2','12.0 / 18.0%','1000',1000,'jme_20FTIrrigationLoadingChart'),
(217,21,'No','No','21','20','4','80','8','12.5%','640',1000,'jme_20FTIrrigationLoadingChart'),
(218,21,'No','No','24','20','2 / 4','40 / 80','4 / 4','8.3 / 16.7%','480',1000,'jme_20FTIrrigationLoadingChart'),
(219,21,'No','No','24 (West)*','20','4','80','8','12.5%','640',1000,'jme_20FTIrrigationLoadingChart'),
(220,21,'No','No','27','20','3','60','6','16.7%','360',1000,'jme_20FTIrrigationLoadingChart'),
(221,22,'No','No','8','20','14','280','16','6.3%','4480',1000,'jme_20FTIrrigationLoadingChart'),
(222,22,'No','No','10','20','11','220','12','8.3%','2640',1000,'jme_20FTIrrigationLoadingChart'),
(223,22,'No','No','12','20','8 / 11','160 / 220','6 / 6','7.0 / 9.6%','2280',1000,'jme_20FTIrrigationLoadingChart'),
(224,22,'No','No','15','20','3 / 8','60 / 160','4 / 8','3.9 / 10.5%','1520',1000,'jme_20FTIrrigationLoadingChart'),
(225,22,'No','No','18','20','2 / 3','40 / 60','2 / 2','4.0 / 6.0%','1000',1000,'jme_20FTIrrigationLoadingChart'),
(226,22,'No','No','18','20','4 / 6','80 / 120','4 / 4','8.0 / 12.0%','1000',1000,'jme_20FTIrrigationLoadingChart'),
(227,22,'No','No','20','20','2 / 4','40 / 80','4 / 8','5.0 / 10.0%','800',1000,'jme_20FTIrrigationLoadingChart'),
(228,23,'No','No','1/2','10','300','3000','80','1.25%','240000',1000,'ElectricalConduitLoadingChart_0'),
(229,23,'No','No','3/4','10','220','2200','80','1.25%','176000',1000,'ElectricalConduitLoadingChart_0'),
(230,23,'No','No','1','10','180','1800','80','1.25%','144000',1000,'ElectricalConduitLoadingChart_0'),
(231,23,'No','No','1 1/4','10','90','900','80','1.25%','72000',1000,'ElectricalConduitLoadingChart_0'),
(232,23,'No','No','1 1/2','10','90','900','80','1.25%','72000',1000,'ElectricalConduitLoadingChart_0'),
(233,23,'No','No','2','10','70','700','72','1.39%','50400',1000,'ElectricalConduitLoadingChart_0'),
(234,23,'No','No','2 1/2','10','50','500','56','1.79%','28000',1000,'ElectricalConduitLoadingChart_0'),
(235,23,'No','No','2 1/2 (West)*','10','50','500','64','1.56%','32000',1000,'ElectricalConduitLoadingChart_0'),
(236,23,'No','No','3','10','50','500','48','2.08%','24000',1000,'ElectricalConduitLoadingChart_0'),
(237,23,'No','No','1/2','10','600','6000','72','1.39%','432000',1000,'ElectricalConduitLoadingChart_0'),
(238,23,'No','No','3/4','10','440','4400','56','1.79%','246400',1000,'ElectricalConduitLoadingChart_0'),
(239,23,'No','No','1','10','360','3600','48','2.08%','172800',1000,'ElectricalConduitLoadingChart_0'),
(240,23,'No','No','1 1/4','10','330','3300','40','2.50%','132000',1000,'ElectricalConduitLoadingChart_0'),
(241,23,'No','No','1 1/2','10','225','2250','40','2.50%','90000',1000,'ElectricalConduitLoadingChart_0'),
(242,23,'No','No','2','10','140','1400','40','2.50%','56000',1000,'ElectricalConduitLoadingChart_0'),
(243,23,'No','No','2 1/2','10','93','930','40','2.50%','37200',1000,'ElectricalConduitLoadingChart_0'),
(244,23,'No','No','3','10','88','880','32','3.13%','28160',1000,'ElectricalConduitLoadingChart_0'),
(245,23,'No','No','3 1/2','10','63','630','32','3.13%','20160',1000,'ElectricalConduitLoadingChart_0'),
(246,23,'No','No','4','10','57','570','24','4.17%','13680',1000,'ElectricalConduitLoadingChart_0'),
(247,23,'No','No','4 (West)*','10','57','570','32','3.13%','18240',1000,'ElectricalConduitLoadingChart_0'),
(248,23,'No','No','5','10','38','380','24','4.17%','9120',1000,'ElectricalConduitLoadingChart_0'),
(249,23,'No','No','6','10','26','260','24','4.17%','6240',1000,'ElectricalConduitLoadingChart_0'),
(250,23,'No','No','6 (West)*','10','26','260','32','3.13%','8320',1000,'ElectricalConduitLoadingChart_0'),
(251,24,'No','No','1/2','10','300','3000','104','0.96%','312000',1000,'jme_SolvetWeldLoadingChart_0'),
(252,24,'No','No','1/2 (West)*','10','300','3000','112','0.89%','336000',1000,'jme_SolvetWeldLoadingChart_0'),
(253,24,'No','No','3/4','10','220','2200','88','1.1%','193600',1000,'jme_SolvetWeldLoadingChart_0'),
(254,24,'No','No','3/4 (West)*','10','220','2200','96','1.0%','211200',1000,'jme_SolvetWeldLoadingChart_0'),
(255,24,'No','No','1','10','180','1800','80','1.3%','144000',1000,'jme_SolvetWeldLoadingChart_0'),
(256,24,'No','No','1 (West)*','10','180','1800','88','1.1%','158400',1000,'jme_SolvetWeldLoadingChart_0'),
(257,24,'No','No','1 1/4','10','90','900','88','1.1%','79200',1000,'jme_SolvetWeldLoadingChart_0'),
(258,24,'No','No','1 1/4 (West)*','10','90','900','96','1.0%','86400',1000,'jme_SolvetWeldLoadingChart_0'),
(259,24,'No','No','1 1/2','10','90','900','80','1.3%','72000',1000,'jme_SolvetWeldLoadingChart_0'),
(260,24,'No','No','2','10','105','1050','48','2.1%','50400',1000,'jme_SolvetWeldLoadingChart_0'),
(261,24,'No','No','2 1/2','10','73','730','48','2.1%','35040',1000,'jme_SolvetWeldLoadingChart_0'),
(262,24,'No','No','3','10','75','750','32','3.1%','24000',1000,'jme_SolvetWeldLoadingChart_0'),
(263,24,'No','No','3 (West)*','10','75','750','40','2.5%','30000',1000,'jme_SolvetWeldLoadingChart_0'),
(264,24,'No','No','4','10','57','570','24','4.2%','13680',1000,'jme_SolvetWeldLoadingChart_0'),
(265,24,'No','No','4 (West)*','10','57','570','32','3.1%','18240',1000,'jme_SolvetWeldLoadingChart_0'),
(266,24,'No','No','6','10','26','260','24','4.2%','6240',1000,'jme_SolvetWeldLoadingChart_0'),
(267,24,'No','No','6 (West)*','10','26','260','32','3.1%','8320',1000,'jme_SolvetWeldLoadingChart_0'),
(268,25,'Yes','No','1/2','20','360','7200','36','2.8%','259200',10,'jme_SolvetWeldLoadingChart_0'),
(269,25,'No','No','1/2 (West)*','20','360','7200','40','2.5%','288000',1000,'jme_SolvetWeldLoadingChart_0'),
(270,25,'Yes','No','3/4','20','400','8000','24','4.2%','192000',10,'jme_SolvetWeldLoadingChart_0'),
(271,25,'No','No','3/4 (West)*','20','400','8000','28','3.6%','224000',1000,'jme_SolvetWeldLoadingChart_0'),
(272,25,'Yes','No','1','20','280','5600','20','5.0%','112000',10,'jme_SolvetWeldLoadingChart_0'),
(273,25,'No','No','1 (West)*','20','280','5600','24','4.2%','134400',1000,'jme_SolvetWeldLoadingChart_0'),
(274,25,'Yes','No','1 1/4','20','220','4400','24','4.2%','105600',10,'jme_SolvetWeldLoadingChart_0'),
(275,25,'No','No','1 1/4 (West)*','20','220','4400','28','3.6%','123200',1000,'jme_SolvetWeldLoadingChart_0'),
(276,25,'Yes','No','1 1/2','20','180','3600','24','4.2%','86400',8,'jme_SolvetWeldLoadingChart_0'),
(277,25,'Yes','No','2','20','105','2100','24','4.2%','50400',11,'jme_SolvetWeldLoadingChart_0'),
(278,25,'Yes','No','2 1/2','20','73','1460','24','4.2%','35040',12,'jme_SolvetWeldLoadingChart_0'),
(279,25,'Yes','No','3','20','75','1500','16','6.3%','24000',12,'jme_SolvetWeldLoadingChart_0'),
(280,25,'Yes','No','4','20','57','1140','12','8.3%','13680',13,'jme_SolvetWeldLoadingChart_0'),
(281,25,'No','No','4 (West)*','20','57','1140','16','6.3%','18240',1000,'jme_SolvetWeldLoadingChart_0'),
(282,25,'No','No','5','20','38','760','12','8.3%','9120',1000,'jme_SolvetWeldLoadingChart_0'),
(283,25,'No','No','5 (West)*','20','38','760','16','6.3%','12160',1000,'jme_SolvetWeldLoadingChart_0'),
(284,25,'Yes','No','6','20','26','520','12','8.3%','6240',13,'jme_SolvetWeldLoadingChart_0'),
(285,25,'No','No','6 (West)*','20','26','520','16','6.3%','8320',1000,'jme_SolvetWeldLoadingChart_0'),
(286,25,'Yes','No','8','20','15','300','12','8.3%','3600',9,'jme_SolvetWeldLoadingChart_0'),
(287,25,'No','No','8 (West)*','20','20','400','12','8.3%','4800',1000,'jme_SolvetWeldLoadingChart_0'),
(288,25,'Yes','No','10','20','12','240','12','8.3%','2880',9,'jme_SolvetWeldLoadingChart_0'),
(289,25,'Yes','No','12','20','6 / 8','120 / 160','6 / 6','7.1 / 9.5%','1680',12,'jme_SolvetWeldLoadingChart_0'),
(290,25,'No','No','12 (West)*','20','6 / 8','120 / 160','8 / 8','5.4 / 7.1%','2240',1000,'jme_SolvetWeldLoadingChart_0'),
(291,25,'No','No','14','20','9 / 12','180 / 240','4 / 4','10.7 / 14.3%','1680',1000,'jme_SolvetWeldLoadingChart_0'),
(292,25,'No','No','16','20','6 / 9','120 / 180','4 / 4','10.0 / 15.0%','1200',1000,'jme_SolvetWeldLoadingChart_0'),
(293,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL);

/* Trigger structure for table `product_type` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `update_date_last_updated` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `update_date_last_updated` BEFORE UPDATE ON `product_type` FOR EACH ROW SET NEW.date_last_updated = NOW() */$$


DELIMITER ;

/* Trigger structure for table `product_type` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `update_date_deleted` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `update_date_deleted` BEFORE UPDATE ON `product_type` FOR EACH ROW BEGIN
   IF NEW.deleted_flag = 'Yes' THEN
      SET NEW.date_deleted = NOW();
   ELSEIF NEW.deleted_flag = 'No' THEN
      SET NEW.date_deleted = NULL;
   END IF;
END */$$


DELIMITER ;

/* Procedure structure for procedure `create_data_from_eagle_charts` */

/*!50003 DROP PROCEDURE IF EXISTS  `create_data_from_eagle_charts` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `create_data_from_eagle_charts`()
BEGIN
    -- Description: This routine does a complete truncation of current packing data and does a complete initialization of packing data using the data from the eagle charts.
    -- It should only be run when the eagle charts have been modified. Please note that any settings previously set are reset to the defaults including active_flag and deleted_flag.
    -- Once this is run, any previously created reports, etc., are invalid.

    -- Step 1: Truncate the `bundle`, `sku`, and `product_type` tables
    TRUNCATE TABLE h2o_packing_data_base_tables.bundle;
    TRUNCATE TABLE h2o_packing_data_base_tables.sku;
    TRUNCATE TABLE h2o_packing_data_base_tables.product_type;

    -- Step 2: Insert distinct product types into `product_type`
    INSERT INTO h2o_packing_data_base_tables.product_type (product_type)
    SELECT DISTINCT product_type
    FROM eagle_charts.loading_charts;

    -- Step 3: Populate the `sku` table with relevant data
    INSERT INTO sku (
        product_type_id, 
        size, 
        LENGTH, 
        pcs_lift, 
        ft_lift, 
        lifts_load, 
        load_percentage, 
        ft_load, 
        SOURCE
    )
    SELECT 
        product_type.product_type_id, 
        size, 
        LENGTH, 
        pcs_lift, 
        ft_lift, 
        lifts_load, 
        load_percentage, 
        ft_load, 
        SOURCE
    FROM eagle_charts.loading_charts
    JOIN product_type ON product_type.product_type = eagle_charts.loading_charts.product_type
    WHERE eagle_charts.loading_charts.line_number IS NOT NULL
      AND eagle_charts.loading_charts.product_type IS NOT NULL;

    -- Step 4: Populate the `bundle` table with distinct records from `sku`
    INSERT INTO bundle (
        SKU_Id, 
        size, 
        LENGTH, 
        pcs_lift, 
        ft_lift, 
        lifts_load, 
        load_percentage, 
        ft_load, 
        SOURCE
    )
    SELECT DISTINCT 
        SKU_Id, 
        size, 
        LENGTH, 
        pcs_lift, 
        ft_lift, 
        lifts_load, 
        load_percentage, 
        ft_load, 
        SOURCE
    FROM sku;

    -- Step 5: Call the stored procedure to process the records
    CALL update_bundles();
END */$$
DELIMITER ;

/* Procedure structure for procedure `SelectDistinctProductType` */

/*!50003 DROP PROCEDURE IF EXISTS  `SelectDistinctProductType` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `SelectDistinctProductType`()
BEGIN
  TRUNCATE TABLE h2o_packing_data_base_tables.bundle;
  TRUNCATE TABLE h2o_packing_data_base_tables.sku;
    TRUNCATE TABLE h2o_packing_data_base_tables.sku;
    TRUNCATE TABLE h2o_packing_data_base_tables.product_type;
    INSERT INTO h2o_packing_data_base_tables.product_type (product_type)
    SELECT DISTINCT product_type 
    FROM eagle_charts.loading_charts;
     INSERT INTO sku

    (product_type_id, size, LENGTH, pcs_lift, ft_lift, lifts_load, load_percentage, ft_load, SOURCE)

    SELECT product_type.product_type_id, size, LENGTH, pcs_lift, ft_lift, lifts_load, load_percentage, ft_load, SOURCE

    FROM eagle_charts.loading_charts

    JOIN product_type

    ON product_type.product_type = eagle_charts.loading_charts.product_type

    WHERE eagle_charts.loading_charts.line_number IS NOT NULL AND eagle_charts.loading_charts.product_type IS NOT NULL;
INSERT INTO bundle (SKU_Id, size, LENGTH, pcs_lift, ft_lift, lifts_load, load_percentage, ft_load, SOURCE)
SELECT DISTINCT SKU_Id, size, LENGTH, pcs_lift, ft_lift, lifts_load, load_percentage, ft_load, SOURCE
FROM sku;

-- Call the stored procedure to process the records

CALL update_bundles();


END */$$
DELIMITER ;

/* Procedure structure for procedure `update_bundles` */

/*!50003 DROP PROCEDURE IF EXISTS  `update_bundles` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `update_bundles`()
BEGIN
    -- Description: This procedure processes records in the `bundle` table where the `size`, 
    -- `pcs_lift`, `ft_lift`, `lifts_load`, or `load_percentage` columns contain a comma or slash.
    -- It splits these records into separate rows, inserts them back into the `bundle` table, 
    -- and removes all non-numeric characters (except decimal points in `load_percentage`) from specified columns.

    DECLARE done INT DEFAULT FALSE;

    -- Step 1: Create a temporary table with records from the `bundle` table where `size`, `pcs_lift`, `ft_lift`, `lifts_load`, or `load_percentage` contains a comma or slash
    DROP TEMPORARY TABLE IF EXISTS temp_table;
    CREATE TEMPORARY TABLE temp_table AS
    SELECT *
    FROM bundle
    WHERE size LIKE '%,%' 
       OR pcs_lift LIKE '%/%' 
       OR ft_lift LIKE '%/%' 
       OR lifts_load LIKE '%/%' 
       OR load_percentage LIKE '%/%';

    -- Show the contents of the temporary table after creation
    SELECT * FROM temp_table;

    -- Step 2: Delete those records from the `bundle` table
    DELETE FROM bundle
    WHERE bundle_id IN (SELECT bundle_id FROM temp_table);

    -- Loop to process records
    WHILE EXISTS (SELECT 1 FROM temp_table WHERE size LIKE '%,%' 
                                           OR pcs_lift LIKE '%/%' 
                                           OR ft_lift LIKE '%/%' 
                                           OR lifts_load LIKE '%/%' 
                                           OR load_percentage LIKE '%/%') DO

        -- Step 3: Insert processed records back into the `bundle` table
        INSERT INTO bundle (
            SKU_Id, 
            size, 
            LENGTH, 
            pcs_lift, 
            ft_lift, 
            lifts_load, 
            load_percentage, 
            ft_load, 
            SOURCE
        )
        SELECT 
            SKU_Id, 
            SUBSTRING_INDEX(size, ',', 1) AS size, 
            LENGTH, 
            SUBSTRING_INDEX(pcs_lift, '/', 1) AS pcs_lift, 
            SUBSTRING_INDEX(ft_lift, '/', 1) AS ft_lift, 
            SUBSTRING_INDEX(lifts_load, '/', 1) AS lifts_load, 
            SUBSTRING_INDEX(load_percentage, '/', 1) AS load_percentage, 
            ft_load, 
            SOURCE
        FROM temp_table;

        -- Step 4: Remove the first part of the `size` and other columns from the temporary table
        UPDATE temp_table
        SET 
            size = SUBSTRING(size, LOCATE(',', size) + 1),
            pcs_lift = SUBSTRING(pcs_lift, LOCATE('/', pcs_lift) + 1),
            ft_lift = SUBSTRING(ft_lift, LOCATE('/', ft_lift) + 1),
            lifts_load = SUBSTRING(lifts_load, LOCATE('/', lifts_load) + 1),
            load_percentage = SUBSTRING(load_percentage, LOCATE('/', load_percentage) + 1);

        -- Show the contents of the temporary table after update
        SELECT * FROM temp_table;

        -- Step 5: Insert records from the temporary table back into the `bundle` table where `size` does not contain a comma or slash
        INSERT INTO bundle (
            SKU_Id, 
            size, 
            LENGTH, 
            pcs_lift, 
            ft_lift, 
            lifts_load, 
            load_percentage, 
            ft_load, 
            SOURCE
        )
        SELECT 
            SKU_Id, 
            size, 
            LENGTH, 
            pcs_lift, 
            ft_lift, 
            lifts_load, 
            load_percentage, 
            ft_load, 
            SOURCE
        FROM temp_table
        WHERE size NOT LIKE '%,%' 
          AND pcs_lift NOT LIKE '%/%' 
          AND ft_lift NOT LIKE '%/%' 
          AND lifts_load NOT LIKE '%/%' 
          AND load_percentage NOT LIKE '%/%';

        -- Step 6: Delete records from the temporary table where `size` does not contain a comma or slash
        DELETE FROM temp_table
        WHERE size NOT LIKE '%,%' 
          AND pcs_lift NOT LIKE '%/%' 
          AND ft_lift NOT LIKE '%/%' 
          AND lifts_load NOT LIKE '%/%' 
          AND load_percentage NOT LIKE '%/%';

    END WHILE;

    -- Step 7: Remove all non-numeric characters (except decimal points in `load_percentage`) from specified columns
    UPDATE bundle
    SET 
        LENGTH = TRIM(BOTH ' ' FROM LENGTH),
        pcs_lift = TRIM(BOTH ' ' FROM pcs_lift),
        ft_lift = TRIM(BOTH ' ' FROM ft_lift),
        lifts_load = TRIM(BOTH ' ' FROM lifts_load),
        load_percentage = TRIM(BOTH ' ' FROM load_percentage),
        ft_load = TRIM(BOTH ' ' FROM ft_load);

    UPDATE bundle
    SET 
        LENGTH = REGEXP_REPLACE(LENGTH, '[^0-9]', ''),
        pcs_lift = REGEXP_REPLACE(pcs_lift, '[^0-9]', ''),
        ft_lift = REGEXP_REPLACE(ft_lift, '[^0-9]', ''),
        lifts_load = REGEXP_REPLACE(lifts_load, '[^0-9]', ''),
        load_percentage = REGEXP_REPLACE(load_percentage, '[^0-9.]', ''),
        ft_load = REGEXP_REPLACE(ft_load, '[^0-9]', '');

    -- Step 8: Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_table;
END */$$
DELIMITER ;

/*Table structure for table `v_product_sku_bundle` */

DROP TABLE IF EXISTS `v_product_sku_bundle`;

/*!50001 DROP VIEW IF EXISTS `v_product_sku_bundle` */;
/*!50001 DROP TABLE IF EXISTS `v_product_sku_bundle` */;

/*!50001 CREATE TABLE  `v_product_sku_bundle`(
 `productTypeId` int ,
 `productType` varchar(100) ,
 `skuId` int ,
 `skuSize` varchar(255) ,
 `skuLength` varchar(255) ,
 `skuPcsLift` varchar(255) ,
 `skuFtLift` varchar(255) ,
 `skuLiftsLoad` varchar(255) ,
 `skuLoadPercentage` varchar(255) ,
 `skuFtLoad` varchar(255) ,
 `skuPopularity` int ,
 `bundleId` int ,
 `bundleSize` varchar(255) ,
 `bundlePcsLift` varchar(255) ,
 `bundleFtLift` varchar(255) ,
 `bundleLiftsLoad` varchar(255) ,
 `bundleLoadPercentage` varchar(255) ,
 `SOURCE` varchar(255) 
)*/;

/*View structure for view v_product_sku_bundle */

/*!50001 DROP TABLE IF EXISTS `v_product_sku_bundle` */;
/*!50001 DROP VIEW IF EXISTS `v_product_sku_bundle` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_product_sku_bundle` AS select `product_type`.`product_type_id` AS `productTypeId`,`product_type`.`product_type` AS `productType`,`sku`.`SKU_Id` AS `skuId`,`sku`.`size` AS `skuSize`,`sku`.`LENGTH` AS `skuLength`,`sku`.`pcs_lift` AS `skuPcsLift`,`sku`.`ft_lift` AS `skuFtLift`,`sku`.`lifts_load` AS `skuLiftsLoad`,`sku`.`load_percentage` AS `skuLoadPercentage`,`sku`.`ft_load` AS `skuFtLoad`,`sku`.`popularity_score` AS `skuPopularity`,`bundle`.`bundle_id` AS `bundleId`,`bundle`.`size` AS `bundleSize`,`bundle`.`pcs_lift` AS `bundlePcsLift`,`bundle`.`ft_lift` AS `bundleFtLift`,`bundle`.`lifts_load` AS `bundleLiftsLoad`,`bundle`.`load_percentage` AS `bundleLoadPercentage`,`bundle`.`SOURCE` AS `SOURCE` from ((`product_type` join `sku` on((`product_type`.`product_type_id` = `sku`.`product_type_id`))) join `bundle` on((`sku`.`SKU_Id` = `bundle`.`SKU_Id`))) where ((`product_type`.`active_flag` = 'Yes') and (`sku`.`active_flag` = 'Yes') and (`bundle`.`active_flag` = 'Yes')) order by `product_type`.`product_type`,`sku`.`LENGTH`,`sku`.`size`,`bundle`.`size` */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
