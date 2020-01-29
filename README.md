#  Super Trivia
## Robin van Beek, Suzanne Jacobsen en Marten Staghouwer

## Features van de website:
* Verschillende trivia categorieën
* Geen inlog nodig
* Verschillende moeilijkheidsniveaus
* Classic mode: 10 vragen
* Custom mode: Tussen de 1 en 50 vragen

## Doorloop website:
1. Scherm met de naam, een start knop en speluitleg.
2. Pagina waar de categorie en moeilijkheid gekozen kan worden.
3. Pagina waar gekozen kan worden of het single- of multiplayer is en de vraag of je een multiplayer game wilt joinen/maken.

### Classic Mode:
1. Pagina waar de user een naam kan invullen die gebruikt kan worden voor de highscores.
2. Pagina met een vraag, 4 geschuffelde antwoorden, een countdownbar, een progresscounter, aantal goede antwoorden.
3. Highscorepagina waar de top 10 scores van dezelfde category staan.

### Custom Mode:
1. Pagina waar de user een naam kan invullen en tussen 1 tot en met 50 vragen kan kiezen.
2. Pagina met een vraag, 4 geschuffelde antwoorden, een countdownbar, een progresscounter, aantal goede antwoorden.
3. Highscorepagina met de top 3 scores bij het gekozen aantal vragen.

### screenshots applicatie:
![Schets ideeën van pagina's](/doc/screenshot.png)
![links tussen pagina's](/doc/template_linking.png)

### helpfuncties en beschrijvingen:
* classic_question.py: Stopt vragen voor de classic mode in een database.
* correct.py: Verwijderd vragen uit de database als deze beantwoordt zijn.
* highscore.py: Regelt de highscores en voegt deze toe aan de database als dit nodig is.
* customgame.py: Stopt vragen voor de custom mode in een database.
* disp_question.py: Regelt vragendata en stuurt deze naar application.py.
* highscore.py: Handelt alle highscore related database queries af.

### Plugins en frameworks:
* flask: https://flask.palletsprojects.com/en/1.1.x/
* boodstrap: https://getbootstrap.com/docs/4.4/getting-started/introduction/
* AJAX: https://developer.wordpress.org/plugins/javascript/ajax/