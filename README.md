# Smart Notes Organizer

A Python tool that automatically sorts images and PDFs of class notes into subject folders based on their content.

## Features

- Extracts text from images (JPG, PNG) using Tesseract OCR
- Extracts text from PDF files using PyMuPDF
- Classifies notes into subjects based on keyword matching
- Automatically organizes files into subject folders
- Supports both copying and moving files
- Provides detailed logging

## Project Structure

```
smart_notes_sorter/
│
├── main.py           # Entry script
├── sorter.py         # Core logic for classification/sorting
├── ocr_utils.py      # OCR and PDF reading helpers
├── subjects.json     # Dictionary of subject-related keywords
├── requirements.txt  # All dependencies
└── README.md         # Project overview
```

## Prerequisites

- Python 3.9 or higher
- Tesseract OCR installed on your system

### Installing Tesseract OCR

#### Windows
1. Download the installer from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add the installation directory to your system PATH

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/smart-notes-organizer.git
cd smart-notes-organizer
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py --input /path/to/unsorted/notes --output /path/to/sorted/notes
```

### Options

- `--input`: Path to the input folder containing unsorted notes (required)
- `--output`: Path to the output folder where sorted notes will be stored (required)
- `--copy`: Copy files instead of moving them (optional)

### Example

```bash
python main.py --input ./sample_notes --output ./sorted_notes --copy
```

## Customizing Subject Keywords

You can customize the keywords used for subject classification by editing the `subjects.json` file. Each subject has an array of keywords that are used to identify the subject of a note.

## Future Enhancements

- Implement a machine learning classifier for more accurate subject detection
- Add a graphical user interface (GUI) using Tkinter or Flask
- Support for more file formats
- Batch processing with progress reporting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tesseract OCR for image text extraction
- PyMuPDF for PDF text extraction