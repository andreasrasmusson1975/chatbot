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
Koden ovan skapar ett sekventiell modell. Till denna läggs först ett tätt lager bestående av 100 neuroner. Aktiveringsfunktionen i detta lager är "rektified linear unit". Därefter läggs ett dropout lager till med en rate på 0.2, dvs varje neuron av de 100 neuronerna i det första lagret har 20%
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