# AI Book Notes

A Streamlit-based web application for managing and analyzing book notes with AI capabilities.

## Features

- Add and manage books with titles and authors
- Create and organize notes for each book
- Tag system for better organization
- Search functionality for books and notes
- Clean and intuitive user interface

## Setup

1. Clone the repository:
```bash
git clone [your-repository-url]
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run ai_book_notes/src/main.py
```

5. Open your browser and go to `http://localhost:8501`

## Project Structure

```
ai_book_notes/
├── src/
│   └── main.py         # Main application file
└── requirements.txt    # Project dependencies
```

## 🚀 Roadmap

### Phase 1: Core Improvements
- [ ] Migrate to PostgreSQL for data persistence
- [ ] Add simple email/password authentication
- [ ] Make UI mobile-friendly
- [ ] Add dark mode support
- [ ] Enable note export (PDF/Markdown)

### Phase 2: Note-Taking Enhancements
- [ ] Add rich text editor
- [ ] Implement better tag organization
- [ ] Add image attachments to notes
- [ ] Create better search functionality
- [ ] Add note categories/folders

### Phase 3: AI Features
- [ ] Add AI-powered note summarization
- [ ] Implement key insights extraction
- [ ] Generate book recommendations
- [ ] Add automated topic tagging

## Contributing

Feel free to open issues and pull requests for any improvements you'd like to add.

## License

MIT License 