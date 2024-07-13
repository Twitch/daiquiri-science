# Imbalanced Daiquiri Batch Calculator

## Description

This script calculates imbalanced daiquiri batch recipes (with dilution) for a craft cocktail class. The goal is to produce 3 imbalanced samples (a rum heavy, a lime heavy, and a syrup heavy example) to demonstrate imbalance, but the 3 examples can be combined in equal parts to achieve the classic 2:1:1 balance of a daiquiri. 

## Usage

Run the script from the command line:

python3 daiquiri-science.py [serving_size] [num_sets] [dilution]

### Command-line Arguments

1. serving_size: Individual serving size in ounces after dilution (default: 1.0)
2. num_sets: Number of sets to prepare. Each set includes one sample of each variation (default: 30)
3. dilution: Target dilution as a decimal. For example, 0.3 represents 30% dilution (default: 0.3)

### Defaults

If no arguments are provided, the script will use these default values:
- Serving size: 1.0 oz
- Number of sets: 30
- Dilution: 0.3 (30%)

### Examples

1. Using default values:
   python3 daiquiri-science.py

2. Specifying all parameters:
   python3 daiquiri-science.py 1.5 40 0.25
   This calculates batches for 40 sets of 3 samples each, with each sample targeted to be 1.5 oz after dilution, and a 25% dilution target.

## Output

The script provides:
- Batch recipes for each Daiquiri variation
- Total batch volumes
- Number of complete sets and total individual samples
- Combined totals of all ingredients
- Final ratio of ingredients when all batches are combined

## Requirements

- Python 3.6 or higher
