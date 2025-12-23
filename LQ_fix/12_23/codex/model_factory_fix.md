
# Role
你是 PHM-Vibench 项目的核心维护者。请在 `lqfix_25-12` 分支上，对 `src/model_factory/ISFM` 模块进行“无破坏性”的架构升级：引入 Registry 机制。

# Hard Constraints (绝对约束)
1.  **禁止修改 M_01_ISFM.py**：文件 `src/model_factory/ISFM/M_01_ISFM.py` 必须保持字节级不变（用于兜底）。
2.  **变量名严格对齐**：新代码中的参数名必须与 `M_01_ISFM.py` 中的 `args_m` 保持一致。
3.  **单向依赖**：Registry 不应静态导入组件，而是通过 `bootstrap()` 懒加载组件目录来触发注册，避免循环依赖。
4.  **冒烟验证**：改动完成后，必须能同时跑通旧模型（M_01）和新模型（M_04）的冒烟测试。

# Context (代码现状)
* **入口**：`src/model_factory/model_factory.py` 根据 `type` 和 `name` 动态实例化模型。
* **现有模型**：`M_01_ISFM.py` 内部定义了 `Embedding_dict`, `Backbone_dict`, `TaskHead_dict` 来硬编码组件。
* **组件位置**：`src/model_factory/ISFM/backbone/`, `task_head/`, `embedding/`。

# Execution Plan (执行步骤)

## Step 1: 创建注册中心
新建文件 `src/model_factory/ISFM/registry.py`。
* 实现 `Registry` 类和 `GLOBAL_REGISTRY` 单例。
* 提供 `register_backbone`, `register_head`, `register_embedding` 装饰器/函数。
* 提供 `bootstrap()` 方法，在第一次调用时动态 import 子包 (`.backbone`, `.task_head`, `.embedding`)。

## Step 2: 实施“无侵入”注册
修改以下三个文件的 `__init__.py`，在文件末尾**追加**注册逻辑（保留原有 export 不变）：
* `src/model_factory/ISFM/backbone/__init__.py`
* `src/model_factory/ISFM/task_head/__init__.py`
* `src/model_factory/ISFM/embedding/__init__.py`
* **操作**：引入 `GLOBAL_REGISTRY`，并将该目录下 `__all__` 或已导入的类注册进去。

## Step 3: 派生新模型 M_04
1.  复制：`cp src/model_factory/ISFM/M_01_ISFM.py src/model_factory/ISFM/M_04_ISFM_Registry.py`
2.  重构 `M_04_ISFM_Registry.py`：
    * 保留所有 import（为了兼容性）。
    * **删除** `Embedding_dict`, `Backbone_dict`, `TaskHead_dict` 定义。
    * 修改 `__init__` 方法：
        * 调用 `GLOBAL_REGISTRY.bootstrap()`。
        * 使用 `GLOBAL_REGISTRY.get_backbone(args_m.backbone)` 替代字典查找。
        * (注意参数名是 `args_m`)。
3.  暴露新模型：在 `src/model_factory/ISFM/__init__.py` 中导出 `M_04_ISFM_Registry`。

## Step 4: 冒烟测试配置
1.  新建 `configs/demo/00_smoke/dummy_registry_test.yaml`。
2.  内容完全复制自 `configs/demo/00_smoke/dummy_dg.yaml`。
3.  仅修改一行：将 `model.name` 从 `M_01_ISFM` 改为 `M_04_ISFM_Registry`。

# Deliverables (代码产物)
请生成以下 4 个代码块，我将直接写入文件。

## 1. `src/model_factory/ISFM/registry.py`
```python
from typing import Any, Callable, Dict, Optional, Type
import importlib

class RegistryKeyError(KeyError):
    pass

class Registry:
    def __init__(self):
        self._backbones: Dict[str, Type] = {}
        self._heads: Dict[str, Type] = {}
        self._embeddings: Dict[str, Type] = {}
        self._bootstrapped = False

    def bootstrap(self):
        """Lazy import to trigger registration decorators."""
        if self._bootstrapped:
            return
        # 这些 import 会触发各个子模块 __init__.py 里的注册代码
        from . import backbone, task_head, embedding
        self._bootstrapped = True

    def register_backbone(self, name: str, cls: Type, override: bool = False):
        self._register(self._backbones, name, cls, override, "backbone")

    def register_head(self, name: str, cls: Type, override: bool = False):
        self._register(self._heads, name, cls, override, "task_head")

    def register_embedding(self, name: str, cls: Type, override: bool = False):
        self._register(self._embeddings, name, cls, override, "embedding")

    def get_backbone(self, name: str) -> Type:
        return self._get(self._backbones, name, "backbone")

    def get_head(self, name: str) -> Type:
        return self._get(self._heads, name, "task_head")

    def get_embedding(self, name: str) -> Type:
        return self._get(self._embeddings, name, "embedding")

    def list_backbones(self): return list(self._backbones.keys())
    def list_heads(self): return list(self._heads.keys())
    def list_embeddings(self): return list(self._embeddings.keys())

    def _register(self, store, name, cls, override, kind):
        if name in store and not override:
            raise ValueError(f"{kind} '{name}' already registered.")
        store[name] = cls

    def _get(self, store, name, kind):
        if name not in store:
            options = ", ".join(sorted(store.keys())[:10])
            raise RegistryKeyError(f"Unknown {kind}: '{name}'. Available: {options}...")
        return store[name]

GLOBAL_REGISTRY = Registry()

```

