# Space Invaders (1978) 

Rekreacija igre Space Invaders iz 1978. godine sa modernim dizajnom.  
Igra je realizovana uz pomoc PyQt5 biblioteke u python programskom jeziku.  
Cilj igre je pobediti sve vanzemaljce.  

## Neophodne tehnologije 
- [PyQt5](https://pypi.org/project/PyQt5/)  
- [Python3](https://www.python.org/downloads/)  
- [PyCharm](https://www.jetbrains.com/pycharm/download)  

## Uputstvo za korisćenje  

### Meni  
Prilikom pokretanja aplikacije, prikazuje se početni meni.  

![Start Menu](Space%20Invaders/doc/menu.png)  

### Postoji nekoliko režima igranja:  
- Singleplayer  
- Multiplayer  
- Turnir  

Svaki od ovih režima biće objašnjen u posebnim sekcijama.  

### Singleplayer  

Singleplayer je mod igrice u kojem učestvuje jedan igrač.  
Klikom na `start game`, odabira se ovaj mod. 

![select sp](Space%20Invaders/doc/select-sp1.png)  
  
 Nakon klika, korisniku se otvara prozor u kom treba da unese svoj nickname  
 i nudi mu se izbor raznih svemirskih brodova.  
 Polja su validirana, tj. korisnik ne može da nastavi dalje bez unetog imena.  
 
 Pritiskom na `-> start`, igra započinje.  
 
 ![Game sp](Space%20Invaders/doc/game-sp.png)  
 
 
### Multiplayer  

U multiplayer modu, u igri učestvuju dva igrača.  
Svaki igrač ima svoj nickname i svoj svemirski brod, koji odabere u select prozoru koji mu se prikaže  
kada klikne na `multiplayer` dugme.  

Neophodno je da korisnicka imena igrača budu unikatna.  
Ukoliko se imena poklapaju, igrači će dobiti poruku da je neopodno da igra neće započeti  
dok se ne ispoštuje pravilo.  

![select mp](Space%20Invaders/doc/sc-mp.png)  

Nakon unosa imena i selekcije broda, prelazi se na glavni prozor u kom se odvija igrica.  

![game mp](Space%20Invaders/doc/game-mp.png)  


### Turnir  

Tournament mod podržava da u igri učestvuje veći broj igrača.  
Za turnir je potrebno minimum 4 igrača, a maksimalno je podržano 8 igrača.  
Igrači se takmiče po fazama (Quarterfinals -> Semifinals -> The Grand Finale)  
Na sledećoj slici je ilustrovano kako se odvija turnir.  

![tournament](Space%20Invaders/doc/tournament.png)  

Takođe, za turnir takođe važi pravilo da nickname svakog igrača mora biti unikatan, dok brodovi  
mogu da budu isti.  

Klikom na `tournament` dugme, korisniku se nudi izbor koliko igrača želi da prijavi.  
Nakon toga, svaki igrač unosi svoj nickname i bira svog avatara (spaceship).  
Naredna slika je primer turnira sa 4 igrača.  

![4playersTournament](Space%20Invaders/doc/4players.png)  

Kada svi igrači podese svoj unos, nasumično se izaberu dva igrača koji će započeti turnir.  
Igra se odvija sve dok oba igrača ne poginu. Pobednik runde je onaj igrač koji je proveo duže vremena  
igrajući igru, i on prolazi u sledeću fazu.  
Nakon toga se takmiče druga dva igrača, od kojih pobednik prolazi dalje i takmiči se sa pobednikom  
prethodne runde.  
Turnir se odvija sve dok se ne sastanu dva igrača koja su došla do finala i nakon te finalne runde  
se proglašava pobednik turnira.  

 
 ### Ciklus igre   
 #### Početak
	 Na početku igre, vanzemaljci se nalaze na sredini ekrana na vrhu, a startne pozicije igrača su u  
	 donjim uglovima.  
	 Inicijalizuju se 4 štita, koji brane igrača od napada vanzemaljaca.  Štitovi se postepeno raspadaju  
	 kako ih pogodi metak vanzemaljca.  
	 Vanzemaljci se kreću levo-desno i vremenom se spuštaju ka dnu ekrana.  
	 Na određenom vremenskom intervalu vanzemaljci ispaljuju metke koji lete vertikalno ka dole.  
	 Ukoliko se avatar igrača nađe na mestu metka vanzemaljca, tj. dođe do kolizije igrača sa metkom,  
	 igrač gubi život.  
	 Igrači mogu da ispaljuju metke na odgovarajući taster, koji se kreću vertikalno ka gore, i u koliko  
	 metak pogodi vanzemaljca, on nestaje.  
 #### Naredni nivo
	Prilikom prelaska na sledeći nivo, povećava se brzina kojom se kreću vanzemaljci, ubrzava se kretanje  
	metaka ispaljenih od strane vanzemaljaca i smanjuje se interval na kom vanzemaljci ispaljuju metke. 
	Takođe, igračev brod dobija blago ubrzanje kretanja.  
	Ukoliko je igrač pokupio neku slučajnu silu, na narednom nivou mu se oduzima.  	
	Ako je igra u multiplayer modu, ukoliko jedan igrač pogine, drugi nastavlja da igra, i u narednom nivou  
	on nastavlja sam da igra. 
	Životi igrača se resetuju na 3 i štitovi se ponovo inicijalizuju.  
#### DeusEx
	Deus-Ex je komponenta koja na određenom vremenskom intervalu prikazuje slučajnu silu na ekranu,  
	koju igrači mogu da pokupe. Slučajna sila se na ekranu zadržava 2 sekunde, i za to vreme, igrači imaju  
	priliku da je pokupe.  
	
	Postoje tri vrste slučajnih sila:  
	- Skull  
	- Life  
	- Armour  

##### Skull ![skull](Space%20Invaders/doc/skull-resized.gif)
 Ukoliko igrač pokupi ovu silu, gubi jedan život.  
##### Life ![life](Space%20Invaders/doc/lives.png)
 Kada igrač pokupi `srce`, dobija život gratis. Ukoliko je igrač pokupio `srce` dok je imao 3 života,  
neće mu se povećati broj života.   
##### Armour ![armour](Space%20Invaders/doc/armor-resized.gif)
Ukoliko igrač pokupi ovu silu, dobija dodatni štit oko svog avatara, koji ga štiti od metka vanzemaljaca,  
i od gubljenja života ukoliko pokupi slučajnu silu `Skull`.  
Kada igrač, dok ima aktivan štit, pokupi `Skull` silu ili ga pogodi metak vanzemaljca, štit nestaje. 
		
#### Kraj
	Kada svi igrači poginu, prikaže se Game Over prozor koji ispisuje nickname pobednika.  	
 
 ### Pravila igre  
- Svaki igrač ima 3 života
- Pobednik je igrač koji ostane najduže u igri  
- Samo jedan igrač može da pokupi slučajnu silu  
- Prelazak na sledeći nivo se dešava kada se unište svi vanzemaljci  
 
 ### Komande  
 | ACTION | PLAYER 1 | PLAYER 2 |
 | :--- | :---: | ---: |
 | **Move left** | `A` | `Key-Left` |
 | **Move right** | `D` | `Key-Right` |
 | **Shoot** | `space` | `K` |
 
 ### Opis realizacije
Za realizaciju ovog projekta, korišćena je `PyQt5` biblioteka uz pomoć koje je izgrađena grafika.  
Ažuriranje grafike odrađeno je upotrebom procesa (`multiprocessing`) i tredova (`QThread`).  
Komunikacija između procesa se vrši preko `Queue-a`.  

| `Space Invaders`  
|--> `client` : ***prozori za interakciju sa korisnikom***  
|--> `config` --> `cfg.py` : ***konfiguracioni fajl sa konstantama***  
|--> `doc` : ***sadržaj za dokumentaciju***  
|--> `Entities` --> ***objekti u igri***  
|--> `images` --> ***slike za objekte***  
|--> `utilities` --> ***logika za niti i procese***  
|--> `main.py` --> ***glavna skripta***  
