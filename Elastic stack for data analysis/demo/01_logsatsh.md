# Logstash

Logstash is our swiss army knife for logs. With this powerful tool you can collect, parse, analyze, enrich your data and send it in your favourite container.

It works with configuration files, completely customizable for your needs.
To write the configurations, all the plugins are fully documented.

The Logstash event processing pipeline has three stages: inputs → filters → outputs. Inputs generate events, filters modify them, and outputs ship them elsewhere. Inputs and outputs support codecs that enable you to encode or decode the data as it enters or exits the pipeline without having to use a separate filter.

## [Input](https://www.elastic.co/guide/en/logstash/current/input-plugins.html)

An input plugin enables a specific source of events to be read by Logstash.

## [Filter](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html)

A filter plugin performs intermediary processing on an event. Filters are often applied conditionally depending on the characteristics of the event.

## [Output](https://www.elastic.co/guide/en/logstash/current/output-plugins.html)

An output plugin sends event data to a particular destination. Outputs are the final stage in the event pipeline.

## Logstash config for the demo

The Logstash configuration is quite easy:
Reads our csv file as *input*

    input {
      file {
        path => "lyrics-new.csv"
        start_position => "beginning"
        sincedb_path => "since.db"
      }
    }

as a *filter*, it splits the csv content, then replaces the **-** symbol from artists and songs, finally uses the song's release year as document time field

    filter {

      csv {
        columns => ["index", "song", "year", "artist", "genre", "lyrics"]
        separator => ";"
      }

      mutate {
        gsub => [
          "song", "-", " ",
          "artist", "-", " "
        ]
      }

      date {
        match => ["year", "yyyy"]
      }

    }

Then *outputs* everything to Elasticsearch. Note the commented rubydebug output, I left it in case you need it for debugging purposes.

    output {
      elasticsearch {
        index => "logstash-songlyrics"
      }
      # stdout {
      #   codec => rubydebug
      # }
    }

