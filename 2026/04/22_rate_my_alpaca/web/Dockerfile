# NOTE: This hash is pinned to avoid version and environment differences.
FROM php:8.5-apache@sha256:06a15077490436c599e067e3a646f9ba74b3798c82ebfbf635ba5e5a8bae1e9d

COPY flag.txt flag.txt
RUN mv flag.txt /flag-$(md5sum flag.txt | awk '{print $1}').txt

COPY uploads.conf /etc/apache2/conf-available/uploads.conf
RUN a2enconf uploads
RUN mkdir /var/www/uploads
COPY index.php /var/www/html/index.php

RUN chmod -R 777 /var/www/