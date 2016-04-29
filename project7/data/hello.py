from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/data.txt", 2)       # each worker loads a piece of the data file

#data file format: name(user_id) \t item_id

# Read data in as pairs of (user_id, item_id clicked on by the user)
# Group data into (user_id, list of item ids they clicked on)
# Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
# Filter out any results where less than 3 users co-clicked the same pair of items

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[0], [pair[1]]))     # group data into (user_id, list of item ids they clicked on)
count = pages.groupByKey()        # creates list of all pages clicked for each key(name)

output = count.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output: #count is Iterable object of pages clicked by user
	# for item in count:
		print ("page_id %s count %s" % (page_id, count))
print ("Popular items done")

sc.stop()