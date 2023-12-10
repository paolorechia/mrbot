#!/bin/bash
# Requires opencv_traincascade from OpenCV 3.4.16 (compiled from source)
mkdir lbp
opencv_traincascade -data lbp -vec vector.vec -bg bg.txt -featureType LBP -numPos 168 -numNeg 1100 -numThreads 16 -w 220 -h 40