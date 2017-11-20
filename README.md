## Music Recommender
Bo Shen
Oct 2017

### Data
The dataset contains play and download logs of 0.6 million users over 3 months. The dataset has been partitioned into hundreds of compressed files and is hosted in AWS S3. 

### Data extraction
The first step of this project is to read and combine the logs into data tables in the database.  Because of the size of the dataset, this task is difficult to perform locally.  Eventually, AWS Athena service is used for the task.
A sample DDL code is shown as below:

```
CREATE EXTERNAL TABLE IF NOT EXISTS music_box.trial_search (
  `user_id` int,
  `os` string,
  `song_id` int,
  `song_type` int,
  `song_name` string,
  `singer` string,
  `play_time` float,
  `song_length` float,
  `paid_flag` boolean 
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '	',
  'field.delim' = '	',
  'collection.delim' = '',
  'mapkey.delim' = ''
) LOCATION 's3://aws-athena-query-results-607062241800-us-west-2/music_box/'
TBLPROPERTIES ('has_encrypted_data'='false')
```

### Data cleaning and exploration
After data aggregation in AWS Athena, the tables can be loaded into memory of local machine.
Data cleaning and exploration of play frequency and download log can be found in notebooks Down_log_cleaning and play_freq_EDA.
The critical part of this sections is to determine the utility of user based on the play log and download log.

### Building Recommenders
Graphlab has a very efficient algorithms to build recommenders on a local machine. However, because the utility matrix is very sparse, it is quite slow to obtain recommendations. So I had to build the recommender on a Spark cluster. The details are in the music_recommender_spark notebook.

### Web Application
To complete the end-to-end experience of a industry project, I created a web application that read recommendations from a database server and recommend music to the music app users using Flask.
