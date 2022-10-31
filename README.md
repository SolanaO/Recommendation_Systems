# Recommendations with IBM

The goal of this project is to build a recommender engine for IBM Watson.


## Introduction

We analyze the interactions that users have with articles on the IBM Watson Studio platform, and make recommendations to them about new articles. 

### I. Exploratory Data Analysis

Explore the data we are working with.

### II. Rank Based Recommendations

We  first find the most popular articles simply based on the most interactions. Since there are no ratings for any of the articles, it is easy to assume the articles with the most interactions are the most popular. These are then the articles we might recommend to new users (or anyone depending on what we know about them).

### III. User-User Based Collaborative Filtering

In order to build better recommendations for the users of IBM's platform, we could look at users that are similar in terms of the items they have interacted with. These items could then be recommended to the similar users. This would be a step in the right direction towards more personal recommendations for the users. You will implement this next.

### IV. Content Based Recommendations

Given the amount of content available for each article, there are a number of different ways in which someone might choose to implement a content based recommendations system. Using NLP we develop a content based recommendation system. 

### V. Matrix Factorization

Finally, we complete a machine learning approach to building recommendations. Using the user-item interactions, we build out a matrix decomposition.

