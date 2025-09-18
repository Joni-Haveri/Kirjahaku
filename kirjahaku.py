#  --------------------------------------------------------------------------------------------------------------------------------------
# |                                                          Kirjanhaku-ohjelma                                                          |
# |                        Tämä on Pythonilla tehty komentorivipohjainen sovellus, jolla voit hakea kirjoja                              |
# |                              OpenLibraryn (https://openlibrary.org/) avoimen rajapinnan kautta.                                      |                                         
# |                                                                                                                                      |
# |                                        Käyttäjä voi mm. hakea kirjoja kolmella eri tavalla:                                          |                                                                               
# |                                                     1. Kirjan nimellä (title)                                                        |
# |                                                     2. Kirjailijan nimellä (author)                                                  |
# |                            3. Yhdistetyllä haulla (kirjan nimi + kirjailija), joka käyttää laajempaa tietokantaa (q)                 |
# |                                                                                                                                      |
# |    Ohjelma näyttää käyttäjälle viisi hakutulosta, jotka sisältävät kirjan nimen, kirjailijan, ja julkaisuvuoden jos semmoinen löytyy |    
# |                                                                                                                                      |
# |                                          Toimii vain ja ainoastaan tällä hetkellä Terminaalissa                                      |
# |                                              Ota huomioon, että sinulla on vakaa verkkoyhteys                                        |
# |                                                                                                                                      |
# |                                                         Ohjelmoinut Joni Haveri                                                      |
# |                                                         jonihaveri08@gmail.com                                                       |
# |                                                                                                                                      |
#  --------------------------------------------------------------------------------------------------------------------------------------

# Tuodaan requests -kirjasto, jotta API-kutsuja voidaan käyttää
import requests

# Viiveiden lisäämistä varten
import time

# Käytettävän API:n URL-osoite
base_url = "https://openlibrary.org/search.json?"

# Funktio, jossa kirjaimet tulevat hieman viiveellä kirjain kirjaimelta, näyttääkseen hienolta terminaalissa (Vain visuaalisuuden takia)
def type_writer(text, delay=0.05):
 
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Funktio verkkoyhteyden tarkastamiseen
def check_internet():
    try:
        # Pyyntö OpenLibraryyn
        requests.get("https://openlibrary.org", timeout=10)
        return True
    except requests.exceptions.RequestException:
        return False

# Jos verkkoyhteyttä ei ole, tulostetaan ilmoitus
if not check_internet():
    print("Ei internet yhteyttä! Tarkista verkkoyhteys ja käynnistä sitten ohjelma uudelleen")
    time.sleep(3)
    exit()

# Funktio, joka hakee OpenLibrary API:sta kirjan nimellä
def search_by_title(title):
    url_1 = f"{base_url}title={title}"
    response = requests.get(url_1)
    show_results(response)

# Funktio, joka hakee OpenLibrary API:sta kirjailijan nimellä
def search_by_author(author):
    url_2 = f"{base_url}author={author}"
    response = requests.get(url_2)
    show_results(response)

# Funktio, joka hakee OpenLibrary API:sta kirjan-, että kirjailijan nimellä (yhdistetty haku)
# Tarkempi vaihtoehto etsiessään tiettyä haluamaansa kirjaa (laajempi tietokanta edellisiin nähden)
def search_by_title_and_author(title_and_author):
    url_3 = f"{base_url}q={title_and_author}"
    response = requests.get(url_3)
    show_results(response)

# Funktio, joka näyttää hakutulokset käyttäjälle
def show_results(response, max_results = 5):

    # Virheilmoitus, jos API-pyyntö epäonnistuu 
    # Esimerkiksi yhden kirjaimen haut tuottavat valtavan määrän tuloksia Openlibraryn palvelimillaan, joka saa API-pyynnön menemään ihan sekaisin.
    # Vaihtoehtoja on jopa tuhansia, eikä palvelin juuri tämän takia osaa/pysty lähettämään dataa takaisin)
    # Tämän takia asia on otettu huomioon virheilmoituksena
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return
    
    # Haetaan vastaus JSON-muodossa
    data = response.json()

    # Haetaan listasta "docs"-avaimen arvot (eli kirjat)
    docs = data.get("docs", [])

    # Jos kirjaa ei löydy
    if not docs:
        print("Valitettavasti Hakusi ei tuottanut yhtään tulosta!")
        return
    
    # Käydään tulokset läpi for-silmukalla ja tulostetaan tiedot
    # max_results = 5, eli loppujen lopuksi tulostetaan viisi kirjaa, jotka ovat lähempänä käyttäjän antamaa hakusanaa/sanoja
    for i, book in enumerate(docs[:max_results], start=1):

        # Kirjan nimi
        # Unknown = oletusarvo = None, jos kirjan nimeä ei ole tiedossa
        title = book.get("title", "Unknown") 

        # Kirjailijan nimi
        # Unknown = oletusarvo = None, jos kirjailijan nimeä ei ole tiedossa
        authors = ", ".join(book.get("author_name", ["Unknown"]))

        # Julkaisuvuosi, joka tulostetaan kirjan perään
        # Jos julkaisuvuotta ei löydy tietokannasta, merkitään sitä '???'
        year = book.get("first_publish_year", "???")
        print(f"{i}.{title} - {authors} ({year})")


