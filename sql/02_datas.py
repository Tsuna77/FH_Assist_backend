from yoyo import step

__depends__ = ['01_init']

# création des comptes par défaut
step("INSERT INTO `FH_Assistant`.`FH_user` (`id`, `email`) VALUES (1, 'r77raphy@gmail.com');");

# création des hopitaux par défaut
step("INSERT INTO `FH_Assistant`.`FH_hospital` (`id`, `id_user`, `nom`) VALUES (1,1 ,'TsunaCorp');");
step("INSERT INTO `FH_Assistant`.`FH_hospital` (`id`, `id_user`, `nom`) VALUES (2,1 ,'TsunaCorp 2');");

# Généraliste
step("INSERT INTO `FH_Assistant`.`FH_Salles_Def` (`id`, `nom`, `staff`) VALUES (1,'Généraliste' ,'medic');")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL,1,0,0,30)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,1,2,30)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,2,5,29)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,3,8,29)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,4,11,28)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,5,15,28)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,6,18,26)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,7,22,26)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,8,26,24)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,9,31,24)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,10,35,22)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,11,41,22)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,12,47,21)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,13,54,20)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,14,60,20)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,15,67,20)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,16,74,19)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,17,82,19)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,18,89,18)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,19,97,18)")
step("INSERT INTO `FH_Assistant`.`FH_Salles_Stats` (`id`,`id_salles`,`level`, `competence` , `temps`) VALUES (NULL  ,1,20,105,17)")

step("INSERT INTO `FH_Assistant`.`FH_Salles_Def` (`id`, `nom`, `staff`) VALUES (2,'Diag de base' ,'medic');")
