# PunttiPate

Sivulla voi lisätä itselleen penkissä, kyykyssä ja maastavedossa tehtyjä yhden toiston tuloksia. Sivulla voi myös tarkastella koko tietokannan kaikkien aikojen parhaita tuloksia, sekä kuukauden parhaita tuloksia. Suoritukseen merkitään nostetun painon lisäksi päivämäärä, sali sekä tieto suorituksen julkisuudesta.

[PunttiPate Herokussa](https://punttipate.herokuapp.com/)

Kirjautuminen:

Käyttäjänimi: hello
Salasana: world

[Tietokantakaavio](https://github.com/paivo/PunttiPate/blob/master/documentation/Tietokantakaavio.png)

[Käyttötapaukset](https://github.com/paivo/PunttiPate/blob/master/documentation/userstory.md)

Ennen ohjelman asentamista tarvitset:
[Työvälineet ja niiden asentaminen](https://materiaalit.github.io/tsoha-18/tyovalineet/)

Asennus- ja käynnistämisohje paikallisesti:
1. Kopioi repositorion osoite.
2. Mene terminaalissa kansioon johon haluat ohjelman asentaa.
3. Kopio projekti: git clone https://github.com/ErkkiEsimerkki/EsimerkkiProjekti
4. Siirry projektin juurikansiooon: ~/EsimerkkiProjekti$
5. Luo virtuaaliympäristö: python3 -m venv venv
6. Aktivoi virtuaaliympäristö: source venv/bin/activate
7. Lataa riippuvuudet: pip install -r requirements.txt
8. Käynnistä sovellus: python3 run.py
9. Avaa selain ja aseta osoitteeksi: http://localhost:5000/

Asennus- ja käynnistämisohje Herokussa:
Neljä ensimmäistä kohtaa ovat samat kuin paikallisesti käynnistäessä.
5. Luodaan sovellukselle tietokanta Herokuun: heroku addons:add heroku-postgresql:hobby-dev
6. Pusketaan sovellus herokuun: git push heroku master
