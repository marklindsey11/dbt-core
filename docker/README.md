# Docker for dbt
This docker file is suitable for building dbt Docker images locally or using with CI/CD to automate populating a container registry.


## Building an image:
This Dockerfile can create images for the following targets, each named after the database they support:
* `dbt-core` _(no db-adapter support)_
* `dbt-postgres`
* `dbt-redshift`
* `dbt-bigquery`
* `dbt-snowflake`
* `dbt-spark`
* `dbt-all` _(installs all of the above in a single image)_

In order to build a new image, run the following docker command.
```
docker build --tag <your_image_name>  --target <target_name> <path/to/dockerfile>
```
By default the images will be populated with the most recent stable version of `dbt-core` and whatever database adapter you select.  If you need to create an image from a different you can specify it by git ref using the `--build-arg` flag like so:
```
docker build --tag <your_image_name>  --target <target_name> --build-arg <arg_name>=<git_ref> <path/to/dockerfile>
```
valid arg names are:
* `dbt_core_ref`
* `dbt_postgres_ref`
* `dbt_redshift_ref`
* `dbt_bigquery_ref`
* `dbt_snowflake_ref`
* `dbt_spark_ref`

> Note: By overiding build args it is very possible to build an image with incompatible versions of adapter and core!  TODO: provide compatibility matrix or other instructions to determine corectness of versions.

### Examples:
To build an image named "my-dbt" that supports redshift using the latest versions:
```
cd dbt-core/docker
docker build --tag my-dbt  --target dbt-redshift .
```

To build an image named "my-other-dbt" that supports bigquery using core version 0.21.latest and the bigquery adapter version 1.0.0b1:
```
cd dbt-core/docker
docker build \
  --tag my-other-dbt  \
  --target dbt-bigquery \
  --build-arg dbt_bigquery_ref=dbt-bigquery@v1.0.0b1 \
  --build-arg dbt_core_ref=dbt-core@0.21.latest  \
.
```

## Running an image in a container:
The `ENTRYPOINT` for this Dockerfile is the command `dbt` so you simply bind-mount your project to `/usr/app` and use dbt as normal:
```
docker run --mount type=bind,source=path/to/project,target=/usr/app my-dbt ls
```
> Note: bind-mount sources _must_ be an absolute path

