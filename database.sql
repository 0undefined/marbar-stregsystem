CREATE TABLE cms_marbar (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `title` varchar(512) NOT NULL,
  `date_start` datetime(6) NOT NULL,
  `duration` bigint(20) NOT NULL,
  `extra_hours` bigint(20) NOT NULL,
  `note` longtext NOT NULL,
  `style` longtext NOT NULL,
  `banner` varchar(100) DEFAULT NULL,
  `elfsight_apikey` varchar(128) DEFAULT NULL
);

CREATE TABLE cms_marbarconsumer (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` varchar(64) NOT NULL UNIQUE
);

CREATE TABLE `cms_marbarcounter` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `counter` int(11) NOT NULL,
  `consumer_id` bigint(20) NOT NULL REFERENCES cms_marbarconsumer(id),
  `marbar_id` bigint(20) NOT NULL REFERENCES cms_marbar(id)
);
