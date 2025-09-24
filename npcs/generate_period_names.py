#!/usr/bin/env python3
"""
Script to generate period-appropriate names for the game (1970-2030)
This will create approximately 900 names total (75 per 5-year period)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deepseek.services.period_names import PeriodNameGenerator
import json

def main():
    print("="*60)
    print("PERIOD NAME GENERATOR")
    print("Generating period-appropriate names from 1970 to 2030")
    print("="*60)

    # Create generator
    generator = PeriodNameGenerator()

    # Check if we want to regenerate or use existing
    if os.path.exists("period_names.json"):
        response = input("\nExisting names found. Regenerate? (y/n): ")
        if response.lower() != 'y':
            generator.load_from_file()
            print("\nLoaded existing names.")

            # Display summary
            total = 0
            for period, names in generator.period_names.items():
                print(f"{period}: {len(names)} names")
                total += len(names)
            print(f"\nTotal names available: {total}")
            return

    # Generate all names
    print("\nGenerating names for all periods...")
    print("This will make API calls to generate period-appropriate names.\n")

    all_names = generator.generate_all_periods()

    # Display results
    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60)

    total = 0
    for period, names in all_names.items():
        print(f"{period}: {len(names)} names")
        total += len(names)
        # Show first 5 names as example
        print(f"  Examples: {', '.join(names[:5])}")
        print()

    print(f"Total names generated: {total}")

    # Save to file
    generator.save_to_file()
    print(f"\nNames saved to period_names.json")

    # Test retrieval
    print("\n" + "="*60)
    print("TESTING YEAR-BASED RETRIEVAL")
    print("="*60)

    test_years = [1972, 1978, 1985, 1992, 1999, 2005, 2015, 2025]
    for year in test_years:
        names = generator.get_names_for_year(year, 5)
        print(f"\n{year} names: {', '.join(names)}")

    print("\n" + "="*60)
    print("Setup complete! Names are ready for use in the game.")
    print("="*60)


if __name__ == "__main__":
    main()