# PyDelivery
A simple Python CLI program that manages the daily package deliveries for a fictional delivery service.

## Author

Craig Bodo

craigmbodo@gmail.com

## Description

PyDelivery is a simple Python CLI program that manages a fictional delivery service's daily package deliveries. The program uses a custom-built hash table to store and manage the package data, and the Greedy algorithm to "deliver" the packages. The goal of this program was to find the most efficient algorithm to deliver a set of 40 packages between two trucks, i.e. the lowest number of miles driven by both trucks. Amongst other constraints specific to operating hours and package specifics, each truck could only carry a maximum of 16 packages and travel an average of 18 miles per hour. Additionally, the trucks had to complete all deliveries within a combined total of 140 miles. This program delivers the packages in 112 miles, while meeting all assigned constraints.

Additionally, the program stores "snapshots" that display the status of all packages at a specified time (at hub, delivered, or in transit). 


## Running The Application:

This program will run on any system with Python 3.10+ installed.

Navigate to *pydelivery* directory in your terminal/command line prompt, then run the following command:

```bash
$ python3 main.py
```
