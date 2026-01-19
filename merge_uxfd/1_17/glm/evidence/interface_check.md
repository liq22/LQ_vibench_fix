# Interface Consistency Check

## Config Classes

### SP2D
- Module: `UXFD.signal_processing_2d.stft_tfr.STFTConfig`
- Signature: `(cfg: 'Optional[STFTConfig]' = None)`

### Fusion
- Module: `UXFD.fusion.simple_fusion.FusionConfig`
- Signature: `(dim: 'int', cfg: 'Optional[FusionConfig]' = None) -> 'nn.Module'`

### Fuzzy
- Module: `UXFD.fuzzy.fuzzy_reasoner.FuzzyConfig`
- Signature: `(dim_in: 'int', num_classes: 'int', cfg: 'Optional[FuzzyConfig]' = None)`

### OperatorAttention
- Module: `UXFD.operator_attention.operator_attention_1d.OperatorAttentionConfig`
- Signature: `(in_channels: 'int', cfg: 'Optional[OperatorAttentionConfig]' = None)`

### Neurosymbolic
- Module: `UXFD.neurosymbolic.logic_reasoner.LogicConfig`
- Signature: `(dim_in: 'int', num_classes: 'int', cfg: 'Optional[LogicConfig]' = None) -> 'None'`


## __all__ Exports

### fusion
- __all__ = ['FusionConfig', 'build_fusion']

### fuzzy
- __all__ = ['FuzzyConfig', 'FuzzyReasoner']

### operator_attention
- __all__ = ['OperatorAttention1D', 'OperatorAttentionConfig']

### neurosymbolic
- __all__ = ['LogicConfig', 'LogicReasoner']

### signal_processing_2d
- __all__ = ['STFTTimeFrequency']

