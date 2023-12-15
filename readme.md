 Here is a README.md file to explain setting up and running the offer filtering application:

# Offer Filtering Application

## Overview

This application filters a list of offer data from a JSON file based on specified criteria and outputs the filtered offers to another JSON file.

## Prerequisites

- Python 3.6 or higher

## Setting Up

1. Clone this repository

   ```
   git clone https://github.com/fukphua123/Offer-Filtering-Application.git
   ```
## Usage

To filter offers and output to `output.json`:

```
python offer_filter.py 2019-12-25
```

This will filter offers using Dec 25, 2019 as the check-in date.

By default, input data is read from `input.json` and output written to `output.json`.


Use `-h` to show additional options:

```
python offer_filter.py -h
```

## Customization

To change the filtering behavior, modify the variables in the `OffersFilter` class:

- `validity_period`: Number of validity days from check-in date  
- `limit_categories`: Category IDs to limit to 
- `max_offers_per_category`: Maximum number of offers per category
- `offers_count`: Total number of output offers

