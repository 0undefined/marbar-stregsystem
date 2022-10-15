# Marbar Stregsystem V2.0

Dette er det nyere stregsystem, konverteret fra PHP+Python til Django 4.0

Det originale system ligger i git på atlas: git@atlas:marbar.git


# Usage

* Du kan finde en liste over gamle, kommende og nuværende marbare ved /index
* Du kan tilgå tilføjelser og fjernelse af streger af nuværende aktive marbar
  under /interface


# Development

Du kan køre stregsystemet lokalt med docker-compose ved at skrive
`docker-compose up` og tilgå siden i localhost:8000

Alt koden er under stregsystem/ mappen, stregsystem/cms (CMS: Content Management
System) indeholder alt logikken omkring views (sider), skabeloner, og modeller
(database logik).

## Deployment

0. SSH til atlas
1. `sudo su`
2. `cd ~/marbar-stregsystem/ && git pull`
3. Til sidst kør følgende for at bygge, tagge, uploade og genstarte
   stregsystemet:
   ```
   docker build -t marbar-stregsystem:latest .
   docker tag marbar-stregsystem localhost:5000/marbar-stregsystem
   docker push localhost:5000/marbar-stregsystem
   docker pull localhost:5000/marbar-stregsystem
   systemctl restart docker-stregsystem.service
   ```

_er `pull` strengt talt nødvendigt?_

# TODO

* Gør det muligt at tilføje/fjerne consumers fra marbare.
  _således bliver det muligt at bruge systemet til andre ting end marbar, ved at
  kunne fjerne "Aspiranter", "Crew" osv. og tilføje andre ting._
* Tilføje timestamps til streger således at det er muligt at plotte en tidsgraf
  ligesom i det gamle system.
  _Dette gør at det bliver meget tydligt at se aktiviteten af køkkener og kunne
  spotte eventuelt snydere!_
* Tilføj det gamle (eller lav et nyt) bar-plot system.
  + Eller: Vis top 5 Consumers på forsiden
* Dokumenter hvordan det virker
* Automatiser deployment
