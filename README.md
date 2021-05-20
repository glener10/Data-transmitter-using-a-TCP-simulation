# Introduction

Simple algorithm that simulates Socket TCP for transmitting different types of data, such as:

.ppm
.png
.mp3
.jpg
etc...



# Methodology

Through an input file it divides into blocks of optional size (Frames) and sends these blocks to the server separately, it is possible to generate a probability of error and size of each block (frame) to test the algorithm's control features.

It can be used to test the transmission time, graphs with the amount of errors.

# Functionalities

-f = frame size
-e = Percentage of error
-i = input file (It must be inside the 'inputs' folder or edit the default path within the 'transmitter.py' file)

# Example:

1- python receptor.py
2- python transmissor.py -i input4.ppm -f 1024 -e 5

to transmit the file "input4.ppm" with frames (Packages) of 1024 Bytes and with a percentage of 5% of error.

The sending status of each block will be displayed on the screen, and finally the total transmission time, number of errors and the number of blocks sent.

The receiver generates a file with the name 'Output. (Input extension)' with all the content you received from transmitter.py
