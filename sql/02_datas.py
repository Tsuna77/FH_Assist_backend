from yoyo import step

__depends__ = ['01_init']

# création des comptes par défaut
step("INSERT INTO `FH_Assistant`.`FH_user` (`id`, `email`) VALUES (1, 'r77raphy@gmail.com');");

# création des hopitaux par défaut
step("INSERT INTO `FH_Assistant`.`FH_hospital` (`id`, `id_user`, `nom`) VALUES (1,1 ,'TsunaCorp');");
step("INSERT INTO `FH_Assistant`.`FH_hospital` (`id`, `id_user`, `nom`) VALUES (2,1 ,'TsunaCorp 2');");


