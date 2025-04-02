FROM public.ecr.aws/amazonlinux/amazonlinux:minimal

# Install Python + pip + libpq and other dependencies
RUN dnf install -y \
    python3 \
    python3-pip \
    libpq \
    iproute

# Install psycopg3 binary wheel
RUN pip install "psycopg[binary]"

WORKDIR /app

COPY server.py ./
COPY traffic_forwarder.py ./
COPY run.sh ./

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
