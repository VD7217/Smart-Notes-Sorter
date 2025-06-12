#!/usr/bin/env python3
"""
Smart Notes Organizer - Main Entry Point

This script serves as the entry point for the Smart Notes Organizer tool,
which automatically sorts images and PDFs into subject folders based on content.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from sorter import NoteSorter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Smart Notes Organizer - Automatically sort notes by subject'
    )
    parser.add_argument(
        '--input', 
        type=str, 
        required=True,
        help='Path to the input folder containing unsorted notes'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        required=True,
        help='Path to the output folder where sorted notes will be stored'
    )
    parser.add_argument(
        '--copy', 
        action='store_true',
        help='Copy files instead of moving them'
    )
    return parser.parse_args()

def main():
    """Main function to run the notes sorter."""
    args = parse_arguments()
    
    # Validate input and output paths
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"Input directory '{input_path}' does not exist or is not a directory")
        return 1
    
    # Create output directory if it doesn't exist
    if not output_path.exists():
        logger.info(f"Creating output directory: {output_path}")
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize and run the sorter
    sorter = NoteSorter(input_path, output_path, copy_files=args.copy)
    sorter.process_files()
    
    logger.info("Notes sorting completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())