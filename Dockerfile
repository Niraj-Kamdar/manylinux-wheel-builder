FROM quay.io/pypa/manylinux2010_x86_64
COPY entrypoint.py /entrypoint.py
CMD /opt/python/cp37-cp37m/bin/python /entrypoint.py