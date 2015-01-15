FROM dockerbase/devbase-spark
MAINTAINER Sven Kreiss <me@svenkreiss.com>

RUN sudo apt-get update && \
    sudo apt-get install -y python-pip python-dev python-virtualenv \
                            pkg-config libpng-dev libfreetype6-dev \
                            python-matplotlib && \
    sudo apt-get clean

# now add code that changes (not cached) and install the rest of the
# dependencies
ADD . /home/devbase/databench_spark
WORKDIR /home/devbase/databench_spark
RUN sudo pip install -r requirements.txt

EXPOSE 5000
CMD ["databench", "--host=0.0.0.0"]
