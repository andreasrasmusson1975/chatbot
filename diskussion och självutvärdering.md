### Diskussion
I applikationen implementeras RAG-tekniker för att tillhandahålla en chatbot som kan svara på frågor om 209 olika 
tekniska manualer. Denna typ av applikation vore väldigt användbar för företag som tillverkar många olika produkter
och där det med varje produkt följer en användarmanual. En chatbot som kan svara på frågor om och förklara innehållet
i manualen blir väldigt värdefull för slutkunden. Ett annat potentiellt användningsområde vore om man till exempel
äger ett förlag som publicerar tekniska böcker eller studentliteratur och vill, utöver boken, tillhandahålla varje
student med en handledare som är expert på boken i fråga och som är tillgänglig dygnet runt.

Det är dock viktigt att säkra upp applikationen så att risken för att det ska gå att kringå systempromptar m.m. minimeras.
Detta är en verklig risk och om den inte hanteras kan det bli pinsamt för den organisation som satt chatboten i produktion.
Eftersom användning av de bästa underliggande modellerna inte är möjlig i en lokal miljö, då de helt enkelt är för stora är
det förenat med ansenliga kostnader för anrop till API om man vill driva en sån här applikation i stor skala, vilket också
är något som en organisation måste ta i beaktande. Utöver det är användande av API-anrop förenat med risker avseende exempel-
vis GDPR. Alternativet är att använda sig av lokala modeller men då betalar man istället ett pris i form av att modellen inte 
är lika kompetent. Det går att göra lokala modeller bra men det är förenat med utvecklingskostnader.

Sammantaget kan den här typen av applikationer vara mycket intressanta för många olika typer av organisationer men det är
förenat med vissa risker som måste hanteras. 