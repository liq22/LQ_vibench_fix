
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
* **重要现实约束**：`model_factory` 会 import `src.model_factory.{type}.{name}`，因此 `model.name` 必须对应 `src/model_factory/ISFM/<name>.py` 的模块文件名；而 `configs/demo/00_smoke/dummy_dg.yaml` 不含 `model:`，模型字段来自 `base_configs.model` 指向的 `configs/base/model/*.yaml`。

# Execution Plan (执行步骤)

## Step 1: 创建注册中心（复用仓库现有 Registry 工具）
新建文件 `src/model_factory/ISFM/registry.py`。
* 复用 `src/utils/registry.py::Registry`，在 ISFM 内建立三个 registry：Embedding / Backbone / TaskHead。
* 提供 `register_backbone`, `register_head`, `register_embedding`（decorator 形式，供 `__init__.py` 追加注册使用）。
* 提供 `bootstrap()`：首次调用时 import `src.model_factory.ISFM.backbone / embedding / task_head`，触发各自 `__init__.py` 的注册逻辑。
* 提供 `get_backbone/get_embedding/get_head`：找不到 key 时给出可用选项，便于定位配置拼写问题。

## Step 2: 实施“无侵入”注册
修改以下三个文件的 `__init__.py`，在文件末尾**追加**注册逻辑（保留原有 export 不变）：
* `src/model_factory/ISFM/backbone/__init__.py`
* `src/model_factory/ISFM/task_head/__init__.py`
* `src/model_factory/ISFM/embedding/__init__.py`
* **操作**：基于 `__all__` 做自动注册（不手写长名单），注册 key 直接使用类名字符串，保证与 `M_01_ISFM.py` 的 dict key 字面一致。
* **错误处理策略**：默认不吞异常（导入失败应尽早暴露）；如确有“可选依赖缺失但 baseline 仍需跑”的历史包袱，再添加最小化的 `ImportError` warn（不要静默 `pass`）。

## Step 3: 派生新模型 M_04
1.  复制：`cp src/model_factory/ISFM/M_01_ISFM.py src/model_factory/ISFM/M_04_ISFM_Registry.py`
2.  重构 `M_04_ISFM_Registry.py`：
    * 保留所有 import（为了兼容性）。
    * **删除** `Embedding_dict`, `Backbone_dict`, `TaskHead_dict` 定义。
    * 修改 `__init__` 方法：
        * 调用 `bootstrap()` 触发注册。
        * 使用 `get_backbone/get_embedding/get_head` 替代字典查找。
        * (注意参数名是 `args_m`)。
3.  可选导出：可在 `src/model_factory/ISFM/__init__.py` 中导出 `M_04_ISFM_Registry`（不影响 `model_factory` 的按模块路径导入）。

## Step 4: 冒烟测试配置（符合 base_configs 叠加机制）
推荐做法（更可追溯）：
1. 新建 `configs/base/model/backbone_dlinear_registry.yaml`（从 `configs/base/model/backbone_dlinear.yaml` 复制，仅改 `model.name: "M_04_ISFM_Registry"`）。
2. 新建 `configs/demo/00_smoke/dummy_dg_registry.yaml`（从 `configs/demo/00_smoke/dummy_dg.yaml` 复制，仅改 `base_configs.model` 指向上面的新 base model）。

备选做法（不加文件，适合临时验证）：
* `python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override model.name=M_04_ISFM_Registry`

## Step 5: 验收
* 旧模型：`python main.py --config configs/demo/00_smoke/dummy_dg.yaml`
* 新模型：`python main.py --config configs/demo/00_smoke/dummy_dg_registry.yaml`（或用 CLI override 方案）
* 可选（若新增 configs）：`python -m scripts.validate_configs`

# Deliverables (代码产物)
请生成以下代码块（可直接写入文件）。

