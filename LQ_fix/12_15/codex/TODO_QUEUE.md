# TODO Queue (2025-12-15)

来源：`rg -n -tpy/ -tyaml "\b(TODO|FIXME|HACK)\b"`（排除 `docs/`）。

- Python: 38 条（见 `scan_logs/rg_todo_fixme_hack_py.txt`）
- YAML: 5 条（见 `scan_logs/rg_todo_fixme_hack_yaml.txt`）

## Python TODO/FIXME/HACK

### `src/model_factory/X_model/TSPN.py` (6)

- [ ] L9: #TODO: 2D signal processing, Logic_inference
- [ ] L72: # TODO logic
- [ ] L120: # TODO: data_id,task_id
- [ ] L148: # TODO op first then weight connection -> attention
- [ ] L204: # TODO # self.weight_connection.weight.data = F.softmax((1.0 / self.temperature) *
- [ ] L220: def __init__(self, in_channels, num_classes): # TODO logic

### `src/model_factory/ISFM/embedding/E_02_HSE_rec.py` (5)

- [ ] L1: ## TODO for reconstruction and prediction task
- [ ] L133: self.use_cond =  None # TODO for conditional generalization args.num_classes is not
- [ ] L145: # S3 TODO ROPE
- [ ] L148: if self.use_interpolation: # TODO
- [ ] L150: if self.use_cond: # TODO y_embedder should be a module dict

### `src/model_factory/X_model/Signal_processing.py` (4)

- [ ] L14: # from utils import convlutional_operator, signal_filter_, FRE # TODO
- [ ] L94: # TODO
- [ ] L158: # TODO add other filter
- [ ] L415: self.fre = FRE # TODO learbable

### `src/data_factory/data_factory.py` (3)

- [ ] L12: from .dataset_task.Dataset_cluster import IdIncludedDataset # ,Balanced_DataLoader_Dict_Iterator # TODO del balanced_data_loader
- [ ] L274: # TODO
- [ ] L387: TODO : 处理子集的情况

### `src/model_factory/ISFM/M_03_ISFM.py` (2)

- [ ] L47: # self.num_classes = self.get_num_classes()  # TODO prediction 任务不需要label？ @liq22
- [ ] L74: elif task_id in ['prediction']: # TODO individual prediction head

### `src/trainer_factory/Default_trainer.py` (2)

- [ ] L62: # 如果不存在log_every_n_steps，使用默认值50 # TODO @liq22
- [ ] L151: monitor=args.monitor, # TODO @liq22

### `src/Pipeline_03_multitask_pretrain_finetune.py` (1)

- [ ] L1: """ ## TODO

### `src/data_factory/dataset_task/ID_dataset.py` (1)

- [ ] L167: # TODO: Implement balanced ID sampling functionality

### `src/data_factory/reader/RM_025_KAIST.py` (1)

- [ ] L1: # TODO

### `src/data_factory/reader/RM_026_HUST23.py` (1)

- [ ] L1: # TODO

### `src/data_factory/samplers/FS_sampler.py` (1)

- [ ] L264: pass # TODO normal few-shot sampler for N-way K-shot tasks, not hierarchical

### `src/data_factory/samplers/del/ID_selector.py` (1)

- [ ] L1: # TODO using IDselector to extend other ID selector

### `src/model_factory/ISFM/M_01_ISFM.py` (1)

- [ ] L63: self.num_classes = self.get_num_classes()  # TODO prediction 任务不需要label？ @liq22

### `src/model_factory/ISFM/M_02_ISFM.py` (1)

- [ ] L61: self.num_classes = self.get_num_classes()  # TODO prediction 任务不需要label？ @liq22

### `src/model_factory/ISFM/backbone/B_02_basic_other.py` (1)

- [ ] L1: # TODO replace all the embedding

### `src/model_factory/ISFM/task_head/H_03_Linear_pred.py` (1)

- [ ] L6: class H_03_Linear_pred(nn.Module):  # TODO

### `src/task_factory/Components/contrastive_strategies.py` (1)

- [ ] L1149: # TODO: Implement adaptive strategy

### `src/task_factory/Components/loss.py` (1)

- [ ] L30: "SIGNAL_MASK_LOSS": Signal_mask_Loss,  # TODO Time Series Prediction

### `src/task_factory/task/GFS/matching.py` (1)

- [ ] L48: file_id = batch['file_id'][0].item()  # 确保 id 是字符串 TODO @liq22 sample 1 id rather than tensor

### `src/task_factory/task/pretrain/classification_prediction.py` (1)

- [ ] L46: file_id = batch['file_id'][0].item()  # 确保 id 是字符串 TODO @liq22 sample 1 id rather than tensor

### `src/task_factory/task/pretrain/prediction.py` (1)

- [ ] L46: file_id = batch['file_id'][0].item()  # 确保 id 是字符串 TODO @liq22 sample 1 id rather than tensor

### `src/utils/validation/OneEpochValidator.py` (1)

- [ ] L274: # TODO: Implement actual data loading using PHM-Vibench

## YAML TODO/FIXME/HACK

### `configs/v0.0.9/demo/X_Single_DG/MWA_CNN/HUST.yaml` (2)

- [ ] L23: batch_size: 64 # TODO: 和task.batch_size 保持一致
- [ ] L37: device: cuda # TODO: 和trainer.device 保持一致

### `configs/v0.0.9/demo/X_Single_DG/TSPN/HUST.yaml` (2)

- [ ] L22: batch_size: 64 # TODO: 和task.batch_size 保持一致
- [ ] L37: device: cuda # TODO: 和trainer.device 保持一致

### `configs/v0.0.9/demo/GFS/GFS_demo.yaml` (1)

- [ ] L124: early_stopping: True # TODO bug?