## 2. `src/model_factory/ISFM/backbone/__init__.py` (Append Snippet)

*请在文件末尾追加以下代码（不要删除原有内容）：*

```python
# ... (保留原有 imports)

# --- Registry Auto-Registration ---
from ..registry import GLOBAL_REGISTRY

# 将当前模块导出的所有 Backbone 类注册到全局注册表
# 假设上方已经 import 了 B_04_Dlinear 等类
try:
    GLOBAL_REGISTRY.register_backbone('B_01_basic_transformer', B_01_basic_transformer)
    GLOBAL_REGISTRY.register_backbone('B_03_FITS', B_03_FITS)
    GLOBAL_REGISTRY.register_backbone('B_04_Dlinear', B_04_Dlinear)
    GLOBAL_REGISTRY.register_backbone('B_05_Mamba', B_05_Mamba)
    GLOBAL_REGISTRY.register_backbone('B_06_TimesNet', B_06_TimesNet)
    GLOBAL_REGISTRY.register_backbone('B_07_TSMixer', B_07_TSMixer)
    GLOBAL_REGISTRY.register_backbone('B_08_PatchTST', B_08_PatchTST)
    GLOBAL_REGISTRY.register_backbone('B_09_FNO', B_09_FNO)
    GLOBAL_REGISTRY.register_backbone('B_10_VIBT', B_10_VIBT)
    GLOBAL_REGISTRY.register_backbone('B_11_MomentumEncoder', B_11_MomentumEncoder)
except NameError:
    pass # 防止部分依赖缺失导致导入失败

```

## 3. `src/model_factory/ISFM/M_04_ISFM_Registry.py` (Core Logic)

*这是基于 M_01 修改后的核心代码片段，请确保替换掉原有的 Dict 定义和 **init** 逻辑：*

```python
# ... (Imports same as M_01)
from src.model_factory.ISFM.registry import GLOBAL_REGISTRY

# (Delete Embedding_dict, Backbone_dict, TaskHead_dict definitions)

class Model(nn.Module):
    """
    M_04_ISFM_Registry: Registry-based ISFM implementation.
    Parameters match M_01 exactly: args_m, metadata
    """
    def __init__(self, args_m, metadata):
        super(Model, self).__init__()
        self.metadata = metadata
        self.args_m = args_m
        
        # 1. 懒加载触发注册
        GLOBAL_REGISTRY.bootstrap()

        # 2. 从 Registry 获取类 (替代原来的 Dict[key])
        EmbeddingCls = GLOBAL_REGISTRY.get_embedding(args_m.embedding)
        BackboneCls = GLOBAL_REGISTRY.get_backbone(args_m.backbone)
        TaskHeadCls = GLOBAL_REGISTRY.get_head(args_m.task_head)

        # 3. 实例化 (保持与 M_01 完全一致的参数传递)
        self.embedding = EmbeddingCls(args_m)
        self.backbone = BackboneCls(args_m)
        
        self.num_classes = self.get_num_classes()
        args_m.num_classes = self.num_classes
        
        self.task_head = TaskHeadCls(args_m)

    # ... (get_num_classes, _embed, _encode, _head, forward 等方法保持原样)

```

## 4. `configs/demo/00_smoke/dummy_registry_test.yaml` (Generation Command)

*直接运行以下 Shell 命令生成测试配置：*

```bash
cp configs/demo/00_smoke/dummy_dg.yaml configs/demo/00_smoke/dummy_registry_test.yaml
# 使用 sed 或编辑器将 model.name: M_01_ISFM 修改为 model.name: M_04_ISFM_Registry
# 所有的 embedding/backbone/task_head 参数保持不变

```

```

```