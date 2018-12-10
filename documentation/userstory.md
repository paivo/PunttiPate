Uusi käyttäjä aloittaa rekisteröimällä itsensä sovelluksen aloitussivulla. Rekisteröitymiseen tarvitaan nimi, käyttäjätunnus ja salasana. Rekisteröitynyt käyttäjä voi kirjautua palveluun. Kirjautuminen vie käyttäjän sovelluksen etusivulle, jolla voi tarkastella kaikkien aikojen ja kuukauden parhaita penkkipunnerrus, jalkakyykky sekä maastaveto suorituksia (Vielä tekemättä). Etusivulla listataan myös suosituimmat kuntosalit. Etusivulta voi siirtyä omalle sivulle, jolla voi tarkastella omia tuloksia. Tällä sivulla voi myös poistaa omia tuloksia sekä asettaa ne julkisiksi, jotta muut voivat niitä myös tarkastella. Tulosten lisäämiselle on myös oma sivunsa. Käyttäjän voi myös poistaa kaikki tietonsa sivulta (Vielä tekemättä).

[User| (pk) id: Integer; name: String; username: String; password: String]
[Gym| (pk) id: Integer; name: String]
[GymUser| (pk) id: Integer; (fk) user_id: Integer; (fk) gym_id: Integer]
[Bench| (pk) id: Integer; (fk) user_id: Integer; weight: Integer; date: Date; public: Boolean]
[Squat| (pk) id: Integer; (fk) user_id: Integer; weight: Integer; date: Date; public: Boolean]
[Dead| (pk) id: Integer; (fk) user_id: Integer; weight: Integer; date: Date; public: Boolean]
[User]*-[GymUser]
[Gym]*-[GymUser]
[User]-*[Bench]
[User]-*[Squat]
[User]-*[Dead]
