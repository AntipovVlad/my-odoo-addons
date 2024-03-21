FROM odoo:15.0
WORKDIR /odoo-main
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
