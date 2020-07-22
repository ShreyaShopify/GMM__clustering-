from pyspark.ml.clustering import PowerIterationClustering

df = spark.createDataFrame([
    (0, 1, 1.0),
    (0, 2, 1.0),
    (1, 2, 1.0),
    (3, 4, 1.0),
    (4, 0, 0.1)
], ["src", "dst", "weight"])

pic = PowerIterationClustering(k=2, maxIter=20, initMode="degree", weightCol="weight")

# Shows the cluster assignment
pic.assignClusters(df).show()e
