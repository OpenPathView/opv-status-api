FROM opv-tasks

ENV OPV_STATUS-API_PORT 5000

COPY . /source/opv-status-api

WORKDIR /source/opv-status-api

RUN pip3 install -r requirements.txt && \
python3 setup.py install

ENV LC_CTYPE "en_US.UTF-8"

EXPOSE 5001:5001

CMD ["opv-status-api"]

