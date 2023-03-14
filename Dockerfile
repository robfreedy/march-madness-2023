FROM prefecthq/prefect:2-python3.10

COPY requirements.txt .

COPY teams.json .

RUN pip install -r requirements.txt