#!/usr/bin/env python
# coding: utf-8

# ## Query Global Land product catalogue via OpenSearch API and download the products
# 
# This notebook shows how to query the Global Land product catalogue service, that implements a standardized [OpenSearch interface](http://docs.opengeospatial.org/is/17-047r1/17-047r1.html).
# 
# OpenSearch is a self-describing search. This means that the service describes how it can be used, which search filters (keys and allowed values) are available.
# For example: 
# * [overall API description](https://globalland.vito.be/catalogue/description)
# * [description for searching Burnt Area collection](https://globalland.vito.be/catalogue/description?collection=clms_global_ba_300m_v3_daily_netcdf)
# 
# The catalogue service can be used in a [Python client](https://github.com/VITObelgium/terracatalogueclient), that is available from VITO's [Terrascope](https://terrascope.be/en) platform, which allows for easy integration in Python notebooks and Python-based processing chains.
# 
# In this demo, we'll show you how to search for Global Land products through this OpenSearch API and then download them.
# 
# **Important!**
# We'll use the new collection of daily Burnt Area 300m v3.1.1 products as example. This API is a recent development - more product collections will become available in the course of 2023.

# ### Table of contents
# * [Install & import packages](#install-import)
# * [Discover collections](#discover-collections)
# * [Search products](#search-products)
# * [Download products](#download-products)

# #### Install & import packages <a class="anchor" id="install-import"></a>

# Let's start with installing the Python catalogue client from the python package repository:

# In[1]:


get_ipython().system('python3 -m pip install --user --quiet --index-url=https://artifactory.vgt.vito.be/api/pypi/python-packages/simple terracatalogueclient==0.1.16')


# On the Terrascope virtual machines and Jupyter notebook environment, the catalogue client package is pre-installed for your convenience.

# Next, we import some required packages and initialize the catalogue client.

# In[2]:


from terracatalogueclient import Catalogue
from terracatalogueclient.config import CatalogueConfig, CatalogueEnvironment


# Copy the configuration file from the Github repository to the same folder.
# Then use it to configure the catalogue client to query Global Land's catalogue.

# In[3]:


config = CatalogueConfig.from_environment(CatalogueEnvironment.CGLS)
catalogue = Catalogue(config)


# #### Discover collections <a class="anchor" id="discover-collections"></a>

# The get_collections() call can be used to discover which collections of Global Land products.
# At this moment, only the products for the daily Burnt Area v3.1.1 collection are available. All other Global Land collections will be added to this API.

# In[4]:


import pandas as pd
collections = catalogue.get_collections()

rows = []
for c in collections:
    rows.append([c.id, c.properties['title']])

df = pd.DataFrame(data = rows, columns = ['Identifier', 'Description'])
df.style.set_properties(**{'text-align': 'left'})


# #### Search products <a class="anchor" id="search-products"></a>

# Using one of the above collection identifiers, let's search for the available daily burnt area products.
# 
# The get_products() call supports filtering time period that the product covers (start/end parameters), or date when the file was last updated (modificationDate)

# In[5]:


import pandas as pd
import datetime as dt

rows = []
products = catalogue.get_products(
    "clms_global_ba_300m_v3_daily_netcdf",
    start=dt.date(2023, 9, 1),
    end=dt.date(2023, 9, 3),
)
for product in products:
    rows.append([product.id, product.data[0].href, (product.data[0].length/(1024*1024))])

df = pd.DataFrame(data = rows, columns = ['Identifier', 'URL', 'Size (MB)'])
df.style.set_properties(**{'text-align': 'left'})


# For a list of available search options, see the opensearch description document or the available help:
# 
# *help(catalogue.get_products)*

# #### Download products <a class="anchor" id="download-products"></a>

# The product download is free and fully open - it does not require any username or password.
# 
# Note that the above get_products() call returns a Python generator! 
# If you want to be able to iterate over the results more than once, you can convert it to a list.
# Keep in mind that such a conversion loads all results in memory. If the number of products found is very high (e.g. hourly LST has tens of thousands of files), then the list can take up a lot of the memory.

# In[6]:


product_list = list(catalogue.get_products(
    "clms_global_ba_300m_v3_daily_netcdf",
    start=dt.date(2023, 9, 1),
    end=dt.date(2023, 9, 3),
))


# Let's actually download the files to the directory where this notebook resides.
# 
# Depending on the connection speed and data volume, this can take a few minutes.

# In[7]:


catalogue.download_products(product_list, './')


# Finally, let's check if the data files are downloaded.
# 
# The download_products() call stores the downloaded files in folders, named after the product identifier.

# In[8]:


import os
os.listdir('./c_gls_BA300-NRT_202309010000_GLOBE_S3_V3.1.1/')


# **Note**
# 
# This demo is designed to download a small set of files, directly to the (limited) workspace of this notebook.
# 
# To download larger sets of files
# * download this code as a stand-alone Python script (CGLS_catalogue_and_download.py), modify it and run it e.g. on your computer or your [Terrascope Virtual Machine](https://terrascope.be/en/services)
# * or save the list of URLs as a text file and provide that as input to download tools like [WinWget](https://winwget.sourceforge.net/), command-line [wget](https://www.gnu.org/software/wget/) or [curl](https://curl.se/)
