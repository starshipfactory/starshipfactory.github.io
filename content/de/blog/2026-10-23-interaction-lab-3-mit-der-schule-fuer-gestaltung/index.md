---
title: "Interaction Lab 3: Die Schule für Gestaltung Basel tüftelt bei uns"
description: "Vier Wochenenden lang haben Studierende der HF Interaction Design der Schule für Gestaltung Basel in der Starship Factory gelernt, Interfaces jenseits des Bildschirms zu bauen: mit Microcontrollern, KI-Agenten, 3D-Druck, Synthesizern und einer Design Challenge."
date: 2026-10-23
author: "starshipfactory"
slug: "interaction-lab-3-sfg-basel"
translationKey: "interaction-lab-3"
images:
  - "/img/blog/interaction-lab-3-feather-sense.jpg"
categories:
  - "Veranstaltungen"
  - "Elektronik"
tags:
  - "workshop"
  - "bildung"
  - "interaction-design"
  - "arduino"
  - "3d-druck"
  - "synthesizer"
---

Vier Wochenenden lang war die Starship Factory Klassenzimmer: Die Studierenden der HF Interaction Design der
Schule für Gestaltung Basel haben bei uns ihr Praxismodul *Interaction Lab 3* absolviert. Das Ziel: Interfaces
entwerfen und bauen, die nicht auf einem Bildschirm enden.
<!--more-->
![Ein Adafruit Feather nRF52840 Sense auf einem Holztisch, die Rückseite mit der Liste der eingebauten Sensoren nach oben](/img/blog/interaction-lab-3-feather-sense.jpg "Das Board, das durch den Kurs führte: der Adafruit Feather nRF52840 Sense")

## Warum ein Makerspace als Lernort?

Interaction Designer:innen gestalten heute längst nicht mehr nur Apps und Webseiten. Bedienelemente im Auto, an
der Ladestation, im Spital oder am Möbelstück verlangen ein Verständnis dafür, wie Software, Elektronik und
Material zusammenspielen. Das Modul *Angewandte Technologien* der Schule soll genau dieses Verständnis aufbauen:
Wer weiss, wie sich eine Idee technisch umsetzen lässt, entwirft von Anfang an bessere Lösungen.

Das Interaction Lab 3 war deshalb bewusst als experimentelles *Tinkering Lab* angelegt, in Kooperation mit uns. Die
Lernziele:

- physische und alternative Schnittstellen konzipieren und gestalten,
- Sensoren, Aktoren und Microcontroller experimentell einsetzen,
- Hardware- und Software-Werkzeuge für funktionierende Prototypen anwenden,
- eigene Ideen durch Tüfteln iterativ erproben und weiterentwickeln.

Die Werkstatt lieferte dafür, was ein Schulzimmer nicht hat: Lötstationen, Bauteile, 3D-Drucker und eine Crew, die
gerne erklärt. Pat Mächler eröffnete den Kurs mit dem Leitsatz, der über allem stand: *«I hear and I forget. I see
and I remember. I do and I understand.»*

