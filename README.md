# Obligoppgave-7
obligatorisk gruppe-oppgave


Her er teksten for oppgaven:

To ting rundt prosjekt del 1 datafila:

1: Tanken var i utgangspunktet å bruke temperaturfeltet som var i fila for å regne ut sommerdager, høysommerdager og tropedager i deloppgave h). Men begrepene sommerdag, høysommerdag og tropedag er egentlig definert med maksimaltemperatur heller enn døgnmiddeltemperaturen som var med i fila. Derfor har jeg lagt ved ei ny datafil som også inneholder makstemperaturen og som dere kan bruke til deloppgave h) om dere ønsker et riktigere resultat. Det er fortsatt døgnmiddeltemperaturen som skal brukes for deloppgave f)

2: For de fleste datoene så ligger de allerede i riktig rekkefølge i fila, men det er noen få unntak hvor tidligere datoer ligger helt på slutten av fila. Det er ikke obligatorisk å håndtere dette, men å ikke håndtere det kan føre til litt rare grafer hvor det går linjer mot venstre. Den enkleste måten å håndtere det på er følgende: Mens dere leser fila, sjekk at datoen til linja dere leser nå er høyere enn høyeste leste dato hittil. Er den ikke det, forkast linja. Å implementere dette eller mer avanserte måter å håndtere det på er frivillige tilleggsoppgaver.

Mer avanserte måter som er innenfor pensum:

Les fila to ganger. Første gang lager dere ei liste med datoer og lister med tomme verdier for de andre feltene. Andre gang leser dere dato og finner den i datolista og fyller inn verdiene på riktig sted i de andre listene.
Lag et dict med dato som nøkkel og ei liste med de andre verdiene som verdi. Etter å ha lest fila, hent ut nøklene fra dict-et med datoer, lag ei liste av dem og sorter dem. Bruk den sorterte lista med datoer for å hente ut de andre verdiene i riktig rekkefølge fra dict-et og lag lister som dere kan bruke til plottingen.
