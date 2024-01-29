# Data Pipelines

This package aims to provide a set of Python code for geospatial format conversion, as well as the ability to create your own STAC Catalog and interact with your data in an object store.

---

## Prerequisites
You can run this script by setting the credentials for the BUCKET Object Store manually.
Or you can set the following environment variables:
- BUCKET_TOKEN
- BUCKET_SECRET
- BUCKET_API_URL

Create and set up a pyenv environment:
``` shell
pyenv virtualenv data_pipelines
pyenv local data_pipelines
```

Install the package and requirements:
``` shell
pip install -e .
```

---

## Data Conversion

Currently, code for converting the following data formats has been implemented:

- Input: TIF, NETCDF, GeoJSON
- Output: COG

### How to Use

Import the function and initialize the variables you will use:

``` python
from data_pipelines.data_pipelines import DataFormatConverter

input_file = '../../raw_data/shipborne_2018.tif'
input_format = 'tif'
output_format = 'cog'
output_filename = 'shipborne_2018.tif'
output_filepath = '../../raw_data/'
bucket_name = 'haig-fras'
bucket_folder = 'layers/bathymetry/shipborne_2018'
```

Create an instance of the class and perform the data conversion:

``` python
d = DataFormatConverter(input_file=input_file, input_format=input_format)

d.convert_format(output_filename=output_filename,
                 output_filepath=output_filepath,
                 output_format=output_format,
                 upload_file=True,
                 bucket_name=bucket_name,
                 bucket_folder=bucket_folder)
```

---

## Work with Files in an Object Store

This package allows you to perform some simple actions in an object store, such as ls, cp, mv, rm, and upload.

### How to Use

Import the function:

``` python
from access_bucket.access_bucket import AccessBucket
```

If you did not set the ENV variables, you need to pass these values to the class constructor:

``` python
a = AccessBucket(aws_access_key_id,
                 aws_secret_access_key,
                 endpoint_url,
                 bucket)
```

If you set the ENV variables, you just pass:

``` shell
a = AccessBucket(bucket)
```

To perform operations in the bucket:

``` shell
# List files
a.ls(bucket_folder='layers/seabed_images/hf2012/images', prefix="M58_10441297_1298774480")

# Remove files
a.rm(bucket_folder='frontend/assets', verbose=1)

# Create a directory
a.mkdir(bucket_folder='layers/sidescan/sidescan_2012')

# Move files
a.mv(
    bucket_folder='layers/bathymetry/',
    output_folder='layers/seabed_images/nbn',
    verbose=1,
)

# Rename files
a.mv(
    bucket_folder='layers/seabed_images/jncc/images',
    sufix='.JPG',
    replace=['.JPG', '.jpg'],
    verbose=1
)

# Copy files
a.mv(
    bucket_folder='mbtiles',
    output_folder='layers/seabed_habitats/habitat_map',
    input_filename='habitats_new-65536.mbtiles',
    output_filename='habitat_map.mbtiles'
)

# Upload files
a.upload(filenames, path, bucket_folder)
```

The notebook [code_test.ipynb](access_bucket/notebooks/code_test.ipynb) provides usage examples.

---

## Create STAC Catalogs

To create STAC Catalogs, you must first create a set of configuration files called "metadata."

Metadata files consist of a primary JSON file representing the main catalog. Depending on the data group, if you want to add sub-catalogs to your catalog, you can create auxiliary JSON files.

The main catalog file should follow the format described in the [example file](create_stac/templates/main_template.json). This file provides examples of adding different types of data to the STAC, such as COG files, GeoJSON, PNG files, WMS links, and links to Asset ION.

### How to Use

To generate the STAC Catalog, follow these steps:

- Create the metadata folder following the example file. In the same folder, there is also an example for adding a [sub-catalog](create_stac/templates/subcatalog_template.json) to your main catalog.
- Import the function and create an instance of the class:

``` python
from create_stac.stac_gen import STACGen

# Create an instance of the class and provide the path to your metadata files (JSON files)
s = STACGen(metadata_path='../metadatas/')
```

- Generate the STAC Catalog. If you did not set the ENV variables, you need to pass these values at this step:

```python
s.stac_gen(upload_bucket=True,
           stac_path='stac',
           aws_access_key_id=aws_access_key_id,
           aws_secret_access_key=aws_secret_access_key,
           endpoint_url=endpoint_url
          )
```

- If you set the ENV variables, you can just pass:

```python
s.stac_gen(upload_bucket=True,
           stac_path='stac',
          )
```

- In the end, a folder called "stac" will be created with your STAC Catalog.

---

## Convert STAC Catalogs to JSON for use in a Web Application

To use STAC Catalogs in a frontend, importing all these files may take a long time. To speed up this process, a set of codes has been created to convert the STAC into a single, user-friendly JSON format accepted by the web application. Currently, we are converting the STAC to a JSON format accepted by the "Haig Fras Digital Twin" project.

### How to Use

To generate the JSON file, follow these steps:

- Import the function and create an instance of the class:

``` python
from create_stac.stac_convert import STACConvert

c = STACConvert(bucket_path=''
               stac_path='stac')
```

- Generate the JSON file from the STAC Catalog:

```python
c.convert()
```

- Save the final JSON file and upload it to the object store. If you did not set the ENV variables, you need to pass these values at this step:

```python
c.save_and_upload(filename='layers.json',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  endpoint_url=endpoint_url)
```

- If you set the ENV variables, you can just pass:

```python
c.save_and_upload(filename='layers.json')
```

- In the end, a file called "layers.json" will be created and ready to be used by the web application.