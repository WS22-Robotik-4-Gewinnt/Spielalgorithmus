# Spielalgorithmus

## Vorschlag Datenstruktur
### Spielfeld
```
6 0  0  0  0  0  0  0
5 0  0  0  0  0  0  0
4 0  0  0  0  0  0  0
3 h  0  0  r  0  0  0
2 h  r  r  h  r  0  r
1 h  h  h  r  h  r  r
--1--2--3--4--5--6--7```

### Übertragung
```{ "Column1": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}, {"Row7":"r"}],
     "Column2": [{"Row1":"h"}, {"Row2":"r"}, {"Row3":"r"}, {"Row4":"h"}, {"Row5":"r"}, {"Row6":"0"}, {"Row7":"r"}],
     "Column3": [{"Row1":"h"}, {"Row2":"0"}, {"Row3":"0"}, {"Row4":"r"}, {"Row5":"0"}, {"Row6":"0"}, {"Row7":"0"}],
}
// h = Human Player | r = Robot Player | 0 = empty space```
