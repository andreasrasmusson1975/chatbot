### Diskussion
I applikationen implementeras RAG-tekniker för att tillhandahålla en chatbot som kan svara på frågor om 209 olika 
tekniska manualer. Denna typ av applikation vore väldigt användbar för företag som tillverkar många olika produkter
och där det med varje produkt följer en användarmanual. En chatbot som kan svara på frågor om och förklara innehållet
i manualen blir väldigt värdefull för slutkunden. Ett annat potentiellt användningsområde vore om man till exempel
äger ett förlag som publicerar tekniska böcker eller studentliteratur och vill, utöver boken, tillhandahålla varje
student med en handledare som är expert på boken i fråga och som är tillgänglig dygnet runt.

Det är dock viktigt att säkra upp applikationen så att risken för att det ska gå att kringå systempromptar m.m. minimeras.
Detta är en verklig risk och om den inte hanteras kan det bli pinsamt för den organisation som satt chatboten i produktion.
Eftersom användning av de bästa underliggande modellerna inte är möjlig on-prem för de flesta organisationer, då de helt enkelt 
är för stora är det förenat med ansenliga kostnader för anrop till API om man vill driva en sån här applikation i stor skala, 
vilket också är något som en organisation måste ta i beaktande. Utöver det är användande av API-anrop förenat med risker 
avseende exempelvis GDPR. Alternativet är att använda sig av lokala modeller men då betalar man istället ett pris i form av 
att modellen inte är lika kompetent. Det går att göra lokala modeller bra men det är förenat med utvecklingskostnader.

Sammantaget kan den här typen av applikationer vara mycket intressanta för många olika typer av organisationer men det är
förenat med vissa risker som måste hanteras.

### Självutvärdering

#### Fråga 1
Vad har varit roligast i kunskapskontrollen?

#### Svar:
Roligast har nog varit att ställa frågor till manualassistenten och faktiskt få rimliga svar och se att det funkar. Att bygga
utvärderingsfunktionaliteten var också kul. Sen var det faktiskt också roligt att få installationsscripten att lira.

#### Fråga 2
Vilket betyg anser du att du ska ha och varför?

##### Svar:
Jag har:

1. gjort en chattbot som använder sig av RAG-teknik för att begränsa svaren till en viss kontext
2. gjort ett system för att evaluera chattboten (se evaluate.py, evaluator.py och evaluation.xlsx).
3. skrivit kod som fungerar och dokumenterat den väl.
4. besvarat de teoretiska frågorna kort och koncist
5. diskuterat potentiella användningsområden och risker

Därför tycker jag att VG är rimligt.

##### Fråga 3
Vad har varit mest utmanande i arbetet och hur har du hanterat det?

#### Svar:
Jag började med att implementera chattboten med hjälp av det API som openai tillhandahåller. Därefter började jag arbeta med
att migrera lösningen till en lokal modell. Men vilken modell jag än provade så var den antingen alldeles för långsam eller 
så gave den inte lika bra som openai's modeller. Till slut valde jag därför att behålla den ursprungliga lösningen. Hade jag 
haft mer tid, hade jag fortsatt att arbeta med att få en lokal modell tillräckligt bra. 

