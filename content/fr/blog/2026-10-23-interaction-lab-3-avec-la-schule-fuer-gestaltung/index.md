---
title: "Interaction Lab 3 : la Schule für Gestaltung Basel bricole chez nous"
description: "Pendant quatre week-ends, des étudiant·e·s en design d’interaction de la Schule für Gestaltung Basel ont appris à la Starship Factory à construire des interfaces au-delà de l’écran : avec des microcontrôleurs, des agents d’IA, l’impression 3D, des synthétiseurs et un défi de design."
date: 2026-10-23
author: "starshipfactory"
slug: "interaction-lab-3-sfg-basel"
translationKey: "interaction-lab-3"
images:
  - "/img/blog/interaction-lab-3-feather-sense.jpg"
categories:
  - "Événements"
  - "Électronique"
tags:
  - "atelier"
  - "formation"
  - "design-interaction"
  - "arduino"
  - "impression-3d"
  - "synthetiseur"
---

Pendant quatre week-ends, la Starship Factory s’est transformée en salle de classe : les étudiant·e·s de la filière
HF Interaction Design de la Schule für Gestaltung Basel (une école supérieure de design à Bâle) ont suivi chez nous
leur module pratique *Interaction Lab 3*. L’objectif : concevoir et construire des interfaces qui ne s’arrêtent pas à
un écran.
<!--more-->
![Un Adafruit Feather nRF52840 Sense posé sur une table en bois, face arrière visible avec la liste des capteurs intégrés](/img/blog/interaction-lab-3-feather-sense.jpg "La carte qui a accompagné tout le cours : l’Adafruit Feather nRF52840 Sense")

## Pourquoi un makerspace comme lieu d’apprentissage ?

Les designers d’interaction ne conçoivent plus depuis longtemps que des applis et des sites web. Les commandes d’une
voiture, d’une borne de recharge, d’un hôpital ou d’un meuble exigent de comprendre comment logiciel, électronique et
matière fonctionnent ensemble. Le module *Technologies appliquées* de l’école vise précisément à construire cette
compréhension : quand on sait comment une idée peut être réalisée techniquement, on conçoit de meilleures solutions
dès le départ.

C’est pourquoi l’Interaction Lab 3 a été pensé délibérément comme un *tinkering lab* expérimental, en coopération
avec nous. Les objectifs d’apprentissage :

- concevoir et façonner des interfaces physiques et alternatives,
- utiliser de manière expérimentale capteurs, actionneurs et microcontrôleurs,
- employer des outils matériels et logiciels pour réaliser des prototypes fonctionnels,
- tester ses propres idées de manière itérative en bricolant, et les faire évoluer.

L’atelier offrait ce qu’une salle de classe n’a pas : des stations de soudure, des composants, des imprimantes 3D et
une équipe qui aime expliquer. Pat Mächler a ouvert le cours avec la devise qui chapeautait tout : *« I hear and I
forget. I see and I remember. I do and I understand. »*

