from yoyo import step

step("CREATE TABLE `FH_Assistant`.`FH_user` ( `id` INT NOT NULL AUTO_INCREMENT , `email` VARCHAR(255) NOT NULL , PRIMARY KEY (`id`), UNIQUE (`email`)) ENGINE = InnoDB;")

step("CREATE TABLE `FH_Assistant`.`FH_hospital` ( `id` INT NOT NULL AUTO_INCREMENT , `id_user` INT NOT NULL , `nom` VARCHAR(64) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")


