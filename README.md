# Podcast Transcription and Academic Paper PDF Conversion

This project provides scripts to transcribe podcasts from audio files or YouTube videos and convert PDFs to Markdown format using the Nougat model.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/andikahakim/podcast_academic_papers_parser.git
    cd <repository_directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Transcribe Podcasts

To transcribe a podcast from an audio file or YouTube video, use the `transcribe_podcast.py` script.

#### From an Audio File
```sh
python src/transcribe_podcast.py <path_to_audio_file>
```

#### From a YouTube Video
```sh
python src/transcribe_podcast.py <youtube_video_url>
```

The transcriptions will be saved as JSON files in the `output/podcasts` directory.

### Convert PDFs to Markdown

To convert PDFs to Markdown format, use the `convert_pdf.py` script.
```sh
python src/python src/convert_pdf.py input_papers
```

The converted Markdown files and corresponding JSON metadata files will be saved in the `output/publications` directory.

## Project Structure
```
podcast_academic_papers_parser/
│
├── src/
│ ├── convert_pdf.py
│ └── transcribe_podcast.py
│
├── input_papers/ # Place your PDF files here
│
├── output/
│ ├── podcasts/ # Transcriptions will be saved here
│ └── publications/ # Converted Markdown files and JSON metadata will be saved here
│
├── requirements.txt
└── README.md
```
>>>>>>> origin/master
