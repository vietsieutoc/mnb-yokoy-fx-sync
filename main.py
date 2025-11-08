#!/usr/bin/env python3
"""
Simple MNB FX Rate Fetcher

Fetches exchange rates from the Hungarian National Bank (MNB) using the mnb library.
Can optionally upload rates to Yokoy.
"""

import sys
import argparse
from datetime import datetime, date
from mnb import Mnb

from config import Config
from yokoy_client import YokoyClient


def fetch_current_rates(client):
    """Fetch and display current exchange rates"""
    print(" Fetching current exchange rates...\n")
    rates_data = client.get_current_exchange_rates()
    
    if not rates_data:
        print("⚠️  No rates available (might be weekend or holiday)")
        return None
    
    return rates_data


def fetch_rates_for_date(client, target_date):
    """Fetch and display exchange rates for a specific date"""
    print(f" Fetching exchange rates for {target_date}...\n")
    
    # Convert string to date object if needed
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    # Get all available currencies first
    currencies = client.get_currencies()
    
    # MNB API expects start date, end date, and list of currencies
    rates_list = client.get_exchange_rates(target_date, target_date, currencies)
    
    if not rates_list or len(rates_list) == 0:
        print(f"⚠️  No rates available for {target_date}")
        print("    (Rates are not published on weekends and holidays)")
        return None
    
    return rates_list[0]  # Return first (and only) day


def display_rates(rates_data):
    """Display exchange rates in a formatted table"""
    print(f"Date: {rates_data.date}")
    print(f"Total currencies: {len(rates_data.rates)}\n")
    
    print("-" * 60)
    print(f"{'Currency':<12} {'Rate (HUF)':<15}")
    print("-" * 60)
    
    # Display all rates
    for rate in rates_data.rates:
        print(f"{rate.currency:<12} {rate.rate:<15.4f}")
    
    print("-" * 60)
    print(f"\n✅ Successfully fetched {len(rates_data.rates)} exchange rates")


def main():
    """Main function to fetch and display exchange rates from MNB"""
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Fetch exchange rates from Hungarian National Bank (MNB) and optionally upload to Yokoy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                        # Fetch current rates
  %(prog)s --date 2025-11-07      # Fetch rates for specific date
  %(prog)s --upload               # Fetch and upload to Yokoy
  %(prog)s -d 2025-11-07 --upload # Fetch specific date and upload
        """
    )
    
    parser.add_argument(
        '--date', '-d',
        type=str,
        help='Fetch rates for specific date (format: YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--upload', '-u',
        action='store_true',
        help='Upload rates to Yokoy (requires YOKOY_API_KEY in .env)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("MNB Exchange Rate Fetcher")
    print("=" * 60)
    
    # Create MNB client
    print("\n Connecting to MNB API...")
    
    try:
        client = Mnb()
        
        # Fetch rates based on arguments
        if args.date:
            # Validate date format
            try:
                target_date_obj = datetime.strptime(args.date, '%Y-%m-%d').date()
            except ValueError:
                print(f"❌ Invalid date format: {args.date}")
                print("   Please use YYYY-MM-DD format (e.g., 2025-11-07)")
                return 1
            
            rates_data = fetch_rates_for_date(client, args.date)
        else:
            rates_data = fetch_current_rates(client)
            target_date_obj = rates_data.date if rates_data else None
        
        # Display results
        if rates_data:
            display_rates(rates_data)
        else:
            return 1
        
        # Upload to Yokoy if requested
        if args.upload:
            print("\n" + "=" * 60)
            print("Yokoy Upload")
            print("=" * 60)
            
            # Check if Yokoy is configured
            if not Config.is_configured():
                print("\n⚠️  Yokoy upload skipped: YOKOY_API_KEY not configured")
                print("   Create a .env file with your YOKOY_API_KEY")
                print("   Example: cp .env.example .env")
                return 1
            
            try:
                Config.validate()
                print(f"\n🔗 Connecting to Yokoy API...")
                print(f"   URL: {Config.YOKOY_API_URL}")
                
                yokoy = YokoyClient(Config.YOKOY_API_URL, Config.YOKOY_API_KEY)
                
                print(f"📤 Uploading {len(rates_data.rates)} rates for {target_date_obj}...")
                result = yokoy.upload_fx_rates(rates_data, target_date_obj)
                
                if result.get('success'):
                    print(f"\n✅ Successfully uploaded {result.get('rates_uploaded')} rates to Yokoy")
                    print(f"   Status: {result.get('status_code')}")
                else:
                    print(f"\n❌ Failed to upload rates to Yokoy")
                    print(f"   Error: {result.get('error')}")
                    if result.get('error_detail'):
                        print(f"   Details: {result.get('error_detail')}")
                    return 1
                    
            except ValueError as e:
                print(f"\n❌ Configuration error: {e}")
                return 1
            except Exception as e:
                print(f"\n❌ Upload error: {e}")
                print(f"   Type: {type(e).__name__}")
                return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Type: {type(e).__name__}")
        if hasattr(e, '__cause__') and e.__cause__:
            print(f"   Cause: {e.__cause__}")
        return 1
    
    print("\n" + "=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())
