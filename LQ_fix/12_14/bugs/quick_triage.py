#!/usr/bin/env python3
"""
快速分析和triage扫描结果
使用方法：python docs/LQ_fix/12_14/bugs/quick_triage.py
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / ".git").exists():
            return parent
    return here.parents[5]


def load_scan_results(scan_dir: Path) -> dict[str, list[str]]:
    """加载扫描结果（优先读取 *_py.txt / *_yaml.txt）。"""
    scan_files = {
        "todo_py": "rg_todo_fixme_hack_py.txt",
        "todo_yaml": "rg_todo_fixme_hack_yaml.txt",
        "except_bare_py": "rg_except_bare_py.txt",
        "except_exception_py": "rg_except_exception_py.txt",
        "except_baseexception_py": "rg_except_baseexception_py.txt",
        "assert_raise_py": "rg_assert_raise_py.txt",
        "paths_envs_py": "rg_paths_envs_py.txt",
        "paths_envs_yaml": "rg_paths_envs_yaml.txt",
    }

    results: dict[str, list[str]] = {}
    for category, filename in scan_files.items():
        filepath = scan_dir / filename
        if filepath.exists():
            results[category] = [
                line.strip()
                for line in filepath.read_text(encoding="utf-8", errors="replace").splitlines()
                if line.strip()
            ]
        else:
            results[category] = []
    return results

def analyze_priority(items: list[str], category: str) -> dict[str, list[dict[str, str]]]:
    """分析项目优先级（粗粒度 heuristic，用于快速 triage）。"""
    priority_items: dict[str, list[dict[str, str]]] = {"P0": [], "P1": [], "P2": [], "P3": []}

    for item in items:
        # 解析文件路径和行号
        if ":" not in item:
            continue
        parts = item.split(":", 2)
        if len(parts) < 2:
            continue
        filepath = parts[0]
        line_num = parts[1]
        content = parts[2] if len(parts) > 2 else ""

        # 根据类别和内容判断优先级
        priority = "P3"  # 默认轻微

        if category == "except_bare_py":
            if filepath.startswith("src/"):
                priority = "P0"
            elif filepath.startswith("dev/scripts/"):
                priority = "P1"
            else:
                priority = "P2"

        elif category == "except_baseexception_py":
            priority = "P0" if filepath.startswith("src/") else "P1"

        elif category == "except_exception_py":
            priority = "P1" if filepath.startswith("src/") else "P2"

        elif category in ("todo_py", "todo_yaml"):
            if "FIXME" in item:
                priority = "P1" if filepath.startswith("src/") else "P2"
            else:
                priority = "P2" if filepath.startswith("src/") else "P3"

        elif category in ("paths_envs_py", "paths_envs_yaml"):
            if "/home/" in item or "/mnt/" in item:
                priority = "P1" if filepath.startswith(("src/", "configs/")) else "P2"
            elif "PROJECT_HOME" in item or "VBENCH_HOME" in item:
                priority = "P2"
            else:
                priority = "P3"

        elif category == "assert_raise_py":
            if filepath.startswith("src/"):
                priority = "P2"
            else:
                priority = "P3"

        priority_items[priority].append({
            'file': filepath,
            'line': line_num,
            'content': content,
            'full': item
        })

    return priority_items

def _top_files(items: list[str], limit: int = 10) -> list[tuple[str, int]]:
    counter = Counter()
    for item in items:
        if ":" not in item:
            continue
        filepath = item.split(":", 1)[0]
        counter[filepath] += 1
    return counter.most_common(limit)


def generate_triage_report(results: dict[str, list[str]], output_dir: Path) -> Path:
    """生成 triage 报告（Markdown）。"""
    report: list[str] = []
    report.append("# 快速 Triage 报告（代码与配置）\n")
    report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 统计总数
    total_items = sum(len(items) for items in results.values())
    report.append(f"## 扫描结果统计\n")
    report.append(f"- 总计发现 {total_items} 个潜在问题\n")

    for category, items in results.items():
        if items:
            report.append(f"- {category}: {len(items)} 条\n")

    report.append("\n## Top 文件（每类最多 10 个）\n\n")
    for category, items in results.items():
        if not items:
            continue
        report.append(f"### {category}\n\n")
        for fp, cnt in _top_files(items, 10):
            report.append(f"- {cnt} × `{fp}`\n")
        report.append("\n")

    report.append("\n## 高优先级问题（需要立即关注）\n\n")

    # 分析并排序所有问题
    all_prioritized = {
        'P0': [],
        'P1': [],
        'P2': [],
        'P3': []
    }

    for category, items in results.items():
        prioritized = analyze_priority(items, category)
        for priority in ['P0', 'P1', 'P2', 'P3']:
            all_prioritized[priority].extend([(category, item) for item in prioritized[priority]])

    # 输出P0和P1问题
    for priority in ['P0', 'P1']:
        items = all_prioritized[priority]
        if items:
            priority_name = {'P0': '致命', 'P1': '严重'}[priority]
            report.append(f"### {priority} - {priority_name}级问题 ({len(items)}个)\n\n")

            for category, item in items[:10]:  # 只显示前10个
                report.append(f"**{category}** - `{item['file']}:{item['line']}`\n")
                report.append(f"```python\n{item['content'][:200]}\n```\n\n")

            if len(items) > 10:
                report.append(f"...还有 {len(items) - 10} 个{priority_name}问题\n\n")

    # 生成详细检查清单
    report.append("\n## 详细检查清单\n\n")

    for category, items in results.items():
        if items:
            report.append(f"### {category} ({len(items)}条)\n\n")

            # 按文件分组
            by_file = defaultdict(list)
            for item in items:
                if ':' in item:
                    parts = item.split(':', 2)
                    if len(parts) >= 2:
                        filepath = parts[0]
                        by_file[filepath].append(item)

            for filepath, file_items in sorted(by_file.items()):
                report.append(f"**文件：{filepath}**\n")
                for item in file_items[:5]:  # 每个文件最多显示5条
                    report.append(f"  - Line {item.split(':')[1]}: {item[:100]}...\n")
                report.append("\n")

    # 保存报告
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "quick_triage_report.md"
    report_path.write_text("".join(report), encoding="utf-8")
    return report_path

def main():
    """主函数"""
    # 目录设置
    repo_root = _find_repo_root()
    scan_dir = repo_root / "docs" / "LQ_fix" / "12_14" / "bugs" / "reports" / "scan_logs"
    if not scan_dir.exists():
        scan_dir = repo_root / "docs" / "LQ_fix" / "12_14" / "reports" / "scan_logs"
    output_dir = repo_root / "docs" / "LQ_fix" / "12_14" / "bugs" / "reports"

    print("=== PHM-Vibench 快速Triage分析 ===\n")

    # 加载扫描结果
    print("1. 加载扫描结果...")
    results = load_scan_results(scan_dir)

    # 生成报告
    print("2. 生成triage报告...")
    report_path = generate_triage_report(results, output_dir)

    # 输出摘要
    print("\n3. 分析摘要：")
    total = sum(len(items) for items in results.values())
    print(f"   - 总计发现 {total} 个潜在问题")

    # 统计P0/P1
    p0_count = 0
    p1_count = 0
    for category, items in results.items():
        prioritized = analyze_priority(items, category)
        p0_count += len(prioritized['P0'])
        p1_count += len(prioritized['P1'])

    print(f"   - P0（致命）：{p0_count} 个")
    print(f"   - P1（严重）：{p1_count} 个")
    print(f"   - 详细报告：{report_path}")

    # 建议下一步
    print("\n4. 建议下一步操作：")
    if p0_count > 0:
        print("   - 立即检查P0级问题（可能导致系统崩溃）")
    if p1_count > 0:
        print("   - 优先处理P1级问题（影响核心功能）")
    print("   - 查看完整报告了解所有问题")
    print("   - 对每个问题进行深入调查并创建Bug记录")

if __name__ == "__main__":
    main()
