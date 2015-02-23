# gr-ec-additional-modules-and-flow-graphs
GNU Radio modules for doppler correction (for GPredict and Hummingbird) and different versions of signal processing flow graphs for ESTCube-1.

This is an addition to gr-ec (https://github.com/andresv/gr-ec) repository, originally created by Martin Neerot and modified by Andres Vahter.

## Version 1
+ GNU Radio Companion file (.grc):
  + uses 'PLL Freq Det' block to find the correct signal frequency.

## Version 2
+ GNU Radio Companion file (.grc).
+ Python script:
  + connects to a Gpredict radio interface, where it gets the correct signal frequency and sends it to the GNU Radio flow graph.

## Version 3
+ GNU Radio Companion file (.grc).
+ GNU Radio module
  + the Python script from version 2 as a GNU Radio block.

## Version 4
+ GNU Radio module
  + communicates with Hummingbird (uses Extended Response Protocol) instead of Gpredict.
Use the flowgraph from version 3.

### How to install the modules in versions 3 and 4
In the module folder:

    cd build
    cmake ..
    make
    sudo make install
    sudo ldconfig
