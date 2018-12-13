FROM tensorflow/tensorflow:1.12.0-gpu

WORKDIR /app

COPY requirements_http.txt ./
RUN pip install --no-cache-dir -r requirements_http.txt

COPY Salient-Object-Detection Salient-Object-Detection
COPY *.py ./

CMD [ "gunicorn", \
	"-b", "0.0.0.0:5001", \
	"--timeout=120", \
	"--access-logfile=-", \
	"--error-logfile=-", \
	"--log-level=DEBUG", \
	"image2salience_http:app" ]