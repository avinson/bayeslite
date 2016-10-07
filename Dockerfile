FROM        ubuntu:14.04

MAINTAINER  Baxter Eaves

RUN         apt-get update
RUN         apt-get install -y git dialog wget nano python2.7-dev python-pip libboost1.54-all-dev libatlas-dev libblas-dev liblapack-dev apt-utils ccache gfortran openssh-client

# pip install various python libraries
RUN         pip install -U distribute && pip install cython && pip install numpy && pip install scipy && pip install patsy && pip install pandas && pip install statsmodels && pip install pytest && pip install cmd2 && pip install pexpect

WORKDIR     /home/bayeslite

ENV         MYPASSWORD bayeslite
ENV         USER bayeslite

# make a nice readme
RUN         echo "\n\nroot password is $MYPASSWORD" >> readme.txt

# show readme at login
RUN         echo "cat ~/readme.txt" >> .bashrc && echo "export PYTHONPATH=/home/bayeslite/crosscat" >> .bashrc

# create a root and bayeslite password
RUN         echo "root:$MYPASSWORD" | chpasswd
RUN         useradd bayeslite
RUN         echo "bayeslite:$MYPASSWORD" | chpasswd
ENV         HOME /home/bayeslite

RUN         cd /home/bayeslite && git clone https://github.com/probcomp/crosscat.git
RUN         cd /home/bayeslite && git clone https://github.com/probcomp/bayeslite.git

# install crosscat and bayeslite
RUN         cd /home/bayeslite/crosscat && python setup.py install
RUN         cd /home/bayeslite/bayeslite && python setup.py install

RUN         chown -R bayeslite /home/bayeslite
USER        bayeslite

CMD         /bin/bash
