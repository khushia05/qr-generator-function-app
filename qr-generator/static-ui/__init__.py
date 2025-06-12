import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(index_path, "r") as f:
        html = f.read()
    return func.HttpResponse(html, mimetype="text/html")
