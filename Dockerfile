FROM quay.io/pypa/manylinux1_x86_64

WORKDIR /tmp
RUN git clone -b 'v1.15.1' --single-branch --depth=1 https://github.com/quickfix/quickfix
RUN /opt/python/cp37-cp37m/bin/python -m pip install -I robotframework==3.1

RUN mkdir /tmp/quickfix-doc
COPY setup.py /tmp/quickfix-doc/
COPY quickfix_doc /tmp/quickfix-doc/quickfix_doc

WORKDIR /tmp/quickfix-doc
RUN for i in /opt/python/*;do "$i/bin/pip" install .;done

COPY acceptance.robot /tmp/quickfix-doc/
RUN mkdir /tmp/quickfix-doc/output
WORKDIR /tmp/quickfix-doc/output
CMD ["/opt/python/cp37-cp37m/bin/python", "-m", "robot", "/tmp/quickfix-doc/acceptance.robot"]
