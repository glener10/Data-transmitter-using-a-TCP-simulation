<h1 align="center">Data Transmitter using a TCP Simulation</h1>

<p align="center"> 🚀Simple algorithm that simulates Socket TCP for transmitting different types of data... </p>


Table of Contents

===================

<!--ts-->
* [Environment](#Environment)
* [Demo](#Demo)


<!--te-->

===================


# Environment

Execution environment used and tested:

**SO**: Ubuntu 20.04     **Kernel**: 5.8.0-63-generic




# Demo

Through an input file it divides into blocks of optional size (Frames) and sends these blocks to the server separately, it is possible to generate a probability of error and size of each block (frame) to test the algorithm's control features.

It can be used to test the transmission time, graphs with the amount of errors.

-f   __* frame size *__

-e __* Percentage of error *__

-i = __* input file (It must be inside the 'inputs' folder or edit the default path within the 'transmitter.py' file) *__



```bash
#Open one CMD
$ ./python receptor.py
```

```bash
#Open a second CMD
$ ./python transmissor.py -i input4.ppm -f 1024 -e 5
```

to transmit the file "input4.ppm" with frames (Packages) of 1024 Bytes and with a percentage of 5% of error.

The sending status of each block will be displayed on the screen, and finally the total transmission time, number of errors and the number of blocks sent.

The receiver generates a file with the name 'Output. (Input extension)' with all the content you received from transmitter.py
