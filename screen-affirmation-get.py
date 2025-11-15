#!/usr/bin/env python3
"""
Fetch daily affirmation from affirmations.dev API
"""

import os
import logging
import requests
from xml.sax.saxutils import escape
from utility import update_svg, configure_logging

configure_logging()

API_URL = "https://www.affirmations.dev/"


def get_affirmation():
    """Fetch a random affirmation from the API"""
    try:
        logging.info("Fetching affirmation from affirmations.dev")
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        affirmation = data.get('affirmation', 'You are doing great!')
        logging.info(f"Got affirmation: {affirmation}")
        return affirmation
        
    except Exception as e:
        logging.error(f"Error fetching affirmation: {e}")
        # Return a default affirmation if API fails
        return "You are capable of amazing things!"


def main():
    output_svg_filename = 'screen-output-weather.svg'
    
    # Get affirmation
    affirmation = get_affirmation()
    
    # Prepare output dict
    output_dict = {
        'AFFIRMATION_TEXT': escape(affirmation)
    }
    
    logging.info(f"Updating SVG with affirmation")
    update_svg(output_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
