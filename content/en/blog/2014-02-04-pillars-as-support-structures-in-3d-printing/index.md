---
title: "Pillars as support structures in 3D printing"
date: 2014-02-04
slug: "pillars-as-support-structures-in-3d-printing"
translationKey: "saeulen-als0stuetzstruktur-im-3d-druck"
categories:
  - "3D printing"
tags:
  - "3d-printing"
  - "support-structure"
  - "process"
---
In 3D printing, objects are usually created by laying several layers of plastic on top of one
another, as with a hot glue gun. That works excellently for objects with a cube- or
pyramid-like shape, but when the object has more than just overhangs (bridges between
sub-objects and so on), it can become necessary to build in support structures. These are
often generated automatically by 3D slicer programs such as Cura or slic3r. They are less
pronounced plastic structures which cannot take much pressure (unlike the structures belonging
to the object itself), but offer enough purchase for the printer's plastic threads to hold on
to, making the object printable.

For many projects the automatically generated support structures are already usable. However,
the support blocks or diamond structures normally generated require a fair amount of plastic
and print time.

This is the problem the [software supplied with the B9Creator UV printer](http://b9creator.com/software/)
tackles: instead of a grid of squares, it prints pillars, which take up less time and plastic.
Since a certain degree of overhang is acceptable in 3D printing, these pillars can be printed
in practically any orientation and hold the 3D object together.

![The B9Creator software generates pillars instead of the usual diamond support structures, to make objects printable that are not connected at the lower end.](/img/blog/die-software-des-b9creator-erzeugt-saulen-statt-der-herkommlichen-rauten-supportstrukturen-um-objekte-druckbar-zu-machen-welche-am-unteren-ende-nicht-zusammen-hangen_2.png "The B9Creator software generates pillars instead of the usual diamond support structures, to make objects printable that are not connected at the lower end.")

The B9Creator software generates pillars instead of the usual diamond support structures, to
make objects printable that are not connected at the lower end.

As you can easily see here, it is also much easier after the print to separate the generated
support structures (the pillars here) from the object itself, since unlike attached diamond
structures they have only a very small contact area.

Another piece of software that uses this technique is [Meshmixer](http://www.meshmixer.com/).
It will probably find its way into the rest of the 3D printing software before long, though.
