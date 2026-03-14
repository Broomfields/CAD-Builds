---
title: "Rocket Booster Bracket"
description: "Custom two-part motor mount designed to hold locally available boosters in a rocket chassis built for larger ones."
date: "2021-07-31"
cover: "02-model-cap"
cover_alt: "Bracket cap model — top view showing the booster retaining geometry"
gallery:
  - name: "01-model-study"
    label: "Bracket — Cap Study, recreating original booster cap as a model"
  - name: "02-model-cap"
    label: "Bracket — Cap, this braces the top of the boosters, and has a cap to hold them in the bracket"
  - name: "03-model-brace"
    label: "Bracket — Brace, this braces the bottom of the boosters and acts as the rocket base"
  - name: "04-rig"
    label: "Launch rig"
  - name: "05-rocket-base"
    label: "Rocket body"
  - name: "06-rocket"
    label: "Rocket assembled and ready"
tags: ["openscad", "3d-printing", "rocketry"]
cad_tool: "OpenSCAD"
status: "complete"
license: "CC BY-SA 4.0"
subpages:
  - "print-settings"
files:
  - name: "rocket-cap.stl"
    label: "Bracket Cap — STL"
  - name: "rocket-brace.stl"
    label: "Bracket Brace — STL"
  - name: "rocket-cap.scad"
    label: "Bracket Cap — OpenSCAD Source"
  - name: "rocket-brace.scad"
    label: "Bracket Brace — OpenSCAD Source"
  - name: "rocket-study.scad"
    label: "Bracket Study — OpenSCAD Source"
---

The rocket we were launching was designed for larger booster motors than we could get locally. Rather than redesign the whole chassis, I modelled a custom two-part motor mount to hold the smaller available boosters securely in their place.

See [Print Settings](print-settings) for slicer configuration.

## Design

The mount is a two-part assembly. The bracket is a flat cylinder with two bored holes sized for the booster casings. The base is the same geometry but adds a retaining lip at one end — the boosters push against it under thrust so they can't travel through the mount. Both parts share a common variables file so booster dimensions only need updating in one place.

