#pdf > token chunk w/ page metadata > embeddings > chroma
from pathlib import Path

import pdfplumber
import tiktoken

PDF_DIR = Path("data/pdfs")#handle os conflict
#settings to change if needed
CHUNK_TOKENS = 800
OVERLAP = 100

enc = tiktoken.get_encoding("cl100k_base") #load tokeniser 


def read_pdf(path):
    #return the whole document as list of tokens + the page num of every token
    tokens, pages = [], []
    with pdfplumber.open(path) as pdf:#guarantee file close incase oif crashf
        for page_no, page in enumerate(pdf.pages, start=1):#start from actual human understable pg1
            text = page.extract_text() or "" #return nothing if page content not suitable 
            page_tokens = enc.encode(text + "\n") #encode into tokjen IDs
            tokens.extend(page_tokens)
            pages.extend([page_no] * len(page_tokens))
    return tokens, pages

#chunkying 

def chunk(tokens, pages):
    #slide window, ~800 tok, stepping 700, neighbour chunk can share 100 buffer
    step = CHUNK_TOKENS - OVERLAP#start 700 after prev
    for start in range(0, len(tokens), step):#set start pos for each chunk
        end = min(start + CHUNK_TOKENS, len(tokens))#end @ end of doc
        yield enc.decode(tokens[start:end]), pages[start], pages[end - 1]#turn back to readable text
        #^yield creates generator, hand 1 chunk at a time, instead of crowding memoryu
        if end == len(tokens):#stop at appt time to stop next chunk from storing prev memory
            break