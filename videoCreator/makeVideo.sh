#!/bin/bash

# $1 is the scene to be rendered
# ql => low quality, qm higher, qh full HD, qk 4k
manim -pql scene.py $1
