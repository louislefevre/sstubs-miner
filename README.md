# SStuBs Miner
Data mining and analysis for the [ManySStuBs4J dataset](https://zenodo.org/record/3653444#.X0qMA4t7lEY) being used in the [MSR 2021 Data Mining Challenge](https://2021.msrconf.org/track/msr-2021-mining-challenge).

## Contents
The program is split into two modules: the data miner and the data analyser.

#### Data Miner
Run using the Miner.py script, and is responsible for:
- Extracting data from the SStuBs dataset.
- Retrieving data from GitHub using their [REST API](https://developer.github.com/v3/).
- Writing the data to a CSV file.

Any code relating to this module can be found in the *miners* folder, as well as the (shared) *util* folder.

#### Data Analyser
Run using the Analyser.py script, and is responsible for:
- Extracting data from the CSV file generated by the data miner.
- Analysing the data and calculating results.
- Generating the results as output.

Any code relating to this module can be found in the *analysers* folder, as well as the (shared) *util* folder.

## Program Execution
Running the program requires two things:
- A *tokens* file, containing one or more personal access tokens for authenticating with GitHub. This must be located in the *data* directory.
- The ManySStuBs4J dataset, named *sstubs.json*. This must be located in the *data* directory.

The code can then be executed simply by running *python Miner.py* or *python Analyser.py* on the command line

## Notes
- This program was built on a custom setup of Arch Linux, and has not been tested on other operating systems.
- The code is only designed to retrieve data related to our needs, but is extensible and can be adapted for different data.
- A single personal access token can only send 5000 requests to GitHub per hour, limiting the rate at which data is mined.
- Multiple tokens can be placed in the *token* file, and the program will automatically choose the best one throughout execution (based on remaining requests and reset time).
- Dta mining takes an extremely long time (roughly 1 hour per 800 entries).
