import mlflow

# start new run
with mlflow.start_run():
  
  # log single key-value param
  mlflow.log_param("param1", 5)
  
  # log single key-value metric
  mlflow.log_metric("foo", 2, step=1)
  mlflow.log_metric("foo", 4, step=2)
  mlflow.log_metric("foo", 6, step=3)
  
  with open("output.txt", "w") as f:
    f.write("Hello world!")
    
  # logs local file or directory as artifact,
  mlflow.log_artifact("output.txt")