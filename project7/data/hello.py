from pyspark import SparkContext
import itertools

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# Read the file with data in
# ------------------------------------------------------------------------
data = sc.textFile("/tmp/data/data.txt", 2)       # each worker loads a piece of the data file

# Read data in as pairs of (user_id, item_id clicked on by the user)
# ------------------------------------------------------------------------
pairs = data.map(lambda line: line.split("\t")) # tell each worker to split each line of it's partition
p = pairs.map(lambda pair: (pair[0], pair[1]))

# Group data into (user_id, list of item ids they clicked on)
# ------------------------------------------------------------------------
ps = p.groupByKey()

# Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
# ------------------------------------------------------------------------
ps_items = ps.flatMapValues(lambda i: itertools.combinations(set(i), 2))

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
# ------------------------------------------------------------------------
ps_user = ps_items.map(lambda x: (x[1], x[0]))
ps_users = ps_user.groupByKey()

output = sorted(ps_user.collect())
for p, u in output:
	print("( " + str(p) + ": " + u + " )")

print ("Step 4: is done")

# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
# ------------------------------------------------------------------------
ps_count = ps_users.map(lambda x: (x[0], len(x[1])))

output = sorted(ps_count.collect())
for p, c in output:
	print("( " + str(p)+ ": " + str(c)+" )")

print ("Step 5: is done")

# Filter out any results where less than 3 users co-clicked the same pair of items
# ------------------------------------------------------------------------
count = ps_count.filter(lambda x: x[1] >= 3)

# Bring the data back to the master node so we can print it out
# ------------------------------------------------------------------------

output = sorted(count.collect())
for p, c in output:
	print("( " + str(p) + ": " + str(c) + " )")

print ("Step 6: is done")
print ("Popular items done")


sc.stop()
