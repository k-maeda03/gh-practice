#!/usr/bin/env python3
"""
Improved hello world script for GitHub CLI practice
"""
import argparse
import logging
import sys
from typing import Optional


def setup_logging() -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main() -> None:
    """Main function with improved features"""
    parser = argparse.ArgumentParser(description="GitHub CLI practice script")
    parser.add_argument(
        "--name", default="GitHub CLI", help="Name to greet (default: GitHub CLI)"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        setup_logging()
        logging.info("Starting hello script")

    try:
        print(f"Hello, {args.name}!")
        print("This is an improved practice repository.")

        if args.verbose:
            logging.info("Script completed successfully")

    except Exception as e:
        try:
            print(f"Error: {e}", file=sys.stderr)
        except Exception:
            # If even stderr printing fails, just exit
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
