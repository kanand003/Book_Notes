# src/main.py
import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Initialize database
def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         author TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         book_id INTEGER,
         content TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY (book_id) REFERENCES books (id))
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tags
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         note_id INTEGER,
         tag_name TEXT NOT NULL,
         FOREIGN KEY (note_id) REFERENCES notes (id))
    ''')
    conn.commit()
    conn.close()

def add_book(title, author):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
    conn.commit()
    conn.close()

def add_note(book_id, content):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO notes (book_id, content) VALUES (?, ?)', (book_id, content))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect('books.db')
    books = pd.read_sql_query('SELECT * FROM books', conn)
    conn.close()
    return books

def get_notes(book_id):
    conn = sqlite3.connect('books.db')
    notes = pd.read_sql_query('SELECT * FROM notes WHERE book_id = ?', conn, params=(book_id,))
    conn.close()
    return notes

def search_books(query):
    conn = sqlite3.connect('books.db')
    books = pd.read_sql_query(
        'SELECT * FROM books WHERE title LIKE ? OR author LIKE ?', 
        conn, 
        params=(f'%{query}%', f'%{query}%')
    )
    conn.close()
    return books

def search_notes(query, book_id=None):
    conn = sqlite3.connect('books.db')
    if book_id:
        notes = pd.read_sql_query(
            'SELECT * FROM notes WHERE book_id = ? AND content LIKE ?',
            conn,
            params=(book_id, f'%{query}%')
        )
    else:
        notes = pd.read_sql_query(
            'SELECT notes.*, books.title as book_title FROM notes JOIN books ON notes.book_id = books.id WHERE content LIKE ?',
            conn,
            params=(f'%{query}%',)
        )
    conn.close()
    return notes

def add_tags(note_id, tags):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    for tag in tags:
        c.execute('INSERT INTO tags (note_id, tag_name) VALUES (?, ?)', (note_id, tag.strip()))
    conn.commit()
    conn.close()

def main():
    st.set_page_config(page_title="AI Book Notes", page_icon="📚", layout="wide")
    
    # Initialize database
    init_db()
    
    # Sidebar for adding new books
    with st.sidebar:
        st.header("📖 Add New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        if st.button("Add Book"):
            if title and author:
                add_book(title, author)
                st.success("Book added successfully!")
    
    # Main content area
    st.title("📚 AI Book Notes")
    
    # Add search functionality
    search_query = st.text_input("🔍 Search books and notes", key="search_box")
    if search_query:
        st.subheader("Search Results")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("📚 Matching Books")
            matching_books = search_books(search_query)
            if not matching_books.empty:
                for _, book in matching_books.iterrows():
                    st.write(f"- {book['title']} by {book['author']}")
            else:
                st.info("No matching books found")
                
        with col2:
            st.write("📝 Matching Notes")
            matching_notes = search_notes(search_query)
            if not matching_notes.empty:
                for _, note in matching_notes.iterrows():
                    with st.expander(f"Note from {note['book_title']}"):
                        st.write(note['content'])
            else:
                st.info("No matching notes found")
    
    # Book selection
    books = get_books()
    if not books.empty:
        st.subheader("Select a Book")
        selected_book = st.selectbox(
            "Choose a book to view/add notes",
            books['title'].tolist(),
            key="book_selector"
        )
        
        # Get selected book id
        book_id = books[books['title'] == selected_book]['id'].iloc[0]
        
        # Note taking section
        st.subheader("Add Note")
        note_content = st.text_area("Write your note", height=100)
        tags_input = st.text_input("Add tags (comma-separated)")
        
        if st.button("Save Note"):
            if note_content:
                conn = sqlite3.connect('books.db')
                c = conn.cursor()
                c.execute('INSERT INTO notes (book_id, content) VALUES (?, ?)', (book_id, note_content))
                note_id = c.lastrowid
                conn.commit()
                conn.close()
                
                if tags_input:
                    tags = [tag.strip() for tag in tags_input.split(',')]
                    add_tags(note_id, tags)
                
                st.success("Note saved successfully!")
        
        # Display existing notes
        notes = get_notes(book_id)
        if not notes.empty:
            st.subheader("📝 Your Notes")
            for idx, note in notes.iterrows():
                with st.expander(f"Note {idx + 1} - {note['created_at'][:16]}"):
                    st.write(note['content'])
                    
                    # Future AI analysis placeholder
                    st.info("🤖 AI Analysis coming soon!")
    else:
        st.info("👈 Start by adding a book in the sidebar!")

if __name__ == "__main__":
    main()