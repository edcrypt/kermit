FROM crux/python:onbuild

RUN make

ENTRYPOINT ["./bin/kermit"]
