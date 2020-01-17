#  Trivia Project
## Features van de website:
* Multiplayer
* verschillende triviacategoriën
* kahootstyle player/player, team/team
* verschillende speelcategoriën
* Geen inlog nodig
* Verschillende moeilijkheidsniveaus

## Doorloop website:
1. Beginscherm waarop de gamemode gekozen kan worden
2. Scherm waarop mensen de game kunnen joinen en startknop
3. [Op scherm] een vraag met 4 mogelijke antwoorden.

## Technisch ontwerp:
### lijst routes:
* main pagina: landings scherm wat gebruikers als eerste zien. Een scherm met een start knop en het logo van de site.
* optie menu: Op deze pagina kan de gebruiker kiezen welke categorie en moeilijkheidsgraad de vragen zullen zijn.
* vragen pagina: Op deze pagina staan de vragen met 4 verschillende antwoorden.
* high score pagina: Op deze pagina zijn de highscores van gebruikers te zien.
* multiplayer-eindpagina: Op deze pagina is te zien welk team/welk persoon heeft gewonnen en de bijbehorende score

### schets applicatie:
![Schets ideeën van pagina's](/doc/schets.png)
![links tussen pagina's](/doc/template_linking.png)

### helpfuncties en beschrijvingen:
* question.py: haalt vragen van een gekozen moeilijkheidsgraad en categorie op en returned deze. [post/get]
* score(?).py: voegt score toe of vraagt scores op [get]
* session(?).py: beheerd sessies voor multiplayer games en zorgt dat mensen dezelfde vragen krijgen/dat de scores opgeslaan zijn tot het einde van het spel. [post]

### Plugins en frameworks:
* flask: https://flask.palletsprojects.com/en/1.1.x/
* boodstrap: https://getbootstrap.com/docs/4.4/getting-started/introduction/