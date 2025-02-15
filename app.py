from flask import Flask, request, render_template_string
import pysolr

app = Flask(__name__)

# Configure the Solr instance (replace with your Solr core URL)
SOLR_URL = "http://localhost:8983/solr/mycollection"
solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)

# Basic HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NeuroSeek Search</title>
</head>
<body>
    <h1>Solr Search</h1>
    <form method="GET">
        <input type="text" name="q" placeholder="Enter search query" required>
        <button type="submit">Search</button>
    </form>
    
    {% if results %}
        <h2>Results:</h2>
        <ul>
        {% for doc in results %}
            <li><strong>{{ doc['id'] }}</strong>: {{ doc['title'][0] if 'title' in doc else 'No title' }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = []
    
    if query:
        results = solr.search("title:"+query, rows=10)
    print(list(results))
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(debug=True,port=5000)

    solr.add([
        {
            "id": "test_1",
            "title": "test text 1",
        }
    ])