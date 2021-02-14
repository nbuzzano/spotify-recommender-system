# Spotify recommender system (WIP!!!)


#### Discussion:
In this repository you can find a set of recommender systems based on a Spotify dataset downloaded from [Spotify's Web API](https://developer.spotify.com/documentation/web-api/reference/). 

But there is more... since the goal is always building an awesome project, below you'll find my core ideas and how I want to build this project.

#### Data analysis stage:
+ The final goal is presenting the data analysis on [Tableu](https://www.tableau.com) or [Dash](https://plotly.com/dash/). But on a first stage Jupyter notebooks will be used.

#### Data engineering + MLOps stage:
+ [Airflow](https://airflow.apache.org): To author, schedule and monitor workflows.
+ [Kedro](https://github.com/quantumblacklabs/kedro): To create reproducible, maintainable and modular data science code.
+ AWS: To make the recommender systems available to the public (By deploying an API on EC2 or using AWS SageMaker. Not decided yet.).
+ Docker: To package this project into standardized units for development, shipment and deployment.

#### Data science stage:
+ After the data analysis stage, user based and content based recommender systems will be build. Below I'm letting a little of theory, but I will attach a much in deep documentation about my research about recommender systems on the future.

  + Content-based recommenders: suggest similar items based on a particular item. This system uses item metadata, such as genre, director, description, actors, etc. (in case of movies) to make these recommendations. The general idea behind these recommender systems is that if a person likes a particular item, he or she will also like an item that is similar to it. And to recommend that, it will make use of the user's past item metadata. A good example could be YouTube, where based on your history, it suggests you new videos that you could potentially watch.

  + Collaborative filtering engines: these systems are widely used, and they try to predict the rating or preference that a user would give an item-based on past ratings and preferences of other users. Collaborative filters do not require item metadata like its content-based counterparts

#### More:
+ PyCharm.
+ [Poetry](https://python-poetry.org): To handle python packaging and dependency management.
+ Follow [Hypermodern Python guide](https://cjolowicz.github.io/posts/) best practices.
