# Demo

## Index status and settings

After having uploaded all our data, let's open Kibana and navigate to Dev Tools, on the left side.
Here we can query Elasticsearch on the left side and see the response on the right side.

Get the list of our indices:

    GET _cat/indices?v

    health  status index               uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    yellow  open   logstash-songlyrics tBT7Nn4WRUedIwEws1VM-Q   5   1     362238            0    510.6mb        510.6mb
    green   open   .kibana             vLHJYEiSTVaq7q-Mo6CxhA   1   0         10            2     33.9kb         33.9kb

As you can see, our index has *yellow* state. It means there are some *replica* shards which are not initialized. This is correct since it won't place *replica* shards on the same node where the *primary* shards are.
The cluster state is reflecting the worst index state (a yellow index leads all the cluster to be yellow)

    GET _cat/health?v

    epoch      timestamp cluster      status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
    1534945715 15:48:35  download2018 yellow          1         1      6   6    0    0        5             0                  -                 54.5%

We can change the number of replicas to 0 modifying the *settings* of the index:

    PUT logstash-songlyrics/_settings
    {
      "index": {
        "number_of_replicas": 0
      }
    }

    {
      "acknowledged": true
    }

Now the index and cluster state are *green*

    GET _cat/indices?v

    health status index               uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    green  open   logstash-songlyrics tBT7Nn4WRUedIwEws1VM-Q   5   0     362238            0    510.6mb        510.6mb
    green  open   .kibana             vLHJYEiSTVaq7q-Mo6CxhA   1   0         10            2     33.9kb         33.9kb

    GET _cat/health?v
    epoch      timestamp cluster      status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
    1534945974 15:52:54  download2018 green           1         1      6   6    0    0        0             0                  -                100.0%

## Let's search!

### Information on search

 - Elasticsearch provides a full [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html) (Domain Specific Language) based on JSON to define queries
 - The [term](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html) query finds documents that contain the exact term specified in the inverted index
 - [match](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html) queries accept text/numerics/dates, analyzes them, and constructs a query
 - A [Bool](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html) query matches documents matching boolean combinations of other queries.
   It is built using one or more boolean clauses, each clause with a typed occurrence: must, filter, should, must_not
 - Do you know the difference between a [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) and a [text](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) data type? (*keyword* isn't analyzed while *text* is)

### First queries

I want to search for all the songs containing the word **love**:

    GET logstash-songlyrics/_search
    {
      "query": {
        "term": {
          "lyrics": {
            "value": "love"
          }
        }
      }
    }

The response is composed by some information on our search and the matched documents.
In *hits* we can see the total of matched documents and the list of all of them.

    {
      "took": 12,
      "timed_out": false,
      "_shards": {
        "total": 5,
        "successful": 5,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": 86706,
        "max_score": 2.4433963,
        "hits": [
          ... list of all documents matching our query ...
        ]
      }
    }

So 86706 documents, but we are see only 10 in the list, to see more:

    GET logstash-songlyrics/_search
    {
      "size": 100,
      "query": {
        "term": {
          "lyrics": {
            "value": "love"
          }
        }
      }
    }

There is a limit on the number of documents you can return, default is [10000](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-from-size.html), you can change this behavior or use the [scroll](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-scroll.html) API.

Can you tell why this isn't returning any document?

    GET logstash-songlyrics/_search
    {
      "query": {
        "term": {
          "lyrics.keyword": {
            "value": "love"
          }
        }
      }
    }

(term query is searching on the reverted index, a keyword field isn't analysed so it doesn't have any reversed index)

How to search only for **love** songs prior to 2000?

    GET logstash-songlyrics/_search
    {
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "lyrics": {
                  "value": "love"
                }
              }
            },
            {
              "range": {
                "@timestamp": {
                  "lt": "2000",
                  "format": "yyyy",
                  "time_zone": "+01:00"
                }
              }
            }
          ]
        }
      }
    }

## Aggregations

What if I want the number of songs per year, from 1990 to 2000?

    GET logstash-songlyrics/_search
    {
      "size": 0,
      "aggs": {
        "year": {
          "date_histogram": {
            "field": "@timestamp",
            "interval": "year"
          }
        }
      },
      "query": {
        "range": {
          "@timestamp": {
            "gt": 1990,
            "lt": 2000,
            "format": "yyyy",
            "time_zone": "+01:00"
          }
        }
      }
    }

(size 0 to not return any document, only the aggregation result)

