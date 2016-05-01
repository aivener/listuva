
# Project 7
In this project, a map/reduce job was built using Apache Spark. 

It takes in data such as a website access log as input, and then it ouputs data that can be used by things such as a recommendation system.

In order to run this map/reduce job, you must utilze docker containers by running the command:

    docker-compose up

then press control z in your control and run the following command:

    docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/hello.py
    
This will take input from inside the data.txt file found inside the data file and execute the map/reduce job on that data set.

---
### Console Output

Currently, the job prints out 3 different data points onto the console (mostly to show why we get to our final results).

* Step 4: Transform into ((item 1, item2), list of user 1, list of user 2 etc) where users are all the ones who co-clicked (item1, item2).
  * Comment out lines 28-32 to remove these statements.

* Step 5: Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
 * Comment out lines 38-42 to remove these statements.

* Step 6: Filters out any results where less than 3 users co-clicked the same pair of items.
 * This is the final result of the Apache Spark Map/Reduce Job




