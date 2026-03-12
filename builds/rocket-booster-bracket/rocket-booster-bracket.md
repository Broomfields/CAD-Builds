---
title: "Rocket Booster Bracket"
description: "Custom two-part motor mount designed to hold locally available boosters in a rocket chassis built for larger ones."
date: "2026-03-11"
cover: "01_model_original.jpeg"
tags: ["openscad", "3d-printing", "rocketry"]
cad_tool: "OpenSCAD"
status: "complete"
files:
  - name: "rocket-top.stl"
    label: "Bracket — STL"
  - name: "rocket-bottom.stl"
    label: "Bracket Base — STL"
  - name: "rocket-top.scad"
    label: "Bracket — OpenSCAD Source"
  - name: "rocket-bottom.scad"
    label: "Bracket Base — OpenSCAD Source"
  - name: "rocket-misc.scad"
    label: "Shared Variables — OpenSCAD Source"
---

The rocket we were launching was designed for larger booster motors than we could get locally. Rather than redesign the whole chassis, I modelled a custom two-part motor mount to hold the smaller available boosters securely in their place.

## Design

The mount is a two-part assembly. The bracket is a flat cylinder with two bored holes sized for the booster casings. The base is the same geometry but adds a retaining lip at one end — the boosters push against it under thrust so they can't travel through the mount. Both parts share a common variables file so booster dimensions only need updating in one place.

## Gallery

![Bracket — front view](01_model_original.png)
![Bracket — three-quarter view](02_model_cap.jpeg)
![Bracket base — retaining lip visible](03_model_base.jpeg)
![Launch rig](04_rig.jpeg)
![Rocket body](05_rocket_base.jpeg)
![Rocket assembled and ready](06_rocket.jpeg)