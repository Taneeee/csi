from flask import Flask, request, jsonify
import PyPDF2

app = Flask(__name__)
def chatbot_response(query, pdf_text):
    
    if query.lower() in pdf_text.lower():
        return f"I found something related to '{query}' in the document."
    else:
        return f"Sorry, I couldn't find anything about '{query}' in the document."

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    pdf_file = request.files['pdf']
    extracted_text = extract_text_from_pdf(pdf_file)
    
    
    app.config['PDF_TEXT'] = extracted_text
    
    return jsonify({"message": "PDF text extracted successfully", "text_length": len(extracted_text)}), 200


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    query = data['query']
    
  
    if 'PDF_TEXT' not in app.config:
        return jsonify({"error": "No PDF uploaded yet"}), 400
    
    pdf_text = app.config['PDF_TEXT']
    
 
    response = chatbot_response(query, pdf_text)
    
    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
