docker compose up -d

docker exec -it namenode bash

hdfs dfs -put data /
