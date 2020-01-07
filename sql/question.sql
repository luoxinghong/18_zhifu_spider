/*
 Navicat Premium Data Transfer

 Source Server         : 本机mysql
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : localhost:3306
 Source Schema         : zhihu

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : 65001

 Date: 02/08/2019 10:38:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for questiones
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `q_id` int(11) DEFAULT NULL,
  `q_full_name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `q_alias_name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `q_title` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `q_detail` longtext COLLATE utf8mb4_bin,
  `q_create_time` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `q_attention_num` int(11) DEFAULT NULL,
  `answer_num` int(11) DEFAULT NULL,
  `q_scanner_num` int(11) DEFAULT NULL,
  `best_answer_id` int(11) DEFAULT NULL,
  `q_url` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `tags` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `qq_id` (`q_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC;
