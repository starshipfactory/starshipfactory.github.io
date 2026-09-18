---
title: "Making ELNA Supermatic pattern discs yourself"
date: 2013-10-09
slug: "making-elna-supermatic-pattern-discs-yourself"
translationKey: "elna-supermatic-musterdisc-selber-herstellen"
categories:
  - "3D printing"
tags:
  - "3d-printing"
  - "sewing"
---
In one of our projects we are trying to make discs for ELNA sewing machines ourselves on the
3D printer. To do that we first have to understand how the discs work, and be able to reduce
them to a model ourselves.

This article explains the current progress in analysing and making the Elna discs. The
[current state](http://wiki.starship-factory.ch/Projekte/ELNA-Musterdisks/) can always be
found in our [wiki](http://wiki.starship-factory.ch/).

## Basic discs

![Many different Elna discs](/img/blog/viele-verschiedene-elna-discs_2.jpeg "Many different Elna discs")

For the ELNA Supermatic machines from the 1950s there are mainly 2 kinds of disc:

- Simple discs are fairly flat and have only an outer ring. The feed speed is constant and
  only the left-right movement of the needle is controlled.
- Double discs are somewhat taller and have two rings. One still controls the left-right
  movement of the needle, the other controls the forward and backward movement.

In both cases there are several levels, represented by outer teeth protruding by different
amounts. (Large deflection == large effect.)

### Dimensions

The discs consist of a thick inner ring, chamfered on the underside so that it fits properly
onto the base in the machine.

![Measuring the inner ring](/img/blog/der-innenring-wird-vermessen_2.jpeg "Measuring the inner ring")

On the underside of the disc there is a hole into which the machine puts a pin that holds the
disc and turns it.

![Elna disc with drive hole](/img/blog/elna-disc-mit-transportloch_2.jpeg "Elna disc with drive hole")

![Elna reading mechanism with drive pin](/img/blog/elna-lesemechanik-mit-transportstift_2.jpeg "Elna reading mechanism with drive pin")

The thick inner ring has a diameter of 3.4 cm, with a 1.7 cm wide hole exactly in the middle.
On this ring there are then rings with raised and lowered sections, which can vary from 0.2 cm
to 0.5 cm.

The chamfer on the underside is in 2 steps. First there is a 1.5 mm deep vertical recess
(towards the underside of the disc). That is followed by a 45-degree chamfer which, over
1.5 mm of depth, makes up the 1.5 mm difference to the inner edge of the hole.

The drive hole is about 4 mm long (measured away from the centre of the disc) and 3 mm wide.
It is 2.5 mm from the inner edge (including the 1.5 mm chamfer). The hole is 5.5 mm deep and
3 mm from the outer edge of the inner ring.

![A simple Elna disc with left-right movement information](/img/blog/eine-einfache-elna-disc-mit-links-rechts-bewegungsinformationen_2.jpeg "A simple Elna disc with left-right movement information")

On simple discs, the ring carrying the needle position information starts 1 mm above the lower
edge of the inner ring. The ring is 3.5 mm wide, so the inner ring only needs to be 7 mm. That
leaves 2.5 mm above the ring without any information.

The height should be kept to nonetheless, so that the disc engages properly. In one full
rotation of the disc the needle makes 18 evenly spaced stitches, starting at the drive hole.

![A simple Elna disc inserted into the machine](/img/blog/eine-einfache-elna-disc-welche-in-die-maschine-eingelegt-wurde_2.jpeg "A simple Elna disc inserted into the machine")

![A self-built Elna disc sitting in the machine](/img/blog/eine-selbst-gebaute-elna-disc-liegt-in-der-maschine_2.jpeg "A self-built Elna disc sitting in the machine")

![This seam was made with the home-made disc](/img/blog/diese-naht-wurde-mit-der-eigenbau-disc-erstellt_2.jpeg "This seam was made with the home-made disc")

The double discs are 9 mm tall. They carry two 3 mm wide rings, 1 mm apart, each 1 mm from the
upper and lower edge of the disc respectively.

![Elna disc with a second track for setting the speed](/img/blog/elna-disc-mit-zweiter-spur-zur-einstellung-der-geschwindigkeit_2.jpeg "Elna disc with a second track for setting the speed")

### Effects of the settings

The lever that sets the stitch width causes the information on the disc to produce larger
variations of the needle when it is read. A setting of 0 accordingly makes the needle sew
straight ahead regardless of the structure of the disc.

The stitch length lever only affects the feed of the fabric and not the disc directly.

## Making discs yourself

With a 3D printer with a 0.3 mm nozzle you can make quite acceptable Elna program discs
yourself. The problem is that the Elna machine's reading mechanism immortalises even the
slightest variation in material as a deviation in the seam, which is why a 0.5 mm nozzle is
not good enough.
