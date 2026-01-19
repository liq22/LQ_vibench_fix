# TSPN_UXFD Integration Check

## Component Enable Switches

49:        self._uxfd_enable_sp2d = bool(_get_attr(args, "uxfd.enable_sp2d", False))
50:        self._uxfd_enable_fuzzy = bool(_get_attr(args, "uxfd.fuzzy.enable", False))
52:            _get_attr(args, "uxfd.operator_attention.enable", False)
54:        self._uxfd_enable_logic = bool(_get_attr(args, "uxfd.logic.enable", False))


## Component Imports

from __future__ import annotations
from dataclasses import asdict
from typing import Any, Dict, Optional
import torch
import torch.nn as nn
from .TSPN import Model as _TSPNModel
from .UXFD.fusion import FusionConfig, build_fusion
from .UXFD.fuzzy import FuzzyConfig, FuzzyReasoner
from .UXFD.neurosymbolic import LogicConfig, LogicReasoner
from .UXFD.operator_attention import OperatorAttention1D, OperatorAttentionConfig
from .UXFD.signal_processing_2d import STFTTimeFrequency
from .UXFD.signal_processing_2d.stft_tfr import STFTConfig


## Config Builder Functions

164:def _build_stft_cfg(args: Any) -> STFTConfig:
190:def _build_fusion_cfg(args: Any) -> FusionConfig:
207:def _build_fuzzy_cfg(args: Any) -> FuzzyConfig:
224:def _build_operator_attention_cfg(args: Any) -> OperatorAttentionConfig:
243:def _build_logic_cfg(args: Any) -> LogicConfig:
