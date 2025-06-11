import logging
import azure.functions as func
import qrcode
import io
import base64

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('QR Function triggered.')

    data = req.params.get('data')
    if not data:
        return func.HttpResponse("Please pass 'data' query string", status_code=400)

    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()
    base64_img = base64.b64encode(img_bytes).decode('utf-8')

    return func.HttpResponse(
        f'<img src="data:image/png;base64,{base64_img}"/>',
        mimetype="text/html"
    )