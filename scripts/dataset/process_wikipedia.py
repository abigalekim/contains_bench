#!/usr/bin/env python3
"""
Script to download the Wikimedia Wikipedia dataset from Hugging Face
and save it as JSON to a specified file location.
"""

import json
import os
from pathlib import Path
from datasets import load_dataset
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_wikipedia_dataset(output_path: str = "/mnt/wiscdb/abigale/wikipedia.json"):
    """
    Download the Wikimedia Wikipedia dataset and save as JSON.
    
    Args:
        output_path (str): Path where the JSON file will be saved
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Starting download of Wikimedia Wikipedia dataset...")
        logger.info("This may take a significant amount of time and storage space.")
        
        # Load the dataset
        # Note: This dataset is very large, you might want to specify a subset
        # For example: dataset = load_dataset("wikimedia/wikipedia", "20231101.en", split="train[:1000]")
        dataset = load_dataset("wikimedia/wikipedia", "20231101.en")
        
        logger.info(f"Dataset loaded successfully. Number of examples: {len(dataset['train'])}")
        
        # Convert to list of dictionaries for JSON serialization
        logger.info("Converting dataset to JSON format...")
        data_list = []
        
        # Process in batches to avoid memory issues
        batch_size = 1000
        total_examples = len(dataset['train'])
        
        for i in range(0, total_examples, batch_size):
            batch = dataset['train'].select(range(i, min(i + batch_size, total_examples)))
            batch_data = [example for example in batch]
            data_list.extend(batch_data)
            
            # Log progress
            if (i // batch_size + 1) % 10 == 0:
                logger.info(f"Processed {i + len(batch_data)}/{total_examples} examples")
        
        # Save to JSON file
        logger.info(f"Saving dataset to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        
        # Get file size for confirmation
        file_size = os.path.getsize(output_path)
        file_size_gb = file_size / (1024**3)
        
        logger.info(f"Dataset successfully saved to {output_path}")
        logger.info(f"File size: {file_size_gb:.2f} GB")
        
    except Exception as e:
        logger.error(f"Error downloading dataset: {str(e)}")
        raise

def download_wikipedia_subset(output_path: str = "/mnt/wiscdb/abigale/wikipedia_subset.json", 
                            num_examples: int = 10000):
    """
    Download a subset of the Wikipedia dataset for testing purposes.
    
    Args:
        output_path (str): Path where the JSON file will be saved
        num_examples (int): Number of examples to download
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting download of Wikipedia dataset subset ({num_examples} examples)...")
        
        # Load a subset of the dataset
        dataset = load_dataset("wikimedia/wikipedia", "20231101.en", split=f"train[:{num_examples}]")
        
        logger.info(f"Dataset subset loaded successfully. Number of examples: {len(dataset)}")
        
        # Convert to list of dictionaries
        data_list = [example for example in dataset]
        
        # Save to JSON file
        logger.info(f"Saving dataset subset to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        
        # Get file size for confirmation
        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024**2)
        
        logger.info(f"Dataset subset successfully saved to {output_path}")
        logger.info(f"File size: {file_size_mb:.2f} MB")
        
    except Exception as e:
        logger.error(f"Error downloading dataset subset: {str(e)}")
        raise

if __name__ == "__main__":
    # Install required packages if not already installed
    try:
        import datasets
    except ImportError:
        logger.error("Required package 'datasets' not found. Please install it with:")
        logger.error("pip install datasets")
        exit(1)
    
    # Choose which function to run:
    # Option 1: Download full dataset (WARNING: This is very large!)
    # download_wikipedia_dataset("/mnt/wiscdb/abigale/wikipedia.json")
    
    # Option 2: Download a subset for testing (recommended to start with this)
    download_wikipedia_subset("/mnt/wiscdb/abigale/wikipedia_subset.json", 1000)
    
    # Uncomment the line below to download the full dataset to your specified path
    # download_wikipedia_dataset("/mnt/wiscdb/abigale/wikipedia.json")