"""
Smart Notes Organizer - Core Sorter Module

This module contains the core logic for classifying and sorting notes files
based on their content.
"""

import json
import logging
import os
import re
import shutil
from pathlib import Path

from ocr_utils import extract_text_from_file

logger = logging.getLogger(__name__)

class NoteSorter:
    """Class to handle the sorting of notes files into subject folders."""
    
    def __init__(self, input_dir, output_dir, copy_files=False):
        """
        Initialize the NoteSorter.
        
        Args:
            input_dir (Path): Directory containing unsorted notes
            output_dir (Path): Directory where sorted notes will be placed
            copy_files (bool): Whether to copy files instead of moving them
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.copy_files = copy_files
        
        # Load subject keywords from JSON file
        subjects_file = Path(__file__).parent / "subjects.json"
        with open(subjects_file, 'r') as f:
            self.subjects_data = json.load(f)
        
        # Supported file extensions
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.pdf'}
    
    def process_files(self):
        """Process all files in the input directory."""
        logger.info(f"Starting to process files from {self.input_dir}")
        
        # Get all files in the input directory
        files = [f for f in self.input_dir.glob('**/*') 
                if f.is_file() and f.suffix.lower() in self.supported_extensions]
        
        if not files:
            logger.warning(f"No supported files found in {self.input_dir}")
            return
        
        logger.info(f"Found {len(files)} files to process")
        
        # Process each file
        for file_path in files:
            self._process_single_file(file_path)
    
    def _process_single_file(self, file_path):
        """
        Process a single file.
        
        Args:
            file_path (Path): Path to the file to process
        """
        logger.info(f"Processing file: {file_path}")
        
        try:
            # Extract text from the file
            text = extract_text_from_file(file_path)
            
            if not text:
                logger.warning(f"Could not extract text from {file_path}")
                subject = "Unclassified"
            else:
                # Determine the subject
                subject = self._classify_text(text)
            
            # Move or copy the file to the appropriate subject folder
            self._move_file_to_subject_folder(file_path, subject)
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
    
    def _classify_text(self, text):
        """
        Classify the text into a subject.
        
        Args:
            text (str): The text to classify
            
        Returns:
            str: The classified subject
        """
        # Preprocess the text
        text = self._preprocess_text(text)
        
        # Count keyword occurrences for each subject
        subject_scores = {}
        for subject, keywords in self.subjects_data.items():
            score = sum(1 for keyword in keywords if keyword in text)
            subject_scores[subject] = score
        
        # Find the subject with the highest score
        if not subject_scores or max(subject_scores.values()) == 0:
            return "Unclassified"
        
        max_score = max(subject_scores.values())
        best_subjects = [subj for subj, score in subject_scores.items() if score == max_score]
        
        # If there's a tie, choose the first one alphabetically for consistency
        return sorted(best_subjects)[0]
    
    def _preprocess_text(self, text):
        """
        Preprocess the text for classification.
        
        Args:
            text (str): The text to preprocess
            
        Returns:
            str: The preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _move_file_to_subject_folder(self, file_path, subject):
        """
        Move or copy a file to the appropriate subject folder.
        
        Args:
            file_path (Path): Path to the file to move
            subject (str): The subject folder to move the file to
        """
        # Create the subject folder if it doesn't exist
        subject_folder = self.output_dir / subject
        subject_folder.mkdir(exist_ok=True)
        
        # Destination path
        dest_path = subject_folder / file_path.name
        
        # Check if destination file already exists
        if dest_path.exists():
            base_name = file_path.stem
            extension = file_path.suffix
            counter = 1
            while dest_path.exists():
                new_name = f"{base_name}_{counter}{extension}"
                dest_path = subject_folder / new_name
                counter += 1
        
        # Move or copy the file
        if self.copy_files:
            logger.info(f"Copying {file_path} to {dest_path}")
            shutil.copy2(file_path, dest_path)
        else:
            logger.info(f"Moving {file_path} to {dest_path}")
            shutil.move(file_path, dest_path)