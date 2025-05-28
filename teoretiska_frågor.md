# Teoretiska frågor

### Fråga 1
Hur är AI, Maskininlärning och Deep Learning relaterat?
### Svar:
AI är det övergripande ämnsesområdet som omfattar all form av artificiell intelligens, från expertsystem till chatbottar till datorseende och allt däremellan. Maskininlärning är en del av AI och omfattar den del där datorer lär från befintlig data för att kunna tillämpa vad de lärt på ny osedd
data. Deep learning är en del av machine learning och omfattar machine learning med hjälp av (djupa) neurala nätverk.

### Fråga 2
Hur är Tensorflow och Keras relaterat?
### Svar:
Tensorflow är ett lågnivåramverk för operationer på tensorer och för träning av neurala nätverk. Keras är en del av Tensorflow och utgör ett högnivå-API för att bygga och träna modeller.

### Fråga 3
Vad är en parameter? Vad är en hyperparameter?
### Svar:
En parameter är en kvantitet som en maskininlärningsalgoritm lär sig med hjälp av datan, exempelvis vikterna i ett neuralt nätverk. En hyperparameter
är en kvantitet som berättar för algoritmen hur den ska lära sig, exempelvis hur mycket, och på vilket sätt regularisering sker.

### Fråga 4
När man skall göra modellval och modellutvärdering kan man använda tränings-, validerings- och testdataset. Förklara hur de olika delarna kan användas.
### Svar:
Träningsdatasetet är den del av datan som algoritmen ska lära ifrån (träna på). Valideringsdatasetet kan användas exempelvis för att finstämma hyperparametrar (Man väljer de hyperparametervärden som ger bäst score på valideringsdatasetet). Testdatasetet används för att få ett unbiased mått 
på generaliseringsförmågan hos modellen.

### Fråga 5
Förklara vad nedanstående kod gör:

    n_cols = x_train.shape[1]
    nn_model = Sequential()
    nn_model.add(Dense(100, activation='relu', input_shape=(n_cols, )))
    nn_model.add(Dropout(rate=0.2))
    nn_model.add(Dense(50, activation='relu'))
    nn_model.add(Dense(1, activation='sigmoid'))
    
    nn_model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy' ])
    
    early_stopping_monitor = EarlyStopping(patience=5)
    nn_model.fit(
        x_train,
        y_train,
        validation_split=0.2,
        epochs=100,
        callbacks=[early_stopping_monitor])

### Svar:
Koden ovan skapar en sekventiell modell. Till denna läggs först ett tätt lager bestående av 100 neuroner. Aktiveringsfunktionen i detta lager är "rektified linear unit". Därefter läggs ett dropout lager till med en rate på 0.2, dvs varje neuron av de 100 neuronerna i det första lagret har 20%
risk att droppas. Sedan läggs ytterligare ett tätt lager, med 50 neuroner och aktiveringsfunktion "relu" till. Därefter läggs det sista lagret till. Detta har en neuron och aktiveringsfunktion sigmoid (aktiveringsfunktion för binär klassificering).

Därefter kompileras modellen. Den optimeringsfunktion som används för bakåtpropageringen är "adam". Förlustfunktionen som används är "binary crossentropy", vilket lämpar sig för ett binärt klassificeringsproblem. Vidare specificeras att vi ska föla även "accuracy" under träningens gång.

I nästa steg skapas ett EarlyStopping objekt, vilket har som funktion att se till att, när modellen tränas, så stoppas träningen när vi inte sett en förbättring i binar crossentropy under 5 epoker. Därefter tränas modellen på träningsdatat under 100 epoker med validering på 20% av datan.

### Fråga 6
Vad är syftet med att regularisera en modell?
### Svar:
Att förhindra överanpassning.

### Fråga 7
”Dropout” är en regulariseringsteknik, vad är det för något?
### Svar:
Dropout innebär att man ger varje neuron i ett lager en viss sannolikhet att inte få bidra med någon output. Eftersom det kommer att variera över tid, vilka neuroner som "drabbas", så får detta (i den bästa av världar) till följd att neuronerna i lagret blir generalister istället för specialister (teamet måste lösa uppgiften även om någon spelare är sjuk). Detta i sin tur minskar variansen och det hela blir därmed en regulariserande åtgärd.

### Fråga 8
”Early stopping” är en regulariseringsteknik, vad är det för något?
### Svar:
Early stopping innebär att om validerinsförlusten inte förbättras under ett visst (förbestämt) antal epoker, så upphör träningen. Det får till följd att nätverket inte "snöar in" för mycket på egenheterna i just det datasetet man tränar på, utan istället stannar när det inte finns mer att lära (enligt de x senaste epokerna) och åtgärden har därför en regulariserande effekt.

### Fråga 9
Din kollega frågar dig vilken typ av neuralt nätverk som är populärt för bildanalys, vad svarar du?
### Svar:
Jag svarar: CNN (Convolutional neural networks).

### Fråga 10
Förklara översiktligt hur ett ”Convolutional Neural Network” fungerar.

### Svar:
Bland de dolda lagerna i ett CNN finns det minst konvolutionslager. Sådana lager använder sig att kärnor (små matriser), även kallat filter för att "scanna av" bilden och beräkna en viktad summa av pixelvärdena i filtrets synfält (synfältet bestäms av kärnans dimensioner). På så sätt lär sig neuronerna i lagret, vilka delar av en bild som är viktiga för att lösa uppgiften. Output från ett konvolutionslager kallas feature maps. Dessa används sedan som input till påföljande lager. Ibland används poolinglager efter ett konvolutionellt lager för att reducera dimensionerna på feature maps.

### Fråga 11
Vad gör nedanstående kod?

    model.save("model_file.keras")
    my_model = load_model("model_file.keras")

### Svar:
Sparar och sen laddar in en befintlig modell.

### Fråga 12
Deep Learning modeller kan ta lång tid att träna, då kan GPU via t.ex. Google Colab skynda på träningen avsevärt. Skriv mycket kortfattat vad CPU och GPU är.

### Svar:
CPU står för Central Processing Unit och är den del av en datorn som vi vanligtvis kallar processorn. Den sköter alla möjliga beräkningar som görs i en dator. Den har oftast ett begränsat antal, säg 4-16 kraftfulla kärnor som kan köra parallellt. GPU står för Graphical Processing Unit och är en del av den del av datorn som vi vanligtvis kallar grafikkortet. En GPU har till skillnad från en CPU många enkla kärnor (tusentals) och kan därför, med hjälp av parallellisering utföra beräkningar väldigt snabbt. GPU:er lämpar sig därför väl för beräkningstunga operationer som till exempel träning av neurala nätverk (eller rendera spel).




