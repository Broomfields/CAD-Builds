---
title: "Rocket Booster Bracket"
description: "Custom two-part motor mount designed to hold locally available boosters in a rocket chassis built for larger ones."
date: "2021-07-31"
cover: "02-model-cap.jpeg"
tags: ["openscad", "3d-printing", "rocketry"]
cad_tool: "OpenSCAD"
status: "complete"
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

## Design

The mount is a two-part assembly. The bracket is a flat cylinder with two bored holes sized for the booster casings. The base is the same geometry but adds a retaining lip at one end — the boosters push against it under thrust so they can't travel through the mount. Both parts share a common variables file so booster dimensions only need updating in one place.

## Gallery

![Bracket — Cap Study, recreating original booster cap as a model](01-model-study.png)
![Bracket — Cap, this braces the top of the boosters, and has a cap to hold them in the bracket](02-model-cap.jpeg)
![Bracket — Brace, this is braces the bottom of the boosters and acts as the rocket base](03-model-brace.jpeg)
![Launch rig](04-rig.jpeg)
![Rocket body](05-rocket-base.jpeg)
![Rocket assembled and ready](06-rocket.jpeg)
