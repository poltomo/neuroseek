import os
import hashlib
import pysolr
import email
from email import policy
from email.parser import BytesParser

SOLR_URL = "http://localhost:8983/solr/enron_emails"
ENRON_DATASET_DIR = "/home/ics-home/neuroseek/maildir/"  # Change this to your dataset path

solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)

def extract_email_fields(file_path):
    """Extract structured fields from an email file."""
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    return {
        "id": hashlib.sha1(file_path.encode()).hexdigest(),
        "from": msg.get("From", ""),
        "to": msg.get("To", ""),
        "subject": msg.get("Subject", ""),
        "date": msg.get("Date", ""),
        "content": msg.get_body(preferencelist=('plain',)).get_content() if msg.is_multipart() else msg.get_payload()
    }

def index_enron_emails():
    """Walk through the Enron dataset directory and index emails."""
    for root, _, files in os.walk(ENRON_DATASET_DIR):
        documents = []
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    doc = extract_email_fields(file_path)
                    documents.append(doc)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        if documents:
            solr.add(documents)
            print(f"Indexed {len(documents)} emails from {root}")
    
    print("Enron dataset indexing complete!")

# Run the indexing function
index_enron_emails()
