#!/bin/bash
# Requires opencv_traincascade from OpenCV 3.4.16 (compiled from source)
opencv_traincascade -data haar -vec vector.vec -bg bg.txt -featureType Haar -numPos 200  -numNeg 1000