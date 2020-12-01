---
title: ELNA Supermatic-Musterdiscs selber herstellen
categories:
- 3D-Druck
tags:
- 3d-druck 
- nähen
header:
  teaser: "/assets/images/snippet_images/content/prototyp-einer-selbst-gedruckten-elna-disc_2.jpeg"
---

Wir versuchen in einem Projekt, Discs für ELNA-Nähmaschinen selbst am 3D-Drucker herzustellen. Dazu muss die Funktionsweise der Discs zuerst verstanden werden und wir müssen sie selbst auf ein Modell herunterrechnen können.

Dieser Artikel erklärt die aktuellen Fortschritte bei der Analyse und Herstellung der Elna-Discs. [Der aktuelle Stand](http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks/ "http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks.html") ist jeweils in unserem [Wiki](http://wiki.starship-factory.ch/ "http://wiki.starship-factory.ch/") zu finden.

# Basisdiscs

![Viele verschiedene Elna-Discs](/assets/images/snippet_images/content/viele-verschiedene-elna-discs_2.jpeg "Viele verschiedene Elna-Discs")

Für die ELNA Supermatic-Maschinen aus den 50ern gibt es hauptsächlich 2 Arten von Discs:

- Einfache Discs sind ziemlich flach und haben nur einen Aussenkranz. Dabei ist die Transportgeschwindigkeit konstant und es wird nur die Links-Rechts-Bewegung der Nadel kontrolliert.
- Doppelte Discs sind etwas höher und verfügen über zwei Kränze. Dabei regelt einer weiterhin die Links-Rechts-Bewegung der Nadel, die andere regelt die Vor- und Zurück-Bewegung.

In jedem Fall gibt es mehrere Stufen, die durch unterschiedlich weit heraus ragende Aussenzähne abgebildet werden. (Grosser Ausschlag == grosse Wirkung.)

## Abmessungen

Die Discs bestehen aus einem dicken Innenring, welcher auf der unteren Seite angeschrägt ist, um richtig auf den Sockel in der Maschine zu passen.

![Der Innenring wird vermessen](/assets/images/snippet_images/content/der-innenring-wird-vermessen_2.jpeg "Der Innenring wird vermessen")

Auf der Unterseite der Disc findet sich ein Loch, in welches die Maschine einen Stift steckt, welcher die Disc festhält und dreht.

![Elna-Disc mit Transportloch](/assets/images/snippet_images/content/elna-disc-mit-transportloch_2.jpeg "Elna-Disc mit Transportloch")

![Elna-Lesemechanik mit Transportstift](/assets/images/snippet_images/content/elna-lesemechanik-mit-transportstift_2.jpeg "Elna-Lesemechanik mit Transportstift")

Der dicke Innenring hat einen Durchmesser von 3.4cm, welcher ein 1.7cm breites Loch genau in der Mitte hat. Auf diesem Ring sind dann Kränze mit Erhöhungen und Vertiefungen angebracht, welche von 0.2cm bis 0.5cm variieren können.

Die Anschrägung auf der Unterseite erfolgt in 2 Stufen. Zuerst einmal gibt es eine 1.5mm tiefe senkrechte Aussparung (zur Unterseite der Scheibe). Darauf folgt eine 45-Grad-Schräge, welche auf 1.5mm Tiefe die 1.5mm Differenz zum Innenrand des Loches wieder ausgleicht.

Das Transportloch ist ca. 4mm lang (vom Zentrum der Disc weg) und 3mm breit. Es ist 2.5mm vom Innenrand (also inklusive der 1.5mm-Schräge) entfernt. Das Loch ist 5.5mm tief und 3mm vom Aussenrand des Innenringes entfernt.

![Eine einfache Elna-Disc mit Links-Rechts-Bewegungsinformationen](/assets/images/snippet_images/content/eine-einfache-elna-disc-mit-links-rechts-bewegungsinformationen_2.jpeg "Eine einfache Elna-Disc mit Links-Rechts-Bewegungsinformationen")

Bei einfachen Discs beginnt der Kranz mit den Nadelpositionsinformationen 1mm über der Unterkante des Innenrings. Der Kranz ist 3.5mm breit, wodurch der Innenring lediglich 7mm gross sein muss. Oberhalb des Kranzes bleiben also noch 2.5mm ohne jegliche Informationen.

Die Höhe sollte jedoch trotzdem eingehalten werden, damit die Disc gut einrasten kann. Bei einer einfachen Umdrehung der Disc sticht die Nadel beginnend beim Transportloch insgesamt 18 mal regelmäßig ein.

![Eine einfache Elna-Disc, welche in die Maschine eingelegt wurde](/assets/images/snippet_images/content/eine-einfache-elna-disc-welche-in-die-maschine-eingelegt-wurde_2.jpeg "Eine einfache Elna-Disc, welche in die Maschine eingelegt wurde")

![Eine selbst gebaute Elna-Disc liegt in der Maschine](/assets/images/snippet_images/content/eine-selbst-gebaute-elna-disc-liegt-in-der-maschine_2.jpeg "Eine selbst gebaute Elna-Disc liegt in der Maschine")

![Diese Naht wurde mit der Eigenbau-Disc erstellt](/assets/images/snippet_images/content/diese-naht-wurde-mit-der-eigenbau-disc-erstellt_2.jpeg "Diese Naht wurde mit der Eigenbau-Disc erstellt")

Die doppelten Discs sind 9mm gross. Darauf sind zwei 3mm breite Kränze angebracht, welche 1mm voneinander entfernt sind und jeweils 1mm Abstand zum oberen bzw. unteren Rand der Scheibe haben.

![Elna-Disc mit zweiter Spur zur Einstellung der Geschwindigkeit](/assets/images/snippet_images/content/elna-disc-mit-zweiter-spur-zur-einstellung-der-geschwindigkeit_2.jpeg "Elna-Disc mit zweiter Spur zur Einstellung der Geschwindigkeit")

## Auswirkungen von Einstellungen

Der Hebel, welcher die Stichbreite einstellt, bewirkt, dass die Informationen auf der Disc beim Abtasten stärkere Variationen der Nadel auslösen. Eine Einstellung von 0 bewirkt dementsprechend, dass die Nadel unabhängig von der Struktur der Disc geradeaus näht.

Der Einstellhebel zur Stichlänge hat lediglich Einfluss auf den Transport des Stoffes und nicht direkt auf die Disc.

# Discs selber herstellen

Mit einem 3D-Drucker mit 0.3mm-Nozzle kann man recht akzeptable Elna-Programmdiscs selbst herstellen. Das Problem dabei ist, dass der Ablesemechanismus der Elna-Maschine bereits geringste Materialschwankungen als Abweichung in der Naht verewigt, weshalb eine 0.5mm-Nozzle nicht ausreicht.

Als Material empfiehlt sich PLA, da es weich genug ist, dass es auch bei den Umdrehungen in der Maschine nicht zerspringt. Die Disc kann allerdings im Betrieb relativ schnell verformt und abgenutzt werden.

Daher käme ABS eigentlich als Material in Betracht; aufgrund der grossen Gefahr, dass die Disc im Betrieb zersplittert, haben wir jedoch noch keinerlei Experimente in diese Richtung durchgeführt.

In unserem [Elna-Disc-Repository](http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary "http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary") haben wir einige 3D-Modelle zusammengestellt, welche mit Hilfe des 3D-Druckers gedruckt werden können; dort finden sich sowohl Basisdiscs ohne weitere Informationen als auch Discs mit Zickzackmustern und dergleichen.

# Resourcen

- [Elna-Supermatic-Musterdiscs: der aktuelle Stand](http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks.html "http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks.html")
- [Auflistung aller discs ohne Fotos](http://whitesewingcenter.com/elnaparts.php "http://whitesewingcenter.com/elnaparts.php")
- [OpenSCAD user manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual "https://en.wikibooks.org/wiki/OpenSCAD_User_Manual")
- Git-Repository: _git clone http://git.ancient-solutions.com/starship-factory/elna-discs.git_
- [Git-Webinterface](http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary "http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary")
