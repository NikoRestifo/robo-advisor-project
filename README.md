# Robo Advisor Program

A Python application that allows the user to pick stocks, returns information about them, and then determines whether the user should buy or sell the stocks.

## Prerequisites

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Fork this [remote repository](git@github.com:NikoRestifo/robo-advisor-project.git) under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```sh
cd ~/Desktop/robo-advisor-project
```

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.8 # (first time only)
conda activate stocks-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)

## Setup

In in the root directory of your local repository, create a new file called ".env", and update the contents of the ".env" file to include ur API key:

    ALPHAVANTAGE_API_KEY="abc123"

## Usage

Run the program:

```py
python app/robo_advisor.py

```

Once the program is run, the user is required to enter stocks one at a time. The user should type 'DONE' when finished entering stock tickers. Once a line chart pops up, the program will not proceed until the user closes the chart.
