-- MySQL dump 10.16  Distrib 10.3.9-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: adh6
-- ------------------------------------------------------
-- Server version	10.3.9-MariaDB-1:10.3.9+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adherents`
--

DROP TABLE IF EXISTS `adherents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adherents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `login` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `chambre_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `date_de_depart` date DEFAULT NULL,
  `commentaires` varchar(255) DEFAULT NULL,
  `mode_association` datetime DEFAULT '2011-04-30 17:50:17',
  `access_token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_adherents_on_chambre_id` (`chambre_id`)
) ENGINE=InnoDB AUTO_INCREMENT=55121 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_creation` int(11) NOT NULL,
  `date_modif` int(11) NOT NULL,
  `categorie` text NOT NULL,
  `titre` text NOT NULL,
  `contenu` text NOT NULL,
  `publie` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `caisse`
--

DROP TABLE IF EXISTS `caisse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `caisse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fond` decimal(10,2) DEFAULT NULL,
  `coffre` decimal(10,2) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chambres`
--

DROP TABLE IF EXISTS `chambres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chambres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `telephone` varchar(255) DEFAULT NULL,
  `vlan_old` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `dernier_adherent` int(11) DEFAULT NULL,
  `vlan_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_chambres_on_vlan_id` (`vlan_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2853 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comptes`
--

DROP TABLE IF EXISTS `comptes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comptes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `intitule` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ecritures`
--

DROP TABLE IF EXISTS `ecritures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ecritures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `intitule` varchar(255) DEFAULT NULL,
  `montant` decimal(10,2) DEFAULT NULL,
  `moyen` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `compte_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `utilisateur_id` int(11) DEFAULT NULL,
  `adherent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_ecritures_on_compte_id` (`compte_id`),
  KEY `index_ecritures_on_utilisateur_id` (`utilisateur_id`),
  KEY `index_ecritures_on_adherent_id` (`adherent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=114810 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `illustrations`
--

DROP TABLE IF EXISTS `illustrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `illustrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenu` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=233 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inscriptions`
--

