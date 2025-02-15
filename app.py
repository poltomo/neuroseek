from flask import Flask, request, render_template_string
import pysolr
from mypyc.ir.ops import Integer
from sentence_transformers import CrossEncoder

from crossEncoder import initCrossEncoder
from sentenceTransformer import initSentenceTransformer

app = Flask(__name__)

# Configure the Solr instance (replace with your Solr core URL)
SOLR_URL = "http://localhost:8983/solr/enron_emails"
solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)

# Basic HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>neuroseek</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            text-align: center;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }
        h1 {
            font-size: 48px;
            color: #000000;
            margin-top: 50px;
        }
        form {
            margin: 20px auto;
        }
        input[type="text"] {
            width: 400px;
            padding: 10px;
            font-size: 18px;
            border: 1px solid #ccc;
            border-radius: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 18px;
            border: none;
            background-color: #f8f8f8;
            cursor: pointer;
            border-radius: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            font-size: 16px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <h1>neuroseek</h1>
    <form method="GET">
        <input type="text" name="q" placeholder="Enter search query" required>
        <button type="submit">Search</button>
    </form>
    
    {% if results %}
        <h2>Results:</h2>
        <ul>
        {% for doc,rk in results %}
            <li><strong>{{ doc['id'] }}</strong> sim {{ rk['score'] }}: {{ doc['content'][0] if 'content' in doc else 'No content' }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""
HTML_TEMPLATE_OLD = """
<!DOCTYPE html>
<html>
<head>
    <title>neuroseek</title>
</head>
<body>
    <h1>neuroseek</h1>
    <form method="GET">
        <input type="text" name="q" placeholder="Enter search query" required>
        <button type="submit">Search</button>
    </form>
    
    {% if results %}
        <h2>Results:</h2>
        <ul>
        {% for doc,rk in results %}
            <li><strong>{{ doc['id'] }}</strong> sim {{ rk['score'] }}: {{ doc['content'][0] if 'content' in doc else 'No content' }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

model = initCrossEncoder()
@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if query:
        results = list(solr.search("content:"+query, rows=10))
        contents = []
        for doc in results:
            if "content" in doc:
                contents.append(doc["content"][0])
        ranking = model.rank(query, contents)
        # print(list(results))
    return render_template_string(HTML_TEMPLATE,
                                  results=zip(sorted(results,key=lambda x:-ranking[results.index(x)]["score"]),
                                           sorted(ranking,key=lambda x:-x["score"])) if query else None)

if __name__ == "__main__":
    app.run(debug=True,port=5000)
    solr.add([
        {
            "id": "test_1",
            "title": "test text 1",
            "content": "ribbit rabbit",
        }
    ])