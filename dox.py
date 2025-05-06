import streamlit as st
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
import docx2txt
import nltk
import os
import sentencepiece


# Download NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Initialize the summarizer and question generator models
summarizer = pipeline('summarization')
tokenizer = T5Tokenizer.from_pretrained('valhalla/t5-small-qg-hl')
model = T5ForConditionalGeneration.from_pretrained('valhalla/t5-small-qg-hl')

def read_docx(uploaded_file):
    # Simply use docx2txt to extract text from the document
    text = docx2txt.process(uploaded_file)
    return text

def summarize_text(text):
    # Break text into chunks if too long for summarizer
    max_chunk_size = 1000
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    
    summaries = []
    for chunk in chunks:
        if len(chunk.strip()) > 100:  # Only summarize chunks with sufficient content
            summary = summarizer(chunk, max_length=100, min_length=25, do_sample=False)
            summaries.append(summary[0]['summary_text'])
    
    return " ".join(summaries)

def generate_questions(text):
    questions = []
    
    # Split the text into sentences
    sentences = nltk.tokenize.sent_tokenize(text)
    
    # Generate a question for each substantive sentence (longer than 20 chars)
    for sentence in sentences:
        if len(sentence) > 20:  # Only process meaningful sentences
            inputs = tokenizer.encode("generate question: " + sentence, return_tensors='pt')
            outputs = model.generate(inputs, max_length=200, do_sample=True, top_p=0.95, top_k=60)
            question = tokenizer.decode(outputs[0], skip_special_tokens=True)
            questions.append(question)
    
    # Limit to 10 questions to prevent overwhelming the user
    return questions[:10]

st.title('Text Summarizer and Question Generator')

uploaded_file = st.file_uploader("Upload a .docx file", type="docx")

if uploaded_file is not None:
    text = read_docx(uploaded_file)
    
    # Display original text with some styling
    st.subheader('Original Text:')
    st.text_area("Document Content", text, height=250)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('Generate Summary'):
            with st.spinner('Generating summary...'):
                summary = summarize_text(text)
                st.subheader('Summary:')
                st.write(summary)
                
                # Option to download summary
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

    with col2:
        if st.button('Generate Questions'):
            with st.spinner('Generating questions...'):
                questions = generate_questions(text)
                st.subheader('Generated Questions:')
                
                if not questions:
                    st.info("Couldn't generate meaningful questions from this document.")
                else:
                    for i, question in enumerate(questions, start=1):
                        st.write(f"Question {i}: {question}")
                    
                    # Option to download questions
                    questions_text = "\n".join([f"Question {i}: {q}" for i, q in enumerate(questions, start=1)])
                    st.download_button(
                        label="Download Questions",
                        data=questions_text,
                        file_name="questions.txt",
                        mime="text/plain"
                    )
else:
    st.info("Please upload a .docx file to get started.")

# Add footer with instructions
st.markdown("---")
st.markdown("**Instructions:** Upload a Word document (.docx) file and click on either 'Generate Summary' or 'Generate Questions' to analyze your text.")