DROP TABLE IF EXISTS `inscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inscriptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `login` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `chambre_id` int(11) DEFAULT NULL,
  `duree_cotisation` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_inscriptions_on_chambre_id` (`chambre_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `last_use_mac_U6`
--

DROP TABLE IF EXISTS `last_use_mac_U6`;
/*!50001 DROP VIEW IF EXISTS `last_use_mac_U6`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `last_use_mac_U6` (
  `mac` tinyint NOT NULL,
  `commentaires` tinyint NOT NULL,
  `last_seen` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `login_authorize`
--

DROP TABLE IF EXISTS `login_authorize`;
/*!50001 DROP VIEW IF EXISTS `login_authorize`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `login_authorize` (
  `id` tinyint NOT NULL,
  `login` tinyint NOT NULL,
  `vlan_nb` tinyint NOT NULL,
  `date_de_depart` tinyint NOT NULL,
  `mode_association` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `login_to_macf`
--

DROP TABLE IF EXISTS `login_to_macf`;
/*!50001 DROP VIEW IF EXISTS `login_to_macf`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `login_to_macf` (
  `login` tinyint NOT NULL,
  `mac` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `login_to_macw`
--

DROP TABLE IF EXISTS `login_to_macw`;
/*!50001 DROP VIEW IF EXISTS `login_to_macw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `login_to_macw` (
  `login` tinyint NOT NULL,
  `mac` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `mac_vendors`
--

DROP TABLE IF EXISTS `mac_vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mac_vendors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prefix` varchar(255) DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1093 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mail_templates`
--

DROP TABLE IF EXISTS `mail_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mail_templates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) DEFAULT NULL,
  `sujet` varchar(255) DEFAULT NULL,
  `template` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expediteur` varchar(255) DEFAULT NULL,
  `destinataire` varchar(255) DEFAULT NULL,
  `sujet` varchar(255) DEFAULT NULL,
  `mail_id` varchar(255) DEFAULT NULL,
  `corps` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `ancestry` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_messages_on_ancestry` (`ancestry`),
  KEY `index_messages_on_mail_id` (`mail_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11753 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `modifications`
--

DROP TABLE IF EXISTS `modifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `adherent_id` int(11) DEFAULT NULL,
  `action` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `utilisateur_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_modifications_on_adherent_id` (`adherent_id`),
  KEY `index_modifications_on_utilisateur_id` (`utilisateur_id`)
) ENGINE=InnoDB AUTO_INCREMENT=781133 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `nb_ordinateurs_actifs`
--

DROP TABLE IF EXISTS `nb_ordinateurs_actifs`;
/*!50001 DROP VIEW IF EXISTS `nb_ordinateurs_actifs`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `nb_ordinateurs_actifs` (
  `adherent_id` tinyint NOT NULL,
  `login` tinyint NOT NULL,
  `prenom` tinyint NOT NULL,
  `nom` tinyint NOT NULL,
  `mail` tinyint NOT NULL,
  `nb_mac_actifs` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `nb_portables_actifs`
--

DROP TABLE IF EXISTS `nb_portables_actifs`;
/*!50001 DROP VIEW IF EXISTS `nb_portables_actifs`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `nb_portables_actifs` (
  `id` tinyint NOT NULL,
  `login` tinyint NOT NULL,
  `nom` tinyint NOT NULL,
  `prenom` tinyint NOT NULL,
  `mail` tinyint NOT NULL,
  `nb_mac_actif` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `ordinateurs`
--

DROP TABLE IF EXISTS `ordinateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordinateurs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `dns` varchar(255) DEFAULT NULL,
  `adherent_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `ipv6` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_ordinateurs_on_adherent_id` (`adherent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=118063 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `portables`
--

DROP TABLE IF EXISTS `portables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `portables` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(255) DEFAULT NULL,
  `adherent_id` int(11) DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_portables_on_adherent_id` (`adherent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=157683 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ports`
--

DROP TABLE IF EXISTS `ports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rcom` int(11) DEFAULT NULL,
  `numero` varchar(255) DEFAULT NULL,
  `oid` varchar(255) DEFAULT NULL,
  `switch_id` int(11) DEFAULT NULL,
  `chambre_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_ports_on_switch_id` (`switch_id`),
  KEY `index_ports_on_chambre_id` (`chambre_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3093 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `radacct`
--

DROP TABLE IF EXISTS `radacct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radacct` (
  `radacctid` bigint(21) NOT NULL AUTO_INCREMENT,
  `acctsessionid` varchar(64) NOT NULL DEFAULT '',
  `acctuniqueid` varchar(32) NOT NULL DEFAULT '',
  `username` varchar(64) NOT NULL DEFAULT '',
  `groupname` varchar(64) NOT NULL DEFAULT '',
  `realm` varchar(64) DEFAULT '',
  `nasipaddress` varchar(15) NOT NULL DEFAULT '',
  `nasportid` varchar(15) DEFAULT NULL,
  `nasporttype` varchar(32) DEFAULT NULL,
  `acctstarttime` datetime DEFAULT NULL,
  `acctupdatetime` datetime DEFAULT NULL,
  `acctstoptime` datetime DEFAULT NULL,
  `acctinterval` int(12) DEFAULT NULL,
  `acctsessiontime` int(12) unsigned DEFAULT NULL,
  `acctauthentic` varchar(32) DEFAULT NULL,
  `connectinfo_start` varchar(50) DEFAULT NULL,
  `connectinfo_stop` varchar(50) DEFAULT NULL,
  `acctinputoctets` bigint(20) DEFAULT NULL,
  `acctoutputoctets` bigint(20) DEFAULT NULL,
  `calledstationid` varchar(50) NOT NULL DEFAULT '',
  `callingstationid` varchar(50) NOT NULL DEFAULT '',
  `acctterminatecause` varchar(32) NOT NULL DEFAULT '',
  `servicetype` varchar(32) DEFAULT NULL,
  `framedprotocol` varchar(32) DEFAULT NULL,
  `framedipaddress` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`radacctid`),
  UNIQUE KEY `acctuniqueid` (`acctuniqueid`),
  KEY `username` (`username`),
  KEY `framedipaddress` (`framedipaddress`),
  KEY `acctsessionid` (`acctsessionid`),
  KEY `acctsessiontime` (`acctsessiontime`),
  KEY `acctstarttime` (`acctstarttime`),
  KEY `acctinterval` (`acctinterval`),
  KEY `acctstoptime` (`acctstoptime`),
  KEY `nasipaddress` (`nasipaddress`)
) ENGINE=InnoDB AUTO_INCREMENT=541763 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `radcheck`
--

DROP TABLE IF EXISTS `radcheck`;
/*!50001 DROP VIEW IF EXISTS `radcheck`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `radcheck` (
  `id` tinyint NOT NULL,
  `username` tinyint NOT NULL,
  `attribute` tinyint NOT NULL,
  `op` tinyint NOT NULL,
  `value` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `radgroupreply`
--

DROP TABLE IF EXISTS `radgroupreply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radgroupreply` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `groupname` varchar(64) NOT NULL DEFAULT '',
  `attribute` varchar(64) NOT NULL DEFAULT '',
  `op` char(2) NOT NULL DEFAULT '=',
  `value` varchar(253) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `groupname` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `radpostauth`
--

DROP TABLE IF EXISTS `radpostauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radpostauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL DEFAULT '',
  `pass` varchar(64) NOT NULL DEFAULT '',
  `reply` varchar(32) NOT NULL DEFAULT '',
  `authdate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45309533 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `radreply`
--

DROP TABLE IF EXISTS `radreply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radreply` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL DEFAULT '',
  `attribute` varchar(64) NOT NULL DEFAULT '',
  `op` char(2) NOT NULL DEFAULT '=',
  `value` varchar(253) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `radusergroup`
--

DROP TABLE IF EXISTS `radusergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radusergroup` (
  `username` varchar(64) NOT NULL DEFAULT '',
  `groupname` varchar(64) NOT NULL DEFAULT '',
  `priority` int(11) NOT NULL DEFAULT 1,
  KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schema_migrations`
--

DROP TABLE IF EXISTS `schema_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schema_migrations` (
  `version` varchar(255) NOT NULL,
  UNIQUE KEY `unique_schema_migrations` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `switches`
--

DROP TABLE IF EXISTS `switches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `communaute` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(255) DEFAULT NULL,
  `message_id` int(11) DEFAULT NULL,
  `utilisateur_id` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_tickets_on_message_id` (`message_id`),
  KEY `index_tickets_on_utilisateur_id` (`utilisateur_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9753 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tutorials`
--

DROP TABLE IF EXISTS `tutorials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tutorials` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `langue` varchar(255) DEFAULT NULL,
  `titre` varchar(255) DEFAULT NULL,
  `contenu` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `introduction` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `utilisateurs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `access` int(11) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `login` varchar(255) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `access_token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1223 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vlans`
--

DROP TABLE IF EXISTS `vlans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vlans` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` int(11) DEFAULT NULL,
  `adresses` varchar(255) DEFAULT NULL,
  `adressesv6` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `webs`
--

DROP TABLE IF EXISTS `webs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `adherent_id` int(11) DEFAULT NULL,
  `login` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `actif` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `last_use_mac_U6`
--

/*!50001 DROP TABLE IF EXISTS `last_use_mac_U6`*/;
/*!50001 DROP VIEW IF EXISTS `last_use_mac_U6`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `last_use_mac_U6` AS select `ordinateurs`.`mac` AS `mac`,`adherents`.`commentaires` AS `commentaires`,`ordinateurs`.`last_seen` AS `last_seen` from (`adherents` join `ordinateurs`) where `adherents`.`id` = `ordinateurs`.`adherent_id` and `ordinateurs`.`ip` like '157.159.46.%' order by `ordinateurs`.`last_seen` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `login_authorize`
--

/*!50001 DROP TABLE IF EXISTS `login_authorize`*/;
/*!50001 DROP VIEW IF EXISTS `login_authorize`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `login_authorize` AS select `adherents`.`id` AS `id`,`adherents`.`login` AS `login`,`vlans`.`numero` AS `vlan_nb`,`adherents`.`date_de_depart` AS `date_de_depart`,`adherents`.`mode_association` AS `mode_association` from ((`adherents` join `chambres`) join `vlans`) where `adherents`.`chambre_id` = `chambres`.`id` and `chambres`.`vlan_id` = `vlans`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `login_to_macf`
--

/*!50001 DROP TABLE IF EXISTS `login_to_macf`*/;
/*!50001 DROP VIEW IF EXISTS `login_to_macf`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `login_to_macf` AS select `A`.`login` AS `login`,`O`.`mac` AS `mac` from (`adherents` `A` join `ordinateurs` `O`) where `A`.`id` = `O`.`adherent_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `login_to_macw`
--

/*!50001 DROP TABLE IF EXISTS `login_to_macw`*/;
/*!50001 DROP VIEW IF EXISTS `login_to_macw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `login_to_macw` AS select `adherents`.`login` AS `login`,`portables`.`mac` AS `mac` from (`portables` join `adherents`) where `portables`.`adherent_id` = `adherents`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `nb_ordinateurs_actifs`
--

/*!50001 DROP TABLE IF EXISTS `nb_ordinateurs_actifs`*/;
/*!50001 DROP VIEW IF EXISTS `nb_ordinateurs_actifs`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `nb_ordinateurs_actifs` AS select `a`.`id` AS `adherent_id`,`a`.`login` AS `login`,`a`.`prenom` AS `prenom`,`a`.`nom` AS `nom`,`a`.`mail` AS `mail`,count(`o`.`mac`) AS `nb_mac_actifs` from (`ordinateurs` `o` join `adherents` `a` on(`a`.`id` = `o`.`adherent_id`)) where to_days(current_timestamp()) - to_days(`o`.`last_seen`) < 15 group by `a`.`id` order by count(`o`.`mac`) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `nb_portables_actifs`
--

/*!50001 DROP TABLE IF EXISTS `nb_portables_actifs`*/;
/*!50001 DROP VIEW IF EXISTS `nb_portables_actifs`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `nb_portables_actifs` AS (select `adherents`.`id` AS `id`,`adherents`.`login` AS `login`,`adherents`.`nom` AS `nom`,`adherents`.`prenom` AS `prenom`,`adherents`.`mail` AS `mail`,count(0) AS `nb_mac_actif` from (`adherents` join `portables` on(`adherents`.`id` = `portables`.`adherent_id`)) where to_days(current_timestamp()) - to_days(`portables`.`last_seen`) <= 30 group by `adherents`.`id`,`adherents`.`nom`,`adherents`.`prenom`,`adherents`.`login`,`adherents`.`mail` order by count(0) desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `radcheck`
--

/*!50001 DROP TABLE IF EXISTS `radcheck`*/;
/*!50001 DROP VIEW IF EXISTS `radcheck`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `radcheck` AS select `adherents`.`id` AS `id`,`adherents`.`login` AS `username`,'NT-Password' AS `attribute`,':=' AS `op`,`adherents`.`password` AS `value` from `adherents` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-30 18:38:29
