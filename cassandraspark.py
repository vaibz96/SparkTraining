from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def parseInput(line):
    fields = line.split('|')
    return Row(user_id = int(fields[0]), age = int(fields[1]),
               gender = fields[2], occupation = fields[3], zip = fields[4])

if __name__ == "__main__":
    # Create a SparkSession
    spark = SparkSession. \
    builder.appName("CassandraExample"). \
    config("spark.cassandra.connection.host", "127.0.0.1"). \
    getOrCreate()

    # Build RDD on a raw text file
    lines = spark.sparkContext.textFile("hdfs:///user/maria_dev/mongodb/movies.user")

    # Convert it to a RDD of Row objects with (userID, age, gender, occupation, zip)
    users = lines.map(parseInput)

    # Convert RDD into a DataFrame
    usersDataset = spark.createDataFrame(users)

    # Write the data into Cassandra
    usersDataset.write\
        .format("org.apache.spark.sql.cassandra") \
        .mode('append') \
        .options(table="users", keyspace="moviesdata") \
        .save()