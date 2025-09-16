# LLM-Document-Parser

This project consists of two main components: a backend API and a core document parsing worker.

## Components

### API

The backend API is built with TypeScript and Bun.

- **Installation:** `bun install`
- **Development:** `bun dev`
- **Production:** `bun start`

### Core Worker

The core worker is a Python application responsible for document parsing.

- **Setup:**
  - Create a virtual environment: `python -m venv .venv`
  - Activate the environment:
    - Linux/macOS: `source .venv/bin/activate`
    - Windows: `.venv\Scripts\activate`
  - Install dependencies: `pip install -r requirements.txt`
- **Run:** `python src/app.py`
