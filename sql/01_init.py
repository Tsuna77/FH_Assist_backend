from yoyo import step


# Table utilisateur
step("""
    CREATE TABLE `FH_Assistant`.`FH_user`
    (
      `id` INT NOT NULL AUTO_INCREMENT ,
      `email` VARCHAR(255) NOT NULL ,
      PRIMARY KEY (`id`),
      UNIQUE (`email`)
    )
    ENGINE = InnoDB;
    """)

# table contenant les hopitaux des utilisateurs
step("""
    CREATE TABLE `FH_Assistant`.`FH_hospital`
    (
      `id` INT NOT NULL AUTO_INCREMENT ,
      `id_user` INT NOT NULL ,
      `nom` VARCHAR(64) NOT NULL ,
      PRIMARY KEY (`id`)
    )
   ENGINE = InnoDB;
   """)

step("""
    ALTER TABLE `FH_Assistant`.`FH_hospital`
    ADD UNIQUE `unique_hospital`(`id_user`, `nom` );
    """)

# Table contenant la liste des salles
step("""
    CREATE TABLE `FH_Assistant`.`FH_Salles_Def`
    (
      `id` INT NOT NULL AUTO_INCREMENT ,
      `nom` VARCHAR(64) NOT NULL ,
      `staff` ENUM('medic', 'nurse') ,
      PRIMARY KEY (`id`)
    )
    ENGINE = InnoDB;
    """)

# Table contenant les stats des salles
step("""
    CREATE TABLE `FH_Assistant`.`FH_Salles_Stats`
    (
      `id` INT NOT NULL AUTO_INCREMENT ,
      `id_salles` INT NOT NULL ,
      `level` INT NOT NULL ,
      `competence` INT NOT NULL ,
      `temps` INT NOT NULL ,
      PRIMARY KEY (`id`)
    )
    ENGINE = InnoDB;
    """)

step("""
    ALTER TABLE `FH_Assistant`.`FH_Salles_Stats`
    ADD UNIQUE `unique_hospital`(`id_salles`, `level` );
    """)
