#
#Docker file to bind the ssh keyfile
#
FROM keybox:ldap
MAINTAINER Selvan R "selvan@cloud-kinetics.com"

RUN mkdir -p /opt/keys
COPY sshkeys/* /opt/keys/

EXPOSE 8443

WORKDIR /opt/KeyBox-jetty/
CMD ./startKeyBox.sh
