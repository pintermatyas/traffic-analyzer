# Témalaboratórium 2022-23/1

Tracking előtt:

![Output](md_files/sampleOutputGif.gif)


Tracking és sebességmeghatározás után:

![Output](md_files/sampleOutputGifTracking.gif)

Le lett korlátozva a felismeréshez használható rész az alsó felére a képnek, hogy ne legyen olyan sok fals pozitív felismerés, amit egy frame után el is veszít. Az autók irányát színkódoltam: a felénk haladó zöld, az elfele haladó kék téglalapot kap.

Picit fejlettebb verziója:
![Output](md_files/2022-11-20-10-48-18.gif)

Az autók irányának meghatározása az eddigiekhez képest semmit nem különbözik, csak pontatlanabb meghatározás ennyit számít. Eddig úgy volt kiszámolva hogy ha az előző pozíciótól felfele van akkor elfele halad, ha lefele van akkor meg felénk jön.  

Heatmap az elhaladó autókról, a sample3 file-on futtatva, rossz iránymeghatározási módszerrel:

![Output](md_files/sample2_detections.png)

Látszódik az ábrán is, hogy főleg a távolabbi régiókban sok zöld pont jelenik meg a kék pontok között, ez a fals meghatározás miatt van

Ez kijavítva: a legelső pozíciójához méri az irányt, nem az előzőhöz:

![Output](md_files/2022-11-20-11-29-21.gif)

![Output](md_files/sample2_detection_fine_dir.png)

Itt már nincsenek az ábrán random zöld pontok a kék pontok között, ki lett javítva a hiba

A következő feladat a sávok, de minimum az úttest felismerése:

![Output](md_files/lane-detection-alpha_model.gif)

Továbbfejlesztve:

![Output](md_files/lane-detection-beta_model.gif)

A nem releváns részeket levágtam róla, így igényesebben is néz ki.

![Output](md_files/lane-detection-3_0_model.gif)

Az egymásba csúszó vagy egymáshoz nagyon közel lévő vonalakat kiszűrtem és csak a leghosszabbat hagytam meg.

Ezután ismét a sebesség meghatározására mentem rá, sikerült egy jobb verziót összehozni:

![Output](md_files/speed-determination.gif)
