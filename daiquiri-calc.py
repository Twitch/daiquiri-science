#!/usr/bin/env python3

import math
import argparse

def round_up_to_quarter(value):
    return math.ceil(value * 4) / 4

def calculate_batch(rum, syrup, lime, num_sets, serving_size, dilution):
    non_water_volume = serving_size * (1 - dilution)
    water_volume = serving_size * dilution
    return {
        'rum': round_up_to_quarter(rum * non_water_volume * num_sets),
        'syrup': round_up_to_quarter(syrup * non_water_volume * num_sets),
        'lime': round_up_to_quarter(lime * non_water_volume * num_sets),
        'water': round_up_to_quarter(water_volume * num_sets)
    }

def calculate_test_set(rum, syrup, lime, dilution):
    total_non_water = rum + syrup + lime

    # Determine the smallest scale factor that makes each ingredient at least 0.25 oz
    scale_factor = math.ceil(0.25 / min(rum, syrup, lime))

    # Calculate the total volume with water
    total_with_water = total_non_water / (1 - dilution)

    # Calculate the scaled amounts
    rum_amount = round_up_to_quarter(rum * total_with_water * scale_factor / total_non_water)
    syrup_amount = round_up_to_quarter(syrup * total_with_water * scale_factor / total_non_water)
    lime_amount = round_up_to_quarter(lime * total_with_water * scale_factor / total_non_water)
    water_amount = round_up_to_quarter(total_with_water * dilution * scale_factor / total_non_water)

    return {
        'rum': rum_amount,
        'syrup': syrup_amount,
        'lime': lime_amount,
        'water': water_amount
    }

def display_output(rum_heavy, syrup_heavy, lime_heavy, num_sets, individual_serving, is_sample=False):
    if is_sample:
        print("\nSample Set Sizes (in ounces):")
    else:
        print(f"\nCalculating batches for {num_sets} sets of 3 samples each (total {num_sets * 3} individual samples)")
        print(f"Each sample is targeted to be {individual_serving:.2f}oz after dilution")
        print(f"Target dilution: {dilution * 100:.1f}%")

    print("\nBatch Recipes (in ounces, rounded up to nearest 1/4 oz):")
    print(f"Rum-heavy:   {rum_heavy['rum']:.2f}oz rum, {rum_heavy['syrup']:.2f}oz syrup, {rum_heavy['lime']:.2f}oz lime, {rum_heavy['water']:.2f}oz water")
    print(f"Syrup-heavy: {syrup_heavy['rum']:.2f}oz rum, {syrup_heavy['syrup']:.2f}oz syrup, {syrup_heavy['lime']:.2f}oz lime, {syrup_heavy['water']:.2f}oz water")
    print(f"Lime-heavy:  {lime_heavy['rum']:.2f}oz rum, {lime_heavy['syrup']:.2f}oz syrup, {lime_heavy['lime']:.2f}oz lime, {lime_heavy['water']:.2f}oz water")

    # Calculate total volume for each batch
    total_volume_rum_heavy = sum(rum_heavy.values())
    total_volume_syrup_heavy = sum(syrup_heavy.values())
    total_volume_lime_heavy = sum(lime_heavy.values())

    print("\nTotal batch volumes:")
    print(f"Rum-heavy:   {total_volume_rum_heavy:.2f}oz")
    print(f"Syrup-heavy: {total_volume_syrup_heavy:.2f}oz")
    print(f"Lime-heavy:  {total_volume_lime_heavy:.2f}oz")

    if not is_sample:
        # Calculate actual number of complete sets each batch will yield
        actual_sets_rum_heavy = math.floor(total_volume_rum_heavy / individual_serving)
        actual_sets_syrup_heavy = math.floor(total_volume_syrup_heavy / individual_serving)
        actual_sets_lime_heavy = math.floor(total_volume_lime_heavy / individual_serving)
        actual_complete_sets = min(actual_sets_rum_heavy, actual_sets_syrup_heavy, actual_sets_lime_heavy)

        print(f"\nEach batch will yield at least {actual_complete_sets} complete sets of samples")
        print(f"Total individual samples: {actual_complete_sets * 3}")

    # Verify the balance when combined
    combined_rum = rum_heavy['rum'] + syrup_heavy['rum'] + lime_heavy['rum']
    combined_syrup = rum_heavy['syrup'] + syrup_heavy['syrup'] + lime_heavy['syrup']
    combined_lime = rum_heavy['lime'] + syrup_heavy['lime'] + lime_heavy['lime']
    combined_water = rum_heavy['water'] + syrup_heavy['water'] + lime_heavy['water']

    print("\nCombined totals:")
    print(f"Rum:   {combined_rum:.2f}oz")
    print(f"Syrup: {combined_syrup:.2f}oz")
    print(f"Lime:  {combined_lime:.2f}oz")
    print(f"Water: {combined_water:.2f}oz")

    total_volume = combined_rum + combined_syrup + combined_lime + combined_water
    print(f"\nActual ratio when combined (rum:syrup:lime:water): {combined_rum/total_volume:.3f}:{combined_syrup/total_volume:.3f}:{combined_lime/total_volume:.3f}:{combined_water/total_volume:.3f}")

def main():
    parser = argparse.ArgumentParser(
        description='Calculate cocktail batch recipes with dilution for a Daiquiri variation class.',
        epilog='This script helps prepare three variations of a Daiquiri (rum-heavy, syrup-heavy, and lime-heavy) '
               'for a cocktail balance class. It calculates the required amounts for each batch, accounting for '
               'the desired serving size, number of sets, and dilution.'
    )

    parser.add_argument('serving_size', type=float, nargs='?', default=1.0,
                        help='Individual serving size in ounces after dilution (default: 1.0)')
    parser.add_argument('num_sets', type=int, nargs='?', default=30,
                        help='Number of sets to prepare. Each set includes one sample of each variation (default: 30)')
    parser.add_argument('dilution', type=float, nargs='?', default=0.3,
                        help='Target dilution as a decimal. For example, 0.3 represents 30%% dilution (default: 0.3)')
    parser.add_argument('--sample', action='store_true',
                        help='Generate a single sample set with practical measurements for bartender testing.')

    args = parser.parse_args()

    individual_serving = args.serving_size
    num_sets = args.num_sets
    global dilution
    dilution = args.dilution
    sample = args.sample

    # Define the imbalanced recipes (proportions for non-water ingredients)
    rum_heavy_recipe = (0.5625, 0.21875, 0.21875)
    syrup_heavy_recipe = (0.46875, 0.3125, 0.21875)
    lime_heavy_recipe = (0.46875, 0.21875, 0.3125)

    if sample:
        print("\nGenerating a single sample set with practical measurements for bartender testing...\n")

        rum_heavy = calculate_test_set(*rum_heavy_recipe, dilution)
        syrup_heavy = calculate_test_set(*syrup_heavy_recipe, dilution)
        lime_heavy = calculate_test_set(*lime_heavy_recipe, dilution)

        display_output(rum_heavy, syrup_heavy, lime_heavy, num_sets, individual_serving, is_sample=True)
    else:
        # Calculate batches with specified serving size
        rum_heavy = calculate_batch(*rum_heavy_recipe, num_sets, individual_serving, dilution)
        syrup_heavy = calculate_batch(*syrup_heavy_recipe, num_sets, individual_serving, dilution)
        lime_heavy = calculate_batch(*lime_heavy_recipe, num_sets, individual_serving, dilution)

        display_output(rum_heavy, syrup_heavy, lime_heavy, num_sets, individual_serving)

if __name__ == "__main__":
    main()
