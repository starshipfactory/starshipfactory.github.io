---
title: "Fabriquer soi-même des disques à motifs ELNA Supermatic"
date: 2013-10-09
slug: "fabriquer-soi-meme-des-disques-elna-supermatic"
translationKey: "elna-supermatic-musterdisc-selber-herstellen"
categories:
  - "Impression 3D"
tags:
  - "impression-3d"
  - "couture"
---

Dans le cadre d'un projet, nous essayons de fabriquer nous-mêmes à l'imprimante 3D des disques pour machines à coudre ELNA. Pour cela, il faut d'abord comprendre le fonctionnement des disques et pouvoir les ramener nous-mêmes à un modèle.

Cet article explique les progrès actuels de l'analyse et de la fabrication des disques Elna. [L'état actuel](http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks/ "http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks.html") se trouve à chaque fois dans notre [wiki](http://wiki.starship-factory.ch/ "http://wiki.starship-factory.ch/").

## Disques de base

![De nombreux disques Elna différents](/img/blog/viele-verschiedene-elna-discs_2.jpeg "De nombreux disques Elna différents")

Pour les machines ELNA Supermatic des années 50, il existe principalement 2 types de disques :

- Les disques simples sont assez plats et n'ont qu'une couronne extérieure. La vitesse d'entraînement est alors constante et seul le mouvement gauche-droite de l'aiguille est contrôlé.
- Les disques doubles sont un peu plus hauts et disposent de deux couronnes. L'une règle toujours le mouvement gauche-droite de l'aiguille, l'autre règle le mouvement avant-arrière.

Dans tous les cas, il y a plusieurs niveaux, représentés par des dents extérieures qui dépassent plus ou moins loin. (Grand débattement == grand effet.)

### Dimensions

Les disques se composent d'un épais anneau intérieur, biseauté sur la face inférieure afin de s'adapter correctement au socle dans la machine.

![L'anneau intérieur est mesuré](/img/blog/der-innenring-wird-vermessen_2.jpeg "L'anneau intérieur est mesuré")

Sur la face inférieure du disque se trouve un trou dans lequel la machine introduit une tige, qui maintient le disque et le fait tourner.

![Disque Elna avec trou d'entraînement](/img/blog/elna-disc-mit-transportloch_2.jpeg "Disque Elna avec trou d'entraînement")

![Mécanisme de lecture Elna avec tige d'entraînement](/img/blog/elna-lesemechanik-mit-transportstift_2.jpeg "Mécanisme de lecture Elna avec tige d'entraînement")

L'épais anneau intérieur a un diamètre de 3,4 cm, avec un trou de 1,7 cm de large exactement au milieu. Sur cet anneau sont ensuite disposées des couronnes comportant des bosses et des creux, qui peuvent varier de 0,2 cm à 0,5 cm.

Le biseau sur la face inférieure se fait en 2 étapes. Il y a d'abord un évidement vertical de 1,5 mm de profondeur (vers la face inférieure du disque). Vient ensuite un biseau à 45 degrés, qui compense sur 1,5 mm de profondeur la différence de 1,5 mm par rapport au bord intérieur du trou.

Le trou d'entraînement mesure env. 4 mm de long (en s'éloignant du centre du disque) et 3 mm de large. Il est à 2,5 mm du bord intérieur (donc y compris le biseau de 1,5 mm). Le trou a 5,5 mm de profondeur et se trouve à 3 mm du bord extérieur de l'anneau intérieur.

![Un disque Elna simple avec les informations de mouvement gauche-droite](/img/blog/eine-einfache-elna-disc-mit-links-rechts-bewegungsinformationen_2.jpeg "Un disque Elna simple avec les informations de mouvement gauche-droite")

Sur les disques simples, la couronne portant les informations de position de l'aiguille commence 1 mm au-dessus du bord inférieur de l'anneau intérieur. La couronne est large de 3,5 mm, ce qui fait que l'anneau intérieur ne doit mesurer que 7 mm. Au-dessus de la couronne, il reste donc encore 2,5 mm sans aucune information.

La hauteur devrait toutefois être respectée malgré tout, pour que le disque puisse bien s'enclencher. Lors d'un tour complet du disque, l'aiguille pique régulièrement 18 fois au total, en commençant au trou d'entraînement.

![Un disque Elna simple, mis en place dans la machine](/img/blog/eine-einfache-elna-disc-welche-in-die-maschine-eingelegt-wurde_2.jpeg "Un disque Elna simple, mis en place dans la machine")

![Un disque Elna fabriqué maison se trouve dans la machine](/img/blog/eine-selbst-gebaute-elna-disc-liegt-in-der-maschine_2.jpeg "Un disque Elna fabriqué maison se trouve dans la machine")

![Cette couture a été réalisée avec le disque fait maison](/img/blog/diese-naht-wurde-mit-der-eigenbau-disc-erstellt_2.jpeg "Cette couture a été réalisée avec le disque fait maison")

Les disques doubles mesurent 9 mm. Deux couronnes de 3 mm de large y sont disposées, éloignées de 1 mm l'une de l'autre et à 1 mm du bord supérieur, respectivement inférieur, du disque.

![Disque Elna avec une deuxième piste pour le réglage de la vitesse](/img/blog/elna-disc-mit-zweiter-spur-zur-einstellung-der-geschwindigkeit_2.jpeg "Disque Elna avec une deuxième piste pour le réglage de la vitesse")

### Effets des réglages

Le levier qui règle la largeur de point fait que les informations du disque provoquent, lors de la lecture, des variations plus fortes de l'aiguille. Un réglage sur 0 a donc pour effet que l'aiguille coud droit, indépendamment de la structure du disque.

Le levier de réglage de la longueur de point n'influence que l'entraînement du tissu et pas directement le disque.

## Fabriquer soi-même des disques

Avec une imprimante 3D à buse de 0,3 mm, on peut fabriquer soi-même des disques de programme Elna tout à fait acceptables. Le problème est que le mécanisme de lecture de la machine Elna immortalise dans la couture, sous forme d'écart, les moindres variations de matière, raison pour laquelle une buse de 0,5 mm ne suffit pas.

Comme matériau, le PLA est recommandé, car il est assez souple pour ne pas éclater malgré les rotations dans la machine. Le disque peut toutefois se déformer et s'user assez vite à l'usage.

C'est pourquoi l'ABS entrerait en fait en ligne de compte comme matériau ; en raison du grand risque que le disque éclate en service, nous n'avons toutefois encore mené aucune expérience dans cette direction.

Dans notre [dépôt de disques Elna](http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary "http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary"), nous avons rassemblé quelques modèles 3D qui peuvent être imprimés à l'aide de l'imprimante 3D ; on y trouve aussi bien des disques de base sans autre information que des disques avec motifs en zigzag et similaires.

## Ressources

- [Disques à motifs Elna Supermatic : l'état actuel](http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks.html "http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks.html")
- [Liste de tous les disques sans photos](http://whitesewingcenter.com/elnaparts.php "http://whitesewingcenter.com/elnaparts.php")
- [OpenSCAD user manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual "https://en.wikibooks.org/wiki/OpenSCAD_User_Manual")
- Dépôt Git : _git clone http://git.ancient-solutions.com/starship-factory/elna-discs.git_
- [Interface web Git](http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary "http://git.ancient-solutions.com/cgi-bin/gitweb.cgi?p=starship-factory/elna-discs.git;a=summary")
