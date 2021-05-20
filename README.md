# Introduction

Simple algorithm for transferring .txt files through UDP Sockets, the same was implemented in python using the libraries:

* Hashlib
* Os
* Time
* Random
* Argparse
* Datetime


# Methodology

Through an input file it divides it into blocks of optional size (Frames) and sends these blocks to the server separately, it is possible to generate an error probability to test the algorithm control functionalities. Can be used to test transmission time, graphs with the amount of error and more,it uses Hash to encrypt the blocks.

# Functionalities

-f = frame size
-e = Percentage of error
-i = input file

Example:

1- python receptor.py
2- python transmissor.py -i data.txt -f 1024 -e 5

to transmit the file "data.txt" with frames (Packages) of 1024 Bytes and with a percentage of 5% of error.

A log file ("log.txt") will be generated with the transmission information, where the error occurred, the amount of error, transmission time, etc. And also a file with the entire message received by the recipient ("" message_received_receptor ")

# Future Ideas

Implement some sliding window method to focus on performance


