def main(req):
    with open("static-ui/index.html", "r") as f:
        html_content = f.read()
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html_content
    }
