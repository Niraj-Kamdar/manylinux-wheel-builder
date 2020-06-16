FROM quay.io/pypa/manylinux2010_x86_64
COPY entrypoint.py /entrypoint.py
RUN /opt/python/cp37-cp37m/bin/pip install twine
CMD /opt/python/cp37-cp37m/bin/python /entrypoint.py