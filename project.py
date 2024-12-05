import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Function to extract keywords
def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    return keywords

# Function to identify pros and cons
def identify_pros_cons(sentences):
    pros = []
    cons = []
    for sentence in sentences:
        sentiment = TextBlob(str(sentence)).sentiment.polarity
        if sentiment > 0:
            pros.append(str(sentence))
        elif sentiment < 0:
            cons.append(str(sentence))
    return pros, cons

def summarize_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text!")
        return

    blob = TextBlob(input_text)

    # Sentiment Analysis
    sentiment = blob.sentiment.polarity
    sentiment_result = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

    # Word and Sentence Count
    sentences = blob.sentences
    word_count = len(blob.words)
    sentence_count = len(sentences)

    # Keyword Extraction
    keywords = extract_keywords(input_text)

    # Pros and Cons Identification
    pros, cons = identify_pros_cons(sentences)

    # Generate Summary
    summarized_text = " ".join(str(s) for s in sentences[:2]) if len(sentences) > 1 else input_text

    # Display Results
    summary_output.set(summarized_text)
    sentiment_label.config(text=f"Sentiment: {sentiment_result} ({sentiment:.2f})")
    word_count_label.config(text=f"Words: {word_count}")
    sentence_count_label.config(text=f"Sentences: {sentence_count}")
    pros_label.config(text=f"Pros: {'; '.join(pros) if pros else 'None'}")
    cons_label.config(text=f"Cons: {'; '.join(cons) if cons else 'None'}")
    keywords_label.config(text=f"Keywords: {', '.join(keywords)}")

def clear_text():
    text_input.delete("1.0", tk.END)
    summary_output.set("")
    sentiment_label.config(text="Sentiment: N/A")
    word_count_label.config(text="Words: 0")
    sentence_count_label.config(text="Sentences: 0")
    pros_label.config(text="Pros: N/A")
    cons_label.config(text="Cons: N/A")
    keywords_label.config(text="Keywords: N/A")

def copy_to_clipboard():
    summary = summary_output.get()
    if summary:
        root.clipboard_clear()
        root.clipboard_append(summary)
        root.update()  # Ensure the clipboard is updated
        messagebox.showinfo("Copy Success", "Summary copied to clipboard!")
    else:
        messagebox.showwarning("Copy Error", "No summary to copy!")

# GUI Setup
root = tk.Tk()
root.title("Review Summarizer with Sentiment Analysis")
root.geometry("700x600")

# Input Area
tk.Label(root, text="Enter Review:").pack(anchor="w", padx=10)
text_input = tk.Text(root, height=8, width=85)
text_input.pack(padx=10, pady=5)

# Output Area
tk.Label(root, text="Summary:").pack(anchor="w", padx=10)
summary_output = tk.StringVar()
tk.Label(root, textvariable=summary_output, wraplength=650, bg="white", anchor="nw", height=6, width=85).pack(padx=10, pady=5)

# Information Labels
sentiment_label = tk.Label(root, text="Sentiment: N/A", anchor="w")
sentiment_label.pack(anchor="w", padx=10)

word_count_label = tk.Label(root, text="Words: 0", anchor="w")
word_count_label.pack(anchor="w", padx=10)

sentence_count_label = tk.Label(root, text="Sentences: 0", anchor="w")
sentence_count_label.pack(anchor="w", padx=10)

pros_label = tk.Label(root, text="Pros: N/A", anchor="w", wraplength=650, justify="left")
pros_label.pack(anchor="w", padx=10)

cons_label = tk.Label(root, text="Cons: N/A", anchor="w", wraplength=650, justify="left")
cons_label.pack(anchor="w", padx=10)

keywords_label = tk.Label(root, text="Keywords: N/A", anchor="w", wraplength=650, justify="left")
keywords_label.pack(anchor="w", padx=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Summarize", command=summarize_text, width=15).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Clear", command=clear_text, width=15).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Copy", command=copy_to_clipboard, width=15).grid(row=0, column=2, padx=5)

# Run the App
root.mainloop()