print("\n")

# Tervetuloa-viesti      
type_writer("Tervetuloa terminaalissa toimivaan Kirjanhaku -ohjelmaani📚")
type_writer("Voit hakea kirjan muun muassa nimen, kirjailijan tai yhdistetyn haun perusteella.\n")
print(" -----------------------------")
print("|    1. Kirjan nimellä        |")
print("|    2. Kirjailijan nimellä   |")
print("|    3. Kirja + kirjailija    |")
print(" -----------------------------\n")

# Pääsilmukka, joka kysyy käyttäjältä, mitä hakutapaa käytetään
while True:
    try:
        choose = int(input("\nValitse numero 1 - 3 sen perusteella, mitä hakutapaa haluat käyttää."
        " (1) kirjan nimi, (2) kirjailijan nimi, (3) yhdistetty haku (nimi + kirjailija): "))

        # Jos käyttäjä syöttää muuta kuin numerot väliltä 1 - 3, tulostetaan virheilmoitus
        if choose not in [1, 2, 3]:
            print("\nVirheellinen valinta! Valitse numero 1 - 3 väliltä")
            continue

    # Jos käyttäjä syöttää kirjaimia
    except ValueError:
        print("\nVirheellinen valinta, älä syötä kirjaimia, vaan numeroita väliltä 1 - 3")
        continue

    # Kirjan nimen syöttäminen   
    if choose == 1:
        hakusana = input("Anna kirjan nimi: ")

        # Jos käyttäjä ei syötä mitään
        if not hakusana:
            print("Kirjan nimi ei saa olla tyhjä, Yritä uudelleen.\n")
            continue

        print() # Tulostaa tyhjän rivin
        
        # Haetaan kirjoja nimen perusteella
        search_by_title(hakusana)

    # Kirjailijan nimen syöttäminen
    if  choose == 2:
        hakusana = input ("Anna kirjailijan nimi: ")
        print()
        if not hakusana:
            print("Kirjailijan nimi ei saa olla tyhjä, Yritä uudelleen.\n")
            continue

        # Tarkistetaan onko hakusanassa numeroita
        if hakusana.strip().lstrip('-').isdigit():
            print("Kirjailijan nimi ei voi olla pelkästään positiivinen tai negatiivinen numero/numeroita. Yritä uudelleen\n")
            continue

        # Haetaan kirjoja kirjailijan nimen perusteella
        search_by_author(hakusana)

    # Yhdistetty haku (Kirjan nimi, ja kirjailija)
    if  choose == 3:
        while True:

            book_name = input("Anna kirjan nimi: ")
            book_author = input("Anna kirjailijan nimi: ")
            print()
            # Jos kirjan nimeen tai kirjailijaan käyttäjä ei syötä mitään "Enter"- tulostetaan huomautus käyttäjälle
            if not book_name or not book_author:
                print("Molemmat tiedot ovat pakollisia. Yritä uudelleen\n")
                continue
            
            # Jos käyttäjä syöttää 'kirjailija' -syötteeseen positiivisen tai negatiivisen luvun - tulostetaan huomautus käyttäjälle
            elif book_author.strip().lstrip('-').isdigit():
                print("Kirjailijan nimi ei voi olla pelkkä numero. Yritä uudelleen.\n")
                continue

            # Yhdistetään nimi ja kirjailija
            combined = f"{book_name} {book_author}"

            # Haetaan kirjoja hakusanojen perusteella
            search_by_title_and_author(combined)
            break

    # Kysytään käyttäjältä, aikooko jatkaa vielä hakua
    while True:
        continue_finding = input("\nHaluatko jatkaa kirjojen etsiskelyä? Paina 'k' = kyllä, tai 'e' = ei (k/e): ").lower()

        # Jos käyttäjän syöte on k-kirjain, silmukka katkaistaan ja kirjojen hakeminen alkaa alusta
        if continue_finding == "k":
            break
        
        # jos käyttäjän syöte on e-kirjain, Python-ohjelma sulkeutuu
        elif continue_finding == 'e':
            type_writer("\nKiitos, että käytit Kirjanhaku-ohjelmaani!📚")
            type_writer("Sulkeutuu...")

            # Odotetaan hetki ennen sulkeutumista
            time.sleep(3)

            #Lopetetaan ohjelma
            exit()
            
        # Jos käyttäjä syöttää muuta kun k, tai e
        else:
            print("\nVäärä syöte, Kirjoita 'k' jatkaaksesi tai 'e' lopettaaksesi")