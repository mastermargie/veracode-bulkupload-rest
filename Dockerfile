FROM python:3.9.5-windowsservercore

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD [ "python", "/app/veracode_bulkupload_rest.py" ]
