import hydra
import mlflow

@hydra.main(config_path="conf",config_name="config_test.yaml")

def my_app(cfg):
    print(cfg.model.node1) # 128
    print(cfg.optimizer.lr) # 0.001

if __name__ == "__main__":
    my_app()

# c = []
# hydra.main(config_path="conf",config_name="config.yaml")(lambda x:c.append(x))()
# cfg = c[0]
# print('sync')
# print("checks")