Let's search for the top 30 lyrics words:

    GET logstash-songlyrics/_search
    {
      "size": 0,
      "aggs": {
        "lyrics": {
          "terms": {
            "field": "lyrics",
            "size": 30
          }
        }
      }
    }

We get an error

    {
      "error": {
        "root_cause": [
          {
            "type": "illegal_argument_exception",
            "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [lyrics] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
          }
        ],
        "type": "search_phase_execution_exception",
        "reason": "all shards failed",
        "phase": "query",
        "grouped": true,
        "failed_shards": [
          {
            "shard": 0,
            "index": "logstash-songlyrics",
            "node": "SBheg9xxT3-N8EjFiXM2hA",
            "reason": {
              "type": "illegal_argument_exception",
              "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [lyrics] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
            }
          }
        ],
        "caused_by": {
          "type": "illegal_argument_exception",
          "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [lyrics] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead.",
          "caused_by": {
            "type": "illegal_argument_exception",
            "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [lyrics] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
          }
        }
      },
      "status": 400
    }

This is because text fields by default have fielddata disabled.

Here some info on [fielddata](https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html) and [doc_values](https://www.elastic.co/guide/en/elasticsearch/reference/current/doc-values.html).

Can we use the not *analyzed* field?

    GET logstash-songlyrics/_search
    {
      "size": 0,
      "aggs": {
        "lyrics": {
          "terms": {
            "field": "lyrics.keyword",
            "size": 30
          }
        }
      }
    }

The result seems a little odd, we don't see single words but sentences and complete lyrics.
This is because the not analyzed field isn't *tokenized* (an analysis phase).
This makes sense for some use cases, where I don't want the words to be split, such as the top artists:

    GET logstash-songlyrics/_search
    {
      "size": 0,
      "aggs": {
        "lyrics": {
          "terms": {
            "field": "artist.keyword",
            "size": 30
          }
        }
      }
    }

## Mappings

To know where fielddata is enabled we shall look at the index mapping

    GET logstash-songlyrics/_mapping

This is the current "schema" of our index.
The result is organized as follows

    {
      "logstash-songlyrics": {
        "mappings": {
          "_default_": {...},
          "doc": {
            "dynamic_templates": [
              ...
            ],
            "properties": {
            ... list of fields present in our index ...
            }
          }
        }
      }
    }

First, the *_default_* and *doc* types are deprecated. Since Elasticsearch 6.0 an index can have only one type, forget these right now.

Second, the *dynamic_templates* are added by the Logstash template, we will cover this later.

Last but not the least, in properties we can see a list of all the fields in our index, with types and attributes.

Here we can search for our lyrics field:

    "lyrics": {
      "type": "text",
      "norms": false,
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    }

As we can see fielddata is disabled, let's enable it

    PUT logstash-songlyrics/_mapping/doc
    {
      "properties": {
        "lyrics": {
          "type": "text",
          "fielddata": true,
          "norms": false,
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    }

Now we can aggregate on lyrics to see which are the most common words in our songs and get the expected response.

### Templates

As seen, some of the fields of our index's mapping are added by Logstash, but how? Templates is the response.

To see the list of templates:

    GET _cat/templates?v

    name                          index_patterns             order      version
    .ml-anomalies-                [.ml-anomalies-*]          0          6030199
    logstash                      [logstash-*]               0          60001
    .triggered_watches            [.triggered_watches*]      2147483647
    .monitoring-beats             [.monitoring-beats-6-*]    0          6020099
    security-index-template       [.security-*]              1000
    kibana_index_template:.kibana [.kibana]                  0
    .monitoring-es                [.monitoring-es-6-*]       0          6020099
    .ml-meta                      [.ml-meta]                 0          6030199
    .watch-history-7              [.watcher-history-7*]      2147483647
    .watches                      [.watches*]                2147483647
    .monitoring-alerts            [.monitoring-alerts-6]     0          6020099
    security_audit_log            [.security_audit_log*]     1000
    .ml-notifications             [.ml-notifications]        0          6030199
    .ml-state                     [.ml-state]                0          6030199
    .monitoring-logstash          [.monitoring-logstash-6-*] 0          6020099
    .monitoring-kibana            [.monitoring-kibana-6-*]   0          6020099
    logstash-index-template       [.logstash]                0

So we do have a *logstash* template, let's see it

    GET _template/logstash

How is a template composed?
First part is telling us the template's name, *logstash*, the order and the version.
The templates are applied in order (0, 1, 2, 1000, ...), when I update it I can update the version.

    {
      "logstash": {
        "order": 0,
        "version": 60001,

Then we have the *index_patterns*, all indices which does respect this pattern in their name will get affected by this template.

    "index_patterns": [
      "logstash-*"
    ],

Following we have the index level settings. Some of these can be hot changed, such as the number of replicas.

    "settings": {
      "index": {
        "refresh_interval": "5s"
      }
    },

After that there's the *mappings*, currently still organized by *type* ([*\_default\_*](https://www.elastic.co/guide/en/elasticsearch/reference/current/default-mapping.html) in this case) but this is a deprecated information and will be removed.
This is then divided in:

1) *[dynamic templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-templates.html)*: custom mappings that can be applied to dynamically added fields based on *datatype*, name of field and full dotted path to the field
   - *message_fields*: out message field shall be of type text, matched by datatype and name
   - *string_fields*: all string fields are of type text and shall have an additional *.keyword* field of type keyword. Here where it comes from!
2) *properties*: list of fields with datatypes and [parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-params.html)

*message* field contains the original, not parsed, message detected by Logstash.
This will tell to out index of its fields should behave.

    "mappings": {
      "_default_": {
        "dynamic_templates": [
          {
            "message_field": {
              "path_match": "message",
              "match_mapping_type": "string",
              "mapping": {
                "type": "text",
                "norms": false
              }
            }
          },
          {
            "string_fields": {
              "match": "*",
              "match_mapping_type": "string",
              "mapping": {
                "type": "text",
                "norms": false,
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          }
        ],
        "properties": {
          "@timestamp": {
            "type": "date"
          },
          "@version": {
            "type": "keyword"
          },
          "geoip": {
            "dynamic": true,
            "properties": {
              "ip": {
                "type": "ip"
              },
              "location": {
                "type": "geo_point"
              },
              "latitude": {
                "type": "half_float"
              },
              "longitude": {
                "type": "half_float"
              }
            }
          }
        }
      }
    },

Last, here's the list of aliases added to indices. Having an alias I can do query directly on that, without knowledge of which index it insists on.

    "aliases": {}
      }
    }

I can create as much templates as I need.

When I create an index, all the templates that match the index's name will be applied in order. The configuration of my index will be the sum of all the applied templates. All the fields of the documents that will be indexed in this index shall respect its configuration.

To create a template, the base is

    PUT _template/<template name>
    {
      "index_patterns": [...],
      "settings": {...},
      "mappings": {
        "doc": {
          "properties": {...}
        }
      }
    }

### Analyzer && reindex && aliases

In our top words in lyrics query we see that the most used words by songwriters are prepositions, postpositions and articles: the, to, and, a, i, you, in, me, of, my, it, that, on, all, your, is, for, be, so, but, ...

This makes little sense in our analysis, how to get rid of them? We can use [analyzers](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html)

 - *"Analysis is the process of converting text into tokens or terms which are added to the inverted index for searching"*

The analyzer can be specified at different levels, to have a consistent result you should use the same analyzer at index and at query time.

We have an API to test analyzers: `_analyze`.
Can you tell what is the difference between the whitespace analyzer and the standard analyzer?

    POST _analyze
    {
      "analyzer": "whitespace",
      "text": "Finished with my woman 'cause she couldn't help me with my mind"
    }

    POST _analyze
    {
      "analyzer": "default",
      "text": "Finished with my woman 'cause she couldn't help me with my mind"
    }

(*default* analyzer does lowercasing and removes punctuation, whitespace does not)

Our index has used the default analyzer while indexing since we didn't specified any.
Since we already indexed our data, we cannot change the index analyzer now, but we can reindex our data with a different analyzer.

Let's create an index with a different analyzer

    PUT logstash-songlyrics-new
    {
      "settings": {
        "index": {
          "number_of_replicas": 0
        },
        "analysis": {
          "analyzer": {
            "std_english": {
              "type": "standard",
              "stopwords": "_english_"
            }
          }
        }
      },
      "mappings": {
        "doc": {
          "properties": {
            "lyrics": {
              "analyzer":"std_english",
              "type": "text",
              "fielddata": true,
              "norms": false,
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        }
      }
    }

This analyzer, named *std_english*, takes into account a [*stopwords*](https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer-anatomy.html#_token_filters) token filter.
The english analyzer stops the current [list](https://github.com/apache/lucene-solr/blob/53981795fd73e85aae1892c3c72344af7c57083a/lucene/core/src/java/org/apache/lucene/analysis/standard/StandardAnalyzer.java#L44-L50) of words:

    "a", "an", "and", "are", "as", "at", "be", "but", "by",
    "for", "if", "in", "into", "is", "it",
    "no", "not", "of", "on", "or", "such",
    "that", "the", "their", "then", "there", "these",
    "they", "this", "to", "was", "will", "with"

We specified the analyzer for our field, if you don't want to specify it, you can add it to an index template as a dynamic template ;)

First, let's test it:

    POST logstash-songlyrics-new/_analyze
    {
      "analyzer": "std_english",
      "text": "Finished with my woman 'cause she couldn't help me with my mind"
    }

This works as expected! Now let's [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) our data in the new index

    POST _reindex
    {
      "source": {
        "index": "logstash-songlyrics"
      },
      "dest": {
        "index": "logstash-songlyrics-newnew"
      }
    }

This operation can take some time, you can monitor it by looking at the indices list and the number of documents.

Now query the data set to see the top words

    GET logstash-songlyrics-new/_search
    {
      "size": 0,
      "aggs": {
        "lyrics": {
          "terms": {
            "field": "lyrics",
            "size": 30
          }
        }
      }
    }

So we confirmed it works! If the *\_english\_* analyzer isn't enough you can always specify your own list of stopwords

It can be helpful to specify an alias, so you don't have to change the index for your queries.

To add an alias to an index

    POST /_aliases
    {
      "actions": [
        {
          "add": {
            "index": "logstash-songlyrics",
            "alias": "mysongs"
          }
        }
      ]
    }

To see the list of aliases

    GET _alias

To remove an alias from an index

    POST /_aliases
    {
      "actions": [
        {
          "remove": {
            "index": "logstash-songlyrics",
            "alias": "mysongs"
          }
        }
      ]
    }

In this way you always query *mysongs* index without caring of which index is insisting on.
This is particularly useful for Kibana and custom applications.

### More queries

Top words in Rock or Pop after 2000, for genre

    GET mysongs/_search
    {
      "size": 0,
      "aggs": {
        "genre": {
          "terms": {
            "field": "genre.keyword",
            "size": 10
          },
          "aggs": {
            "words": {
              "terms": {
                "field": "lyrics",
                "size": 10
              }
            }
          }
        }
      },
      "query": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "gte": "2000",
                  "format": "yyyy",
                  "time_zone": "+01:00"
                }
              }
            },
            {
              "bool": {
                "should": [
                  {
                    "term": {
                      "genre": {
                        "value": "rock"
                      }
                    }
                  },
                  {
                    "term": {
                      "genre": {
                        "value": "pop"
                      }
                    }
                  }
                ],
                "minimum_should_match": 1
              }
            }
          ]
        }
      }
    }

Top 5 words for top 5 artist, for top 5 genres, before 2000, excluding Pop genre and *love* word in lyrics

    GET mysongs/_search
    {
      "size": 0,
      "aggs": {
        "top 5 genres": {
          "terms": {
            "field": "genre.keyword",
            "size": 5
          },
          "aggs": {
            "top 5 artists": {
              "terms": {
                "field": "artist.keyword",
                "size": 5
              },
              "aggs": {
                "top 5 words": {
                  "terms": {
                    "field": "lyrics",
                    "size": 5
                  }
                }
              }
            }
          }
        }
      },
      "query": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "gte": 2000,
                  "format": "yyyy",
                  "time_zone": "+01:00"
                }
              }
            }
          ],
          "must_not": [
            {
              "term": {
                "lyrics": {
                  "value": "love"
                }
              }
            }
          ]
        }
      }
    }

number of songs per top 10 artists per decade, from 1970, which aren't pop singers, doesn't mention love in the songs and doesn't have "the" in their name

    GET mysongs/_search
    {
      "size": 0,
      "aggs": {
        "decade": {
          "date_histogram": {
            "field": "@timestamp",
            "interval": "3650d"
          },
          "aggs": {
            "top 5 artists": {
              "terms": {
                "field": "artist.keyword",
                "size": 10
              }
            }
          }
        }
      },
      "query": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "gte": 1970,
                  "format": "yyyy",
                  "time_zone": "+01:00"
                }
              }
            }
          ],
          "must_not": [
            {
              "bool": {
                "should": [
                  {
                    "term": {
                      "genre": {
                        "value": "pop"
                      }
                    }
                  },
                  {
                    "term": {
                      "lyrics": {
                        "value": "love"
                      }
                    }
                  },
                  {
                    "term": {
                      "artist": {
                        "value": "the"
                      }
                    }
                  }
                ],
                "minimum_should_match": 3
              }
            }
          ]
        }
      }
    }