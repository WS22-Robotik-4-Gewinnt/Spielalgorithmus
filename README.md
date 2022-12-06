# Spielalgorithmus

## Datenstruktur
### Spielfeld 7x6
```
6 0  0  0  0  0  0  0
5 0  0  0  0  0  0  0
4 0  0  0  0  0  0  0
3 h  0  0  r  0  0  0
2 h  r  r  h  r  0  r
1 h  h  h  r  h  r  r
--1--2--3--4--5--6--7

// h = Human Player | r = Robot Player | 0 = empty space
```

## Schnittstellen / Kommunikation
###  Bildverarbeitung -> Spielalgorithmus
```json
{ "Column1": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}, {"Row7":"r"}],
     "Column2": [{"Row1":"h"}, {"Row2":"r"}, {"Row3":"r"}, {"Row4":"h"}, {"Row5":"r"}, {"Row6":"0"}, {"Row7":"r"}],
     "Column3": [{"Row1":"h"}, {"Row2":"0"}, {"Row3":"0"}, {"Row4":"r"}, {"Row5":"0"}, {"Row6":"0"}, {"Row7":"0"}],
}
```

### Übertragung Spielalgorithmus -> Hardwaresteuerung
```json
{
 "x_pos": 4,
 "y_pos": 5
}
```

## Algorithmen
### Minimax
Der Minimax-Algorithmus ist ein Spielstrategie für sogenannte Nullsummenspiele, die außerdem für zwei Spieler ausgelegt sind. Neben Vier gewinnt kann der Algorithmus also beispielsweise auch für Schach oder Go eingesetzt werden.
Die Strategie lässt sich durch einen Baum darstellen, der die möglichen Züge für die Spieler darstellt. Die Höhe bestimmt abwechselnd die Züge des Minimizing bzw. Maximizing Players. Anschließend wird eine Tiefensuche auf einem Baum durchgeführt, die für die Stellungen auf dem Spielfeld Punkte vergibt. 
