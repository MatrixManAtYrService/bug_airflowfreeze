FROM apache/airflow:2.1.3
USER root
RUN apt update && apt install -y curl

# kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# kubeconfig
RUN mkdir -p ~/.kube
COPY ./config /home/airflow/.kube/config
ENV KUBECONFIG=/home/airflow/.kube/config
RUN chown airflow /home/airflow/.kube/config

COPY increment.py $AIRFLOW_HOME/dags/increment.py


USER airflow

RUN pip install sh
