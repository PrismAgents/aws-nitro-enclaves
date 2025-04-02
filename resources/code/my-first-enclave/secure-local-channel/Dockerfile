FROM public.ecr.aws/amazonlinux/amazonlinux:2023

# Install Python and pip
RUN dnf install -y \
    python3 \
    python3-pip \
    iproute \
    && dnf clean all

# Install pg8000 (pure-Python PostgreSQL driver)
RUN pip3 install --no-cache-dir pg8000

WORKDIR /app

COPY server.py ./
COPY traffic_forwarder.py ./
COPY run.sh ./

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
