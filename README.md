# HTBOldSchool
HTB Old Machines - OffSeasson

## EASY MACHINES

[GreenHorn](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Easy/GreenHorn) - Easy

Es fácil acceder a la máquina y llegar a user, pero tiene cosillas el conseguir la flag de root, se necesita depixelar una imagen.

[BoardLigth](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Easy/BoardLigth) - Easy

En sencilla en general, solo hay que buscar los CVE para aprovechar las vulnerabilidades.

[Usage](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Easy/Usage) - Easy

No es díficil pero se hace larga, se usa el sqlmap lo cual alarga el pentesting, y luego la escalada de privilegios a admin lleva algo de investigación. No es díficil pero lleva tiempo


## MEDIUM MACHINES

[Blurry](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Medium/Blurry) - Medium

La máquina tiene miga, hay que manejarse con software que no se conoce y requiere conocimientos de programación bajo mi punto de vista.
Es cierto que el acceso a user se facilita con el CVE y es sencillo, pero luego la escalada de privilegios parece más complicada

[WifineticTwo](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Medium/WifineticTwo) - Medium

La máquina tiene migilla al configurar el segundo route para poder entrar, pero en general es divertida

[SolarLab](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Medium/SolarLab) - Medium

Se complica un poco la parte de acceder a root, se hace algo larga y hay que usar varios cve más que buscar credenciales. No es demasiado díficil,
pero si larga

[Runner](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Medium/Runner) - Medium

Fue fácil la verdad, más que otras del mismo nivel, si es cierto que hay que buscar un poco y trastear con las aplicaciones que se encuentran

[Runner](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Medium/Cascade) - Medium

Sencilla, tiene cosas simples de AD

## HARD MACHINES

[Freelancer](https://github.com/manuelsantosiglesias/HTBOldSchool/tree/main/Hard/Freelancer) - Hard

Máquina complicadísima, si bien la bandera de user es más o menos normal, luego hay que hacer de todo, necesité bastante ayuda después de la
flag de user.

Hay unos scripts para el archivo final de ccache, pero no era necesario, con el export se arreglaba
