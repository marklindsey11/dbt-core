##
#  Generic dockerfile for dbt image building.  
#  See README for operational details
##

##
# base image (abstract)
##
FROM python:3.9-slim-bullseye as base

# Build args
# TODO: Can we automate this so it doesn't need to be updated with each major rev?
# N.B. dbt-postgres is currently found in the core codebase so a value of dbt-core@1.0.latest is correct
ARG dbt_core_ref=dbt-core@1.0.latest
ARG dbt_postgres_ref=dbt-core@1.0.latest
ARG dbt_redshift_ref=dbt-redshift@1.0.latest
ARG dbt_bigquery_ref=dbt-bigquery@1.0.latest
ARG dbt_snowflake_ref=dbt-snowflake@1.0.latest
ARG dbt_spark_ref=dbt-spark@1.0.latest
ARG dbt_spark_version=all
ARG dbt_third_party

# System setup
# TODO: python-dev libsasl2-dev gcc unixodbc-dev are only needed for spark... make more selective
RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y --no-install-recommends \
    git \
    ssh-client \
    software-properties-common \
    make \
    build-essential \
    ca-certificates \
    libpq-dev \
    python-dev \
    libsasl2-dev \
    gcc \
    unixodbc-dev \
  && apt-get clean \
  && rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/*

# Env vars
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

# Update python
RUN python -m pip install --upgrade pip setuptools --no-cache-dir

# Set docker basics
WORKDIR /usr/app/dbt/
VOLUME /usr/app
ENTRYPOINT ["dbt"]

##
# dbt-core
##
FROM base as dbt-core
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir

##
# dbt-postgres
##
FROM base as dbt-postgres
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_postgres_ref}#egg=dbt-postgres&subdirectory=plugins/postgres" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir


##
# dbt-redshift
##
FROM base as dbt-redshift
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_redshift_ref}#egg=dbt-redshift" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir

##
# dbt-bigquery
##
FROM base as dbt-bigquery
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_bigquery_ref}#egg=dbt-bigquery" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir


##
# dbt-snowflake
##
FROM base as dbt-snowflake
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_snowflake_ref}#egg=dbt-snowflake" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir


##
# dbt-spark
##
FROM base as dbt-spark
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_spark_ref}#egg=dbt-spark[${dbt_spark_version}]" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir


##
# dbt-third-party
##
FROM base as dbt-third-party
RUN python -m pip install "${dbt_third_party}" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir


##
# dbt-all
##
FROM base as dbt-all
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_postgres_ref}#egg=dbt-postgres&subdirectory=plugins/postgres" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_redshift_ref}#egg=dbt-redshift" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_bigquery_ref}#egg=dbt-bigquery" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_snowflake_ref}#egg=dbt-snowflake" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_spark_ref}#egg=dbt-spark[${dbt_spark_version}]" --no-cache-dir
RUN python -m pip install "git+https://github.com/dbt-labs/${dbt_core_ref}#egg=dbt-core&subdirectory=core" --no-cache-dir

