#!/usr/bin/env python
# coding: utf-8

# # Exploring Ebay Car Sales Data 

# ### We'll be working with a dataset of used cars from eBay Kleinanzeigen, a classifieds section of the German eBay website
# 

# In[3]:


import pandas as pd
import numpy as np


# In[4]:


autos = pd.read_csv("autos.csv",encoding="Latin-1")


# In[5]:


autos


# In[6]:


autos.info()


# In[7]:


print(autos.head(5))


# ## We made the following observations:
# ### The dataset contains 20 columns, most of which are strings.
# ### Some columns have null values, but none have more than ~20% null values.
# ### The column names use camelcase instead of Python's preferred snakecase, which means we can't just replace spaces with underscores.

# In[8]:


column_names = autos.columns
print(column_names)


# In[9]:


corrections = {"yearOfRegistration":"registration_year", 
               "monthOfRegistration":"registration_month",
              "notRepairedDamage":"unrepaired_damage",
              "dateCreated":"date_created",
              "dateCrawled":"date_crawled",
               "name":"name","seller":"seller",
               "offerType":"offer_type",
               "price":"price", "abtest":"abtest", 
               "vehicleType":"vehicle_type",
               "gearbox":"gearbox", "brand":"brand",
               "powerPS":"power_ps",
               "model":"model","odometer":"odometer",
               "fuelType":"fuel_type",
               "nrOfPictures":"num_pictures",
               "postalCode":"postal_code", "lastSeen":"last_seen"}


# In[10]:


column_names = column_names.map(corrections)
print(column_names)


# In[11]:


autos.columns = column_names
print(autos.columns)


# In[12]:


print(autos.head(3))


# ## The column names were changed from camel case to snake case for easier data handling.
# 

# In[13]:


autos.describe(include='all')


# ## Some things to be done
# ### columns that have mostly one value that are candidates to be dropped: num_pictures, offer_type, seller
# ### columns with numeric data stored as text that needs to be cleaned: price, odometer 

# In[14]:


autos.drop(["num_pictures","offer_type","seller"],axis=1,inplace=True)


# In[15]:


autos["price"] = (autos["price"]
                           # .str.replace("km","")
                            .str.replace("$","")
                            .str.replace(",","")
                            .astype(int)
                    )

autos.rename({"odometer":"odometer_km"}, axis=1, inplace=True)


# In[16]:


autos["odometer_km"] = (autos["odometer_km"]
                            .str.replace("km","")
                           # .str.replace("$","")
                            .str.replace(",","")
                            .astype(int)
                    )


# In[17]:


print(autos["price"].describe())


# In[18]:


print(autos["price"].value_counts().sort_index(ascending=False).head(20))

### seeing that the maximum value is too high, I looked at the top 20 prices and saw that there was an irregular jump from 350000 to 999990 so I deicided to make the cutoff at 350000.
# In[19]:


autos.drop(autos[autos["price"].between(999990,99999999)].index,inplace=True)


# In[20]:


print(autos.shape)


# In[21]:


print(autos["price"].describe())


# ### The mean went down from 9840 to 5721 but the median and the lower and upper quartiles did not change.

# In[22]:


print(autos["odometer_km"].describe())


# In[23]:


print(autos["registration_year"].describe())


# ### the registration year has a min of 1000 which is weird because cars weren't invented then and the max is 9999, which is also inaccurate

# In[24]:


print(autos["registration_year"].sort_values().head(10))


# ### The cutoff will be at 1910 because cars were being manufactured starting early 1900s and at 2016 because the data was compiled in 2016 so cars listed shouldn't have been registered after that.

# In[25]:


autos.drop(autos[(autos["registration_year"]>2016) | (autos["registration_year"]<1910)].index,inplace=True)


# In[26]:


print(autos["registration_year"].value_counts())


# In[27]:


print(autos.shape)


# In[28]:


brands = autos["brand"].unique()


# In[29]:


mean_price_by_brand = dict()
for brand in brands:
    rows = autos[autos["brand"]==brand]
    mean_price = round(rows["price"].mean())
    mean_price_by_brand[brand] = mean_price
print(mean_price_by_brand)


# In[30]:


print(sorted(mean_price_by_brand.items(), key = lambda kv: kv[1]))


# ### First I decided to find the mean price for all the brands and then create another dictionary for the top 20

# In[31]:


brands=autos["brand"].value_counts().head(20).index
print(brands)


# In[32]:


mean_price_by_brand = dict()
for brand in brands:
    rows = autos[autos["brand"]==brand]
    mean_price = round(rows["price"].mean())
    mean_price_by_brand[brand] = mean_price
print(mean_price_by_brand)


# In[33]:


print(sorted(mean_price_by_brand.items(), key = lambda kv: kv[1]))


# In[34]:


brands=autos["brand"].value_counts().head(6).index
mean_price_by_brand = dict()
for brand in brands:
    rows = autos[autos["brand"]==brand]
    mean_price = round(rows["price"].mean())
    mean_price_by_brand[brand] = mean_price
print(sorted(mean_price_by_brand.items(), key = lambda kv: kv[1]))


# In[35]:


bmp_series = pd.Series(mean_price_by_brand)
print(bmp_series)


# In[36]:


df = pd.DataFrame(bmp_series, columns=['mean_price'])
df


# In[37]:


mean_mileage = dict()
for brand in brands:
    rows = autos[autos["brand"]==brand]
    mean_miles = round(rows["odometer_km"].mean())
    mean_mileage[brand] = mean_miles
print(sorted(mean_mileage.items(), key = lambda kv: kv[1]))


# In[40]:


bmp_series = pd.Series(mean_mileage)
df["mean_mileage"] = bmp_series
df


# In[39]:


print(autos.head(3))

