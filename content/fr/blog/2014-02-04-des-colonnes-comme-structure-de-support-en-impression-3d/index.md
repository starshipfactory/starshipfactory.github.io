---
title: "Des colonnes comme structure de support en impression 3D"
date: 2014-02-04
slug: "des-colonnes-comme-structure-de-support-en-impression-3d"
translationKey: "saeulen-als0stuetzstruktur-im-3d-druck"
categories:
  - "Impression 3D"
tags:
  - "impression-3d"
  - "structure-support"
  - "procede"
---

En impression 3D, les objets sont habituellement créés en déposant plusieurs couches de plastique les unes sur les autres, comme avec un pistolet à colle chaude. Cela fonctionne à merveille pour les objets qui ont une forme proche du cube ou de la pyramide, mais lorsque l'objet comporte plus que de simples saillies (des ponts entre sous-objets, etc.), il peut devenir nécessaire d'intégrer des structures de support. Celles-ci sont souvent créées automatiquement par les logiciels de tranchage 3D comme par ex. Cura ou slic3r. Il s'agit de structures en plastique moins marquées, qui ne supportent pas beaucoup de pression (contrairement aux structures appartenant à l'objet), mais offrent assez de maintien pour que les fils de plastique de l'imprimante puissent y tenir et que l'objet devienne imprimable.

Avec les structures de support générées automatiquement, on peut déjà travailler utilement sur beaucoup de projets. Les blocs de support ou les structures en losange normalement générés nécessitent toutefois relativement beaucoup de plastique et aussi de temps d'impression.

C'est sur cette problématique qu'intervient le [logiciel livré avec l'imprimante UV B9Creator](http://b9creator.com/software/ "http://b9creator.com/software/") : au lieu d'une trame de quadrilatères, ce sont ici des colonnes qui sont imprimées, lesquelles prennent moins de temps et de plastique. Comme une certaine quantité de porte-à-faux est acceptable en impression 3D, ces colonnes peuvent être imprimées pratiquement dans n'importe quelle orientation et maintenir l'objet 3D.

![Le logiciel du b9creator génère des colonnes au lieu des structures de support en losange classiques, afin de rendre imprimables des objets qui ne sont pas solidaires à leur extrémité inférieure.](/img/blog/die-software-des-b9creator-erzeugt-saulen-statt-der-herkommlichen-rauten-supportstrukturen-um-objekte-druckbar-zu-machen-welche-am-unteren-ende-nicht-zusammen-hangen_2.png "Le logiciel du b9creator génère des colonnes au lieu des structures de support en losange classiques, afin de rendre imprimables des objets qui ne sont pas solidaires à leur extrémité inférieure.")

Le logiciel du b9creator génère des colonnes au lieu des structures de support en losange classiques, afin de rendre imprimables des objets qui ne sont pas solidaires à leur extrémité inférieure.

  

Comme on peut facilement le constater ici, il est aussi beaucoup plus simple, après l'impression, de séparer de l'objet proprement dit les structures de support générées (ici les colonnes), car elles n'ont, contrairement par exemple aux structures en losange accolées, qu'une très petite surface de contact.

Un autre logiciel qui applique cette technique est [Meshmixer](http://www.meshmixer.com/). Il est toutefois probable qu'elle trouvera bientôt aussi son application dans le reste des logiciels d'impression 3D.
