#  Trivia Project
## Features van de website:
* Multiplayer (WIP)
* Verschillende trivia categoriën
* Geen inlog nodig
* Verschillende moeilijkheidsniveaus

## Doorloop website:
1. Scherm met de naam, een start knop en speluitleg.
2. Pagina waar de categorie en moeilijkheid gekozen kan worden.
3. Pagina waar gekozen kan worden of het single- of multiplayer is en de vraag of je een multiplayer game wilt joinen/maken.

### Singleplayer:
1. Pagina waar de user een naam kan invullen die gebruikt kan worden voor de highscores.
2. Vragenpagina met de vraag, 4 antwoorden, een countdown en een scorecounter.
3. Highscorepagina waar de top 10 scores staan.

### Multiplayer:
#### Room aanmaken
1. Scherm waarop de host een roomnaam kan opgeven en een username kan opgeven.
2. Vragenpagina met de vraag, 4 antwoorden, een countdown, een roomcode en een scorecounter.
3. Highscorepagina waar de top 3 scores staan.

#### Room joinen:
1. Pagina waar je een roomcode op kan geven en een username.
2. Highscorepagina waar de top 3 scores staan.

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
* sp_question.py: haalt vragen van een gekozen moeilijkheidsgraad en categorie op en returned deze. [post/get]
* score(?).py: voegt score toe of vraagt scores op [get]
* session(?).py: beheerd sessies voor multiplayer games en zorgt dat mensen dezelfde vragen krijgen/dat de scores opgeslaan zijn tot het einde van het spel. [post]

### Plugins en frameworks:
* flask: https://flask.palletsprojects.com/en/1.1.x/
* boodstrap: https://getbootstrap.com/docs/4.4/getting-started/introduction/
* AJAX: https://developer.wordpress.org/plugins/javascript/ajax/