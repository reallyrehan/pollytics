# Pollytics
## Elections 2020: Biden Vs Trump
### Sentiment Analysis - Can Social Media be an alternative for election polling?

As a part of a course in our Data Science Degree, we worked on analyzing sentiment around Biden and Trump for the year 2020 using around 60,000 Reddit posts. We analyzed and compared it with tweets of Biden (2k tweets) and Trump (10k tweets) and poll data (obtained from FiveThirtyEight).

We created a website visualizing all this data using Python's Dash framework which is fetching data from Firebase, deployed on Heroku. Also used Tableau for some visualizations to add some pretty cool visuals. Topic modeling has also been done using LDA (latent Dirichlet allocation) for creating a generative statistical model for each month that allows sets of observations to be explained by unobserved groups that explain why some parts of the data are similar. 

### Stack Used
- **Python** - Data Scraping, Collection, Cleaning, Processing
- **PySpark** -  Data Processing for Poll Data
- **Firebase** - for realtime Data Storage and access
- **Plotly Express** - for interactive Data Visualizing and Graphing
- **Tableau** -  Data Visualizing
- **Python Dash (with Flask)** - for creating a React Web App with bootstrap components
- **Heroku** - deploying [Web App](http://pollytics.herokuapp.com/)

The Heroku Web app is available on,
[http://pollytics.herokuapp.com/](http://pollytics.herokuapp.com/)

### Data Sources
- [**Twitter API**](https://developer.twitter.com/en/docs/twitter-api) - for scraping Donald Trump and Joe Biden Tweets
- [**Trump Archive**](https://www.thetrumparchive.com/faq) - Since Twitter limits tweets to 3k and Trump had over 10k tweets for 2020, we used Trump Archive to extract tweets that exceeded the limit
- [**PushShift Reddit API**](https://github.com/pushshift/api) - for scraping Reddit posts/tweets, aggregated stats for 2020
- [**FiveThirtyEight**](https://data.fivethirtyeight.com/) - for Polling Data

### Demo
[![Demo Video](https://img.youtube.com/vi/RyRQuFVxo8Q/0.jpg)](https://www.youtube.com/watch?v=RyRQuFVxo8Q)


## Sentiment Analysis
![Sentiment Analysis](img/1.png)

### Overall Stats
![Overall Stats](img/2.png)

### Topic Modeling
![Topic modeling](img/3.png)

### Some interesting sights
- We see a dip in sentiment around Trump and Biden, both, around April - the time when Covid started to make its impact in the US
- We plotted a moving average against poll results and we were surprised to see similar dips in the sentiment way before the dips can be seen in the polls a few weeks later, effectively predicting the polls.
- For every tweet Biden made, Trump tweeted 4 times
- Biden had more negative tweets than Trump

### Made By
- Rehan Ahmed
- Saurabh Jain
- Danielle Sim