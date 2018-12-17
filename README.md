# HouseFinder
Looking for a place to rent can be hassle and take a huge amount of hours. This application attempts to help people in this process.

This REST API is used for an application that finds you the prettiest apartment or house to rent in a given area.
The API is used to store data about property listings from the british house listing site zoopla. It allows you to 
request the top x prettiest number of houses and give parameters such as pricing or max distance from a specific location.



As part of the entire Django Application, the project also runs a python script on a regular, 1 hour basis every day of the week.

The python scripts webscrape the housing site zoopla to find all new propertylistings of the past hour and their core information.

For each newly scraped property, it then sends of each individual picture of it to a machine learning model that predicts the pictures
prettiness. Based off of the ratings of a propertie's pictures, an overall prettiness rating for the entire property is then
calculated by taking the average.

Each newly scraped and rated property is then POSTed to the database, keeping the database up to date with every single listing on zoopla.

Ultimately, the database contains and keeps itself up to date with thousands of property listings that are all rated on their prettiness.

The purpose of the this Django REST API is for a user, who is looking for a place to rent, to interact with this data,
using a website(that does not exist yet), in which the user can easily get a list of top properties filtered down by the 
following parameters:

      Number of bedrooms
      Minimum Price
      Maximum Price
      City
      Minimum amount of pictures
      Minimum amount of bedroom pictures
      Minimum amount of kitchen pictures
      Minimum amount of bathroom pictures
      Minimum amount of livingroom pictures
      Maximum amount of distance away from a given address
      
