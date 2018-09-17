# Kibana

You use [Kibana](https://www.elastic.co/guide/en/kibana/current/index.html) to search, view, and interact with data stored in Elasticsearch indices. You can easily perform advanced data analysis and visualize your data in a variety of charts, tables, and maps.

Here we will use Kibana to explore and visualize our lyrics data set

## [Index patterns](https://www.elastic.co/guide/en/kibana/current/tutorial-define-index.html)

Index patterns tell Kibana which Elasticsearch indices you want to explore. An index pattern can match the name of a single index, or include a wildcard (*) to match multiple indices.

We can both define an index pattern for an index or an alias

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2001.PNG)

## [Discover](https://www.elastic.co/guide/en/kibana/current/discover.html)

You can interactively explore your data from the Discover page. You have access to every document in every index that matches the selected index pattern. You can submit search queries, filter the search results, and view document data. You can also see the number of documents that match the search query and get field value statistics.

The use of the search bar at the top will be explained later.

We can create a search on our index by adding the columns we like from the bar on the left side or from inside a document with the magnifier:

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2002.PNG)

## [Visualize](https://www.elastic.co/guide/en/kibana/current/visualize.html)

Visualize enables you to create visualizations of the data in your Elasticsearch indices. You can then build dashboards that display related visualizations.
Kibana visualizations are based on Elasticsearch queries. By using a series of Elasticsearch aggregations to extract and process your data, you can create charts that show you the trends, spikes, and dips you need to know about.
You can create visualizations from a search saved from Discover or start with a new search query.

How to create a simple top artists visualization?
Select the chart type you like the most (following a pie), slit by *terms* aggregation, select the *artists.keyword* field and then press the play button to se the result!

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2003.PNG)

The size parameter let's you decide how many buckets (you need top 10? top 20?) ot show, the more buckets you want, the more computation time will take to load your visualization.

You can create as much visualizations as you want. Play with the different visualization to make some practice.

A suggestion: save the visualization with a talking name, I typically use the saved search name and a description of what it shows.
This is because when you will have many visualizations, if the name does not tell you much about what it shows, it could be difficult to find the one you are searching for.

How to do a visualization with more than one aggregation? While creating a visualization click on  "add sub-buckets" button

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2004.PNG)

All visualization differs on the kind of aggregations they offer and how many of them you can use.

## Dashboard

A Kibana dashboard displays a collection of visualizations and searches. You can arrange, resize, and edit the dashboard content and then save the dashboard so you can share it.

Now that you have created some visualizations, you can add them to a dashboard. Go to the dashboard tab on the left,  click on the "create new dashboard" button and start putting yur visualizations in it.
Resize and position them until you are happy with your result.

A suggestion: adding also the search can be useful to see what documents are displayed in the current visualizations.

How to add the visualizations...

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2005.PNG)

And the final dashboard...

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2006.PNG)

## Search

Every visualization is responsive, when you click on a pie, on a bar or else, you will filter all teh dashboard by the value of the component you clicked on.+
Successive filters will be added to this, the resulting dashboard is the sum of all the filters.

To get insights on the queries used for the visualizations, click on the arrow button under a visualization: here you can see not only the Elasticsearch query but also the response and the performance of the query. You can detect slower visualizations and tune or get your dashboard rid of them.

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2007.PNG)

You can also see, and modify, the DSL query used in filters. Here you can put also very complex queries.

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2008.PNG)

To search more accurately without having to write Elasticsearch queries, you can use the search bar at the top of the dashboard. This bar uses the [Lucene query syntax](https://www.elastic.co/guide/en/kibana/current/lucene-query.html).

For example you can search *love*, in any document, in any field, by typing the word in the bar and then pressing the search button. That simple.

How to search for *black sabbath* artist? If you try to type the name you will see all documents containing the words *black* and *sabbath*, no matter where.

To search for that artist you should type this:

    artist:"black sabbath"

![alt text](https://raw.githubusercontent.com/MisoMadao/download2018/master/Elastic%20stack%20for%20data%20analysis/imgs/elastic%2009.jpg)

It supports also AND and OR boolean operators

    artist:"black sabbath" AND year:1970

And also exclude some words by placing a !

    artist:"black sabbath" AND year:1970 AND !pigs

Notice the last operator is excluding all documents containing the pigs word, no matter where.

These are only some of the many possibilities, explore the language to query different data types.

## [Console](https://www.elastic.co/guide/en/kibana/current/console-kibana.html)

The Console plugin provides a UI to interact with the REST API of Elasticsearch.

We already used it in the Elasticsearch demo

## Plugins

Kibana is a pluggable framework. Out there exists many plugins to enhance your experience and empower this tool.

Take a look at the [known plugin](https://www.elastic.co/guide/en/kibana/current/known-plugins.html) page.
