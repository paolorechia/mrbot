#!/bin/bash
# Requires opencv_createsamples from OpenCV 3.4.16 (compiled from source)
opencv_createsamples -info annotations.txt  -vec vector.vec -bg bg.txt 