FROM public.ecr.aws/amazonlinux/amazonlinux:minimal

# Install Python + pip + libpq and other dependencies
RUN dnf install -y \
    python3 \
    python3-pip \
    postgresql \
    iproute \
    && dnf clean all

# Install psycopg v3 using the prebuilt binary
RUN pip3 install --no-cache-dir "psycopg[binary]"


WORKDIR /app

COPY server.py ./
COPY traffic_forwarder.py ./
COPY run.sh ./

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