## 1. `src/model_factory/ISFM/registry.py`
```python
from __future__ import annotations

from typing import Any, Type

from src.utils.registry import Registry

class RegistryKeyError(KeyError):
    """Raised when a component key is missing from the ISFM registries."""

_BOOTSTRAPPED = False

BACKBONES: Registry = Registry()
EMBEDDINGS: Registry = Registry()
HEADS: Registry = Registry()

def bootstrap() -> None:
    """Lazy import to trigger auto-registration in component packages."""
    global _BOOTSTRAPPED
    if _BOOTSTRAPPED:
        return
    _BOOTSTRAPPED = True
    from . import backbone  # noqa: F401
    from . import embedding  # noqa: F401
    from . import task_head  # noqa: F401

def register_backbone(name: str):
    return BACKBONES.register(name)

def register_embedding(name: str):
    return EMBEDDINGS.register(name)

def register_head(name: str):
    return HEADS.register(name)

def _get_or_raise(registry: Registry, name: str, kind: str) -> Any:
    try:
        return registry.get(name)
    except KeyError as exc:  # pragma: no cover - defensive error path
        options = ", ".join(sorted(registry.available().keys()))
        raise RegistryKeyError(f"Unknown {kind}: '{name}'. Available: {options}") from exc

def get_backbone(name: str) -> Type:
    return _get_or_raise(BACKBONES, name, "backbone")

def get_embedding(name: str) -> Type:
    return _get_or_raise(EMBEDDINGS, name, "embedding")

def get_head(name: str) -> Type:
    return _get_or_raise(HEADS, name, "task_head")

```

## 2. `src/model_factory/ISFM/backbone/__init__.py` (Append Snippet)

*请在文件末尾追加以下代码（不要删除原有内容）：*

```python
# ... (保留原有 imports)

# --- Registry Auto-Registration ---
from ..registry import register_backbone

for _name in __all__:
    _obj = globals().get(_name)
    if isinstance(_obj, type):
        register_backbone(_name)(_obj)

```

## 3. `src/model_factory/ISFM/embedding/__init__.py` (Append Snippet)

*请在文件末尾追加以下代码（不要删除原有内容）：*

```python
# ... (保留原有 imports)

# --- Registry Auto-Registration ---
from ..registry import register_embedding

for _name in __all__:
    _obj = globals().get(_name)
    if isinstance(_obj, type):
        register_embedding(_name)(_obj)

```

## 4. `src/model_factory/ISFM/task_head/__init__.py` (Append Snippet)

*请在文件末尾追加以下代码（不要删除原有内容）：*

```python
# ... (保留原有 imports)

# --- Registry Auto-Registration ---
from ..registry import register_head

for _name in __all__:
    _obj = globals().get(_name)
    if isinstance(_obj, type):
        register_head(_name)(_obj)

```

## 5. `src/model_factory/ISFM/M_04_ISFM_Registry.py` (Core Logic)

*这是基于 M_01 修改后的核心代码片段，请确保替换掉原有的 Dict 定义和 **init** 逻辑：*

```python
# ... (Imports same as M_01)
from src.model_factory.ISFM.registry import bootstrap, get_backbone, get_embedding, get_head

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
        bootstrap()

        # 2. 从 Registry 获取类 (替代原来的 Dict[key])
        EmbeddingCls = get_embedding(args_m.embedding)
        BackboneCls = get_backbone(args_m.backbone)
        TaskHeadCls = get_head(args_m.task_head)

        # 3. 实例化 (保持与 M_01 完全一致的参数传递)
        self.embedding = EmbeddingCls(args_m)
        self.backbone = BackboneCls(args_m)
        
        self.num_classes = self.get_num_classes()
        args_m.num_classes = self.num_classes
        
        self.task_head = TaskHeadCls(args_m)

    # ... (get_num_classes, _embed, _encode, _head, forward 等方法保持原样)

```

## 6. 冒烟配置生成命令（推荐的“新增 base + 新增 demo”）

*直接运行以下 Shell 命令生成测试配置（更贴合当前仓库的 base_configs 机制）：*

```bash
cp configs/base/model/backbone_dlinear.yaml configs/base/model/backbone_dlinear_registry.yaml
# 编辑 configs/base/model/backbone_dlinear_registry.yaml:
# 将 model.name: "M_01_ISFM" 改为 model.name: "M_04_ISFM_Registry"

cp configs/demo/00_smoke/dummy_dg.yaml configs/demo/00_smoke/dummy_dg_registry.yaml
# 编辑 configs/demo/00_smoke/dummy_dg_registry.yaml:
# 将 base_configs.model 改为 "configs/base/model/backbone_dlinear_registry.yaml"
```
