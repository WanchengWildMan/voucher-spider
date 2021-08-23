CREATE TABLE IF NOT EXISTS  voucher (
  city varchar(255) NOT NULL,
  gdp19 double DEFAULT NULL,
  gdpStage19 double DEFAULT NULL,
  peo double DEFAULT NULL,
  moneyDigit double DEFAULT NULL,
  lon double NOT NULL,
  lat double NOT NULL,
  giveOutMethod varchar(255) NOT NULL,
  methodDescribe varchar(255) NOT NULL,
  giveTimeDescribe varchar(255) NOT NULL,
  moneyDescribe varchar(255) NOT NULL,
  numDescribe varchar(255) NOT NULL,
  ruleDescribe varchar(255) NOT NULL,
  url varchar(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY IDX_a4efa4fe4fe6fb5465109c2f00 (city)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;