Jedes Modul lief über einen Freitag und einen Samstag. In mehreren Modulen kam dasselbe Board zum Einsatz, der
[Adafruit Feather nRF52840 Sense](https://learn.adafruit.com/adafruit-feather-sense): ein Microcontroller mit
Bluetooth, Beschleunigungssensor, Gyroskop, Magnetometer, Licht-, Gesten- und Näherungssensor, Mikrofon sowie
Temperatur-, Druck- und Feuchtigkeitsmessung. Ein einziges Board, an dem sich fast jede Art von Interaktion
ausprobieren lässt.

## Modul 1: Playful Interfaces

George Cave von [Interaction Magic](https://interactionmagic.com/) baut beruflich Prototypen für die Bedienung von
Motorrädern, Autos und Ladestationen. Seine Kernbotschaft: Designer:innen prototypen meist digital und kaum physisch.
Diese beiden Welten sollen sich überlappen.

Der Einstieg dazu war verblüffend einfach: **Alles ist eine Tastatur.** Ein Microcontroller kann sich gegenüber dem
Computer als USB-Tastatur ausgeben. Ein Taster am Board tippt dann einen Buchstaben, und Figma kann auf genau diesen
Tastendruck reagieren. So steuert ein selbst gebautes Bedienelement einen Klick-Dummy, etwa das Dashboard eines Autos
oder den Bildschirm einer Ladestation. Hardware und UI lassen sich damit gemeinsam testen, lange bevor irgendetwas
produziert wird.

![Eine Hand hält einen gelben Taster, der über Krokodilklemmen mit dem Board neben einem Laptop verbunden ist](/img/blog/interaction-lab-3-taster.jpg "Ein Taster, zwei Krokodilklemmen und ein Board: fertig ist die eigene Tastatur")

Dazu gab es eine Lektion, die jede:r nur einmal lernen will: Ein Programm, das ununterbrochen Tasten drückt, kann den
eigenen Laptop lahmlegen. Deshalb gehört in jedes Programm ein Sicherheits-Stopp, ein Pin, der das Programm beim
Start anhält.

Danach ging es weiter mit kabelloser Kommunikation. Die Studierenden verglichen WLAN, Bluetooth, LoRa und Mobilfunk
nach Reichweite, Stromverbrauch und Aufwand und bauten eine Bluetooth-Tastatur. Damit entstand eine
*Wizard-of-Oz*-Jukebox: Ein Objekt, das scheinbar selbst Musik abspielt, in Wahrheit aber Spotify auf dem Laptop
fernsteuert. Den Abschluss bildeten Game-Controller, die per Schütteln, Neigen oder Schreien ein Computerspiel
bedienen.

## Modul 2: KI-Agenten und 3D-Druck

Antonio Lamb aus der Starship-Crew verband das Programmieren mit KI-Agenten mit digitaler Fertigung. Zuerst die Begriffe:
Das Sprachmodell ist der Motor, das *Harness* (hier das Open-Source-Werkzeug [opencode](https://opencode.ai/)) lenkt
ihn und gibt ihm Werkzeuge in die Hand. Beides zusammen ist der Agent.

Der wichtigste Lerninhalt war aber kein technischer: **Das eigene Verständnis bleibt der Engpass.** Je besser Agenten
sich selbst korrigieren, desto verlockender ist es, aus der Schleife auszusteigen. Wer aber nicht mehr versteht, was
entsteht, kann Fehler weder kommen sehen noch beheben, und die technischen Schulden wachsen. «Einfach weiter
vibe-coden, wir können es später immer noch reparieren» ist kein Plan.

![Zwei violette, 3D-gedruckte Gehäusehälften auf dem Druckbett eines 3D-Druckers](/img/blog/interaction-lab-3-controller-gehaeuse.jpg "Frisch gedruckt: Ober- und Unterschale eines Controllers")

Am Freitag programmierten die Studierenden mit dem Agenten ihr eigenes Browserspiel. Dann gestalteten sie in einem
Editor das Gehäuse für einen Controller mit sechs Tasten. Die Tastenanordnung legten sie von Hand fest,
Formänderungen beschrieben sie dem Sprachmodell in eigenen Worten. Dabei lernten sie, wie man einer KI Leitplanken
setzt: Jeder Vorschlag wird von der Software geprüft, ob er druckbar ist und Elektronik, USB-Öffnung und
Schnappverschlüsse frei lässt. Erst dann wird daraus mit [build123d](https://github.com/gumyr/build123d) ein 3D-Modell.
Im Slicer bereiteten sie die Dateien für den Druck vor, und die Gehäuse wurden über Nacht gedruckt.

Am Samstag wurde verdrahtet, die Firmware in CircuitPython aufgespielt, zusammengebaut und gespielt. Als
Gestaltungsprinzipien für den Controller standen *Mapping*, *Affordance* und das *Fitts'sche Gesetz* im Zentrum. Das
Workshop-Material liegt offen auf
[GitHub](https://github.com/antomicblitz/hf-game-controller-workshop).

## Modul 3: Sound Interfaces

Robin Michel, ebenfalls aus der Starship-Crew, brachte Klang in die Werkstatt. Den Anfang machte eine kurze Geschichte der elektronischen Musik, vom
Theremin der 1920er-Jahre über Trautonium, Ondes Martenot und die Radiostudios bis zum ersten Moog-Synthesizer, Wendy
Carlos' *Switched-On Bach* und dem ersten Computer-Musikinstrument Fairlight CMI.

![Ein Tisch voller Synthesizer, Drum-Computer und Kabel, dahinter wird ein Gerät verkabelt](/img/blog/interaction-lab-3-synthesizer.jpg "Der Synthesizer-Tisch: Hier wird Klang zur Interaktion")

Danach wurde es praktisch: Field Recording, einen MIDI-Controller selbst löten, Synthesizer ausprobieren. Theoretisch
ging es um subtraktive Synthese und um die Grundbausteine des Sounddesigns: Rauschanteil, harmonische und
unharmonische Obertöne, der Unterschied zwischen Ton und Geräusch. Die zentrale Frage fürs Interaction Design war das
*Mapping*: Welche Geste, welcher Regler, welcher Sensor steuert welchen Klangparameter? Am Samstag kamen Sampling dazu
und eine eigene Kompositionsskizze in einer DAW. Wer weitermachen will, findet kostenlose Werkzeuge wie
[VCV Rack](https://vcvrack.com/), [plugdata](https://plugdata.org/) oder [SuperCollider](https://supercollider.github.io/).

## Modul 4: Die Design Challenge

Zum Abschluss stellten Pat Mächler und Peter Hess (Industrial Designer bei HKT Design) eine Aufgabe, die alles
zusammenführte: **Wie können wir Alltagsgegenstände einer Möbelmarke mit Interaktion bespielen?** Peter gab dazu eine
Haltung aus seinem Alltag im Medizinaldesign mit: *Human Centered Design*. Der Mensch steht im Zentrum, der Prozess ist
iterativ, und Feedback von Nutzenden treibt die Verbesserung an. Und: Vertrauen in den Prozess.

![Skizzenblätter liegen auf einem Tisch verteilt, zwei Personen ordnen und besprechen sie](/img/blog/interaction-lab-3-crazy-8s.jpg "Nach den Crazy 8s werden die Ideen geclustert")

Der Freitag folgte einem kompakten Design-Sprint:

1. **Ideen allein entwickeln.** Mit der Methode *Crazy 8s* skizziert jede Person acht Ideen in acht Minuten.
   Masse vor Perfektion, damit man über die naheliegenden ersten Einfälle hinauskommt.
2. **Gemeinsam entscheiden.** Im Team werden die Skizzen vorgestellt, gruppiert und anhand klarer Kriterien auf drei
   Ideen verdichtet: Potenzial des Konzepts, Beitrag zum Ziel und Freude an der Umsetzung.
3. **Schnell testen.** Die drei Ideen werden als *Wizard-of-Oz*-Prototypen gebaut, bei denen ein Mensch hinter den
   Kulissen die Technik simuliert, und mit Nutzenden getestet. Dann fällt die Entscheidung für ein Konzept.
4. **Ausarbeiten.** Das gewählte Konzept wird mit Arduino und Sensorik zum funktionierenden Prototypen.

Die Methodik dahinter: Ideen entstehen am besten in Einzelarbeit, weil sich Meinungen in der Gruppe schnell angleichen
und ungewöhnliche Ansätze verloren gehen. Austausch, Kritik und Entscheidung gehören dagegen ins Team. Als
Inspiration für die Technik gab es einen Input zum Smart Mirror, einem halbdurchlässigen Spiegel, hinter dem ein
Display leuchtet.

Am Samstag folgten eine zweite Testrunde, eine letzte Iteration und die Präsentation der Konzepte als Geschichte.
Zum Schluss gab es ein gemeinsames Grillfest.

## Auch die Umwege zählen

Ein Grundsatz zog sich durch alle Module: Dokumentiert wird nicht nur das Ergebnis, sondern der Weg dorthin. Die
Studierenden hielten Ausgangsidee, eingesetzte Technik und wichtigste Erkenntnisse laufend in Bild, Video und kurzen
Texten fest, ausdrücklich auch Fehlversuche und Umwege. Genau so funktioniert ein Makerspace: Man lernt am meisten
aus dem, was beim ersten Mal nicht klappt.

## Danke

Ein grosses Dankeschön an das Modul-Team: Daniel Hunziker und Mario Giudici von [associes.ch](https://associes.ch/),
Pat Mächler, Peter Hess, George Cave, Antonio Lamb und Robin Michel. Und an die Studierenden, die vier Wochenenden
lang unsere Werkstatt mit Leben gefüllt haben. Wir haben uns über jede Lötstelle, jeden gedruckten Controller und
jeden schrägen Synthesizer-Ton gefreut.

Lust bekommen, selbst zu tüfteln? Komm an einem unserer offenen Abende vorbei, dienstags und freitags ab 19:30 Uhr,
oder [werde Mitglied](/mitglied-werden/). Du planst als Schule oder Firma einen Kurs mit Werkstatt-Anteil? Melde
dich in unserem [Forum](https://discourse.starship-factory.ch/), wir freuen uns darauf.