Chaque module se déroulait sur un vendredi et un samedi. Plusieurs modules utilisaient la même carte,
l’[Adafruit Feather nRF52840 Sense](https://learn.adafruit.com/adafruit-feather-sense) : un microcontrôleur avec
Bluetooth, accéléromètre, gyroscope, magnétomètre, capteur de lumière, de gestes et de proximité, microphone, ainsi
que des mesures de température, de pression et d’humidité. Une seule carte pour tester presque tous les types
d’interaction.

## Module 1 : Playful Interfaces

George Cave, d’[Interaction Magic](https://interactionmagic.com/), construit professionnellement des prototypes pour
les commandes de motos, de voitures et de bornes de recharge. Son message principal : les designers prototypent
surtout en numérique et très peu en physique. Ces deux mondes devraient se recouper.

Le point de départ était d’une simplicité étonnante : **tout est un clavier.** Un microcontrôleur peut se présenter à
l’ordinateur comme un clavier USB. Un bouton sur la carte tape alors une lettre, et Figma peut réagir précisément à
cette touche. Ainsi, une commande faite maison pilote une maquette cliquable, par exemple le tableau de bord d’une
voiture ou l’écran d’une borne de recharge. Matériel et interface peuvent être testés ensemble bien avant que quoi que
ce soit ne soit produit.

![Une main tient un bouton-poussoir jaune relié par des pinces crocodile à la carte, à côté d’un ordinateur portable](/img/blog/interaction-lab-3-taster.jpg "Un bouton, deux pinces crocodile et une carte : voilà ton propre clavier")

Avec, une leçon qu’on ne veut apprendre qu’une seule fois : un programme qui appuie sans arrêt sur des touches peut
bloquer ton propre ordinateur. Chaque programme reçoit donc un arrêt de sécurité, une broche qui stoppe le programme
au démarrage.

Ensuite, place à la communication sans fil. Les étudiant·e·s ont comparé Wi-Fi, Bluetooth, LoRa et réseau mobile selon
la portée, la consommation et l’effort, et ont construit un clavier Bluetooth. Il en est sorti un juke-box
*Wizard-of-Oz* : un objet qui semble jouer de la musique tout seul, mais qui en réalité pilote Spotify à distance sur
l’ordinateur. Pour conclure, des manettes de jeu qui commandent un jeu vidéo en secouant, en inclinant ou en criant.

## Module 2 : agents d’IA et impression 3D

Antonio Lamb, de l’équipe Starship, a relié la programmation avec des agents d’IA et la fabrication numérique.
D’abord les notions : le modèle de langage est le moteur, le *harness* (ici l’outil open source
[opencode](https://opencode.ai/)) le guide et lui met des outils en main. Les deux ensemble forment l’agent.

L’enseignement le plus important n’était cependant pas technique : **ta propre compréhension reste le goulot
d’étranglement.** Plus les agents savent se corriger eux-mêmes, plus il est tentant de sortir de la boucle. Mais si tu
ne comprends plus ce qui se construit, tu ne peux ni voir venir les erreurs ni les corriger, et la dette technique
grandit. « Continuons à vibe-coder, on pourra toujours réparer plus tard » n’est pas un plan.

![Deux moitiés de boîtier violettes imprimées en 3D sur le plateau d’une imprimante 3D](/img/blog/interaction-lab-3-controller-gehaeuse.jpg "Tout juste imprimées : les coques supérieure et inférieure d’une manette")

Le vendredi, les étudiant·e·s ont programmé avec l’agent leur propre jeu pour navigateur. Puis ils et elles ont
conçu dans un éditeur le boîtier d’une manette à six boutons. La disposition des boutons se faisait à la main, les
modifications de forme étaient décrites au modèle de langage avec leurs propres mots. Ils et elles ont ainsi appris à
poser des garde-fous à une IA : le logiciel vérifie chaque proposition pour savoir si elle est imprimable et si elle
laisse libres l’électronique, l’ouverture USB et les clips. Ce n’est qu’ensuite que
[build123d](https://github.com/gumyr/build123d) en fait un modèle 3D. Les fichiers ont été préparés dans le slicer,
et les boîtiers imprimés pendant la nuit.

Le samedi, place au câblage, au flashage du firmware CircuitPython, à l’assemblage et au jeu. Les principes de design
de la manette étaient centrés sur le *mapping*, l’*affordance* et la *loi de Fitts*. Le matériel de l’atelier est
librement accessible sur [GitHub](https://github.com/antomicblitz/hf-game-controller-workshop).

## Module 3 : Sound Interfaces

Robin Michel, lui aussi de l’équipe Starship, a fait entrer le son dans l’atelier. Pour commencer, une brève histoire
de la musique électronique, du thérémine des années 1920 au premier synthétiseur Moog, en passant par le Trautonium,
les ondes Martenot et les studios de radio, jusqu’à *Switched-On Bach* de Wendy Carlos et au premier instrument de
musique informatique, le Fairlight CMI.

![Une table couverte de synthétiseurs, de boîtes à rythmes et de câbles, avec un appareil en cours de câblage à l’arrière](/img/blog/interaction-lab-3-synthesizer.jpg "La table des synthétiseurs : là où le son devient interaction")

Ensuite, place à la pratique : field recording, souder son propre contrôleur MIDI, essayer des synthétiseurs. Côté
théorie, il était question de synthèse soustractive et des éléments de base du sound design : la part de bruit, les
harmoniques et les partiels inharmoniques, la différence entre un son tonal et un bruit. La question centrale pour le
design d’interaction était le *mapping* : quel geste, quel potentiomètre, quel capteur contrôle quel paramètre sonore ?
Le samedi s’y sont ajoutés le sampling et une esquisse de composition personnelle dans une DAW. Pour continuer, il
existe des outils gratuits comme [VCV Rack](https://vcvrack.com/), [plugdata](https://plugdata.org/) ou
[SuperCollider](https://supercollider.github.io/).

## Module 4 : le défi de design

Pour conclure, Pat Mächler et Peter Hess (designer industriel chez HKT Design) ont posé une question qui réunissait
tout : **comment donner de l’interaction aux objets du quotidien d’une marque de meubles ?** Peter a transmis une
attitude issue de son quotidien dans le design médical : le *human-centred design*. L’humain est au centre, le
processus est itératif, et les retours des utilisateur·rice·s font avancer les améliorations. Et : faire confiance au
processus.

![Des feuilles d’esquisses étalées sur une table, deux personnes les trient et en discutent](/img/blog/interaction-lab-3-crazy-8s.jpg "Après les Crazy 8s, les idées sont regroupées")

Le vendredi a suivi un design sprint compact :

1. **Développer des idées seul·e.** Avec la méthode *Crazy 8s*, chaque personne esquisse huit idées en huit minutes.
   La quantité avant la perfection, pour dépasser les premières idées évidentes.
2. **Décider ensemble.** En équipe, les esquisses sont présentées, regroupées et réduites à trois idées selon des
   critères clairs : le potentiel du concept, sa contribution à l’objectif et le plaisir de le réaliser.
3. **Tester vite.** Les trois idées sont construites sous forme de prototypes *Wizard-of-Oz*, où une personne en
   coulisses simule la technique, et testées avec des utilisateur·rice·s. Puis l’équipe choisit un concept.
4. **Approfondir.** Le concept retenu devient un prototype fonctionnel avec Arduino et des capteurs.

La méthode derrière tout cela : les idées naissent le mieux en travail individuel, car en groupe les opinions
s’alignent vite et les approches inhabituelles se perdent. L’échange, la critique et la décision, en revanche,
appartiennent à l’équipe. Comme inspiration technique, il y a eu un apport sur le smart mirror, un miroir
semi-transparent derrière lequel brille un écran.

Le samedi ont suivi un deuxième tour de tests, une dernière itération et la présentation des concepts sous forme
d’histoire. Et pour finir, un barbecue tous ensemble.

## Les détours comptent aussi

Un principe a traversé tous les modules : on documente non seulement le résultat, mais aussi le chemin pour y
arriver. Les étudiant·e·s ont consigné au fil du cours leur idée de départ, la technique utilisée et leurs principaux
enseignements en images, en vidéo et en courts textes, y compris explicitement les échecs et les détours. C’est
exactement ainsi que fonctionne un makerspace : on apprend le plus de ce qui ne marche pas du premier coup.

## Merci

Un grand merci à l’équipe du module : Daniel Hunziker et Mario Giudici d’[associes.ch](https://associes.ch/),
Pat Mächler, Peter Hess, George Cave, Antonio Lamb et Robin Michel. Et aux étudiant·e·s qui ont fait vivre notre
atelier pendant quatre week-ends. Nous nous sommes réjouis de chaque soudure, de chaque manette imprimée et de chaque
son de synthétiseur un peu bizarre.

Envie de bricoler toi aussi ? Passe à l’une de nos soirées ouvertes, le mardi et le vendredi dès 19h30, ou
[deviens membre](/fr/devenir-membre/). Tu prépares, pour une école ou une entreprise, un cours avec une partie en
atelier ? Écris-nous sur notre [forum](https://discourse.starship-factory.ch/), on s’en réjouit.
