# AI 交互全过程记录

> **"Code with AI" 海选赛参赛作品** — 5G信号可视化看板
> 技术栈：Streamlit + Pandas + PyDeck + NumPy + Pytest
> AI 工具：Claude Code (DeepSeek V4)

---

## 1. 项目背景

面向 5G 网络优化工程师的交互式信号数据看板，支持 2D/3D 地图可视化和实时筛选。

**数据源**：`data/signal_samples.csv`，包含 8 个字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| Latitude, Longitude | float | 经纬度 |
| CellID | int | 基站 ID |
| Band | string | 频段 (n28/n41/n78) |
| RSRP_dBm | float | 参考信号接收功率 |
| SINR_dB | float | 信干噪比 |
| TerminalType | string | 终端类型 |
| Download_Mbps | float | 下载速率 |

**需求分两级**：
- **基础关卡**：数据加载、2D 热力地图（RSRP 颜色编码）、频段统计柱状图
- **进阶关卡**：侧边栏联动筛选（频段 + RSRP 范围）、3D 柱状图（高度=下载速率）、单元测试

---

## 2. AI 交互轮次记录

### Round 1 — 项目初始化

**请求**：开发 Streamlit 5G 信号可视化看板，加载 CSV、渲染 2D 地图、颜色编码、频段统计。

**产出**：单文件架构 `app.py`，三个纯函数（`load_data`、`get_signal_color`、`filter_data`）+ Streamlit UI。`load_data` 加 `@st.cache_data` 缓存。

### Round 2 — 地图颜色不生效

**问题**：`st.map()` 的 `color` 参数需要 DataFrame 列名而非直接颜色值。

**解决**：在 DataFrame 中预计算 `color` 列（`apply(get_signal_color)`），传给 `st.map(color="color")`。

### Round 3 — 侧边栏筛选

**请求**：频段下拉 + RSRP 滑动条，筛选联动更新。

**实现**：`st.sidebar` + `st.selectbox` + `st.slider`，Streamlit 响应式模型自动触发重渲染。

**后续优化**：将 "全部" 判断从 UI 层 if/else 移入 `filter_data` 函数内部，消除代码重复。

### Round 4 — 3D 柱状图

**请求**：PyDeck ColumnLayer，高度编码下载速率，颜色编码 RSRP。

**演进过程**：
1. 初版用 `mapbox://styles/mapbox/dark-v10` → 需 token，底图空白
2. 切到 PyDeck 内置 `"dark"` → 免费，无需 token
3. 用户反馈改为 `"light"` 白色底图
4. 移除无效参数 `get_elevation_weight`，加 `coverage=0.8`、`auto_highlight`

### Round 5 — 统计图表

**请求**：RSRP 区间分布柱状图 + 关键指标卡片。

**演进过程**：
1. `pd.cut` + `IntervalIndex` → Categorical 排序报错
2. 纯 Python for 循环手动分组 → 可行但 O(n×m)
3. 回归 `pd.cut` + `.reindex(labels, fill_value=0)` → O(n)，5 行代码

### Round 6 — 单元测试

**请求**：Pytest 覆盖数据加载、颜色映射、筛选功能。

**修复记录**：
- 移除多余的 `sys.path` 操作（测试与 app.py 同目录）
- `test_boundary_high(-90)`：断言绿→黄（`-90 > -90` 为 False）
- `test_boundary_low(-110)`：断言红→黄（`-110 < -110` 为 False）
- `test_filter_by_rsrp_range`：band 从 "全部" 改为具体频段

**结果**：12 个测试全部通过。

---

## 3. 遇到的 6 个关键问题

| # | 问题 | 根因 | 解决方案 |
|----|------|------|----------|
| 1 | `st.map()` 颜色不生效 | color 参数需要列名 | DataFrame 预计算颜色列 |
| 2 | 3D 地图无底图 | Mapbox 样式需 token | 改用 PyDeck 内置 `"light"` |
| 3 | RSRP 分布图排序报错 | `pd.cut` 返回 Categorical | `.reindex(labels, fill_value=0)` |
| 4 | 边界值测试断言错误 | 严格不等 `>` / `<` | 修正断言匹配实际函数行为 |
| 5 | `filter_data` 不支持"全部" | 逻辑分散在 UI 层 | "全部"判断内聚进函数 |
| 6 | 测试导入失败 | `sys.path` 多余操作 | 删除，同目录直接 import |

---

## 4. 项目架构

```
app.py                  # 单文件 ~200 行
├── load_data()         # CSV 加载 + @st.cache_data
├── get_signal_color()  # RSRP → RGBA (三段式分段函数)
├── filter_data()       # 频段 + RSRP 组合筛选 (含"全部")
└── Streamlit UI        # 侧边栏、2D 地图、3D 柱状图、统计图表

test_app.py             # 单元测试 ~100 行
├── TestDataLoading     # 3 tests
├── TestSignalColor     # 5 tests (含边界值)
└── TestDataFiltering   # 4 tests
```

**设计原则**：单一职责、UI 与逻辑分离、可测试（三函数均无 Streamlit 依赖）、无多余抽象。

---

## 5. AI 协作心得

**效率提升**：项目初始搭建从 4-6 小时缩短到约 1 小时。AI 在样板代码、API 用法、测试模板方面效率最高。

**迭代模式**：需求描述 → AI 生成 → 运行测试 → 问题诊断 → 人工审查 → 循环。每轮聚焦一个功能。

**关键教训**：
- 需求描述要具体（函数名、参数、返回值、异常处理）
- 分步请求优于一次性全量
- AI 倾向生成"理想情况"代码，边界条件需通过测试覆盖
- AI 对库版本差异不敏感，需用虚拟环境锁定依赖

**关键决策**：

| 决策 | 选择 | 理由 |
|------|------|------|
| 缓存 | `@st.cache_data` | 避免重复 IO |
| 3D 库 | PyDeck ColumnLayer | 与 Streamlit 集成好 |
| 地图底图 | 内置 `"light"` | 零配置，无需 token |
| 筛选 | `filter_data` 内聚 | 单入口，易测试 |
| RSRP 分布 | `pd.cut` + reindex | O(n)，代码简洁 |

---

## 6. 提交清单

| 关卡 | 状态 |
|------|------|
| B1 数据加载 | ✅ |
| B2 2D 地图颜色编码 | ✅ |
| B3 频段统计图表 | ✅ |
| A1 侧边栏联动筛选 | ✅ |
| A2 3D 可视化 | ✅ |
| A3 单元测试 (12 passed) | ✅ |
| README 文档 | ✅ |
| AI_PROMPTS 文档 | ✅ |

---

## 7. Git 提交历史

| Hash | Type | Message |
|------|------|---------|
| `6d77b7b` | docs | 添加应用界面截图 (2D/3D 地图、图表、数据视图) |
| `6f4e6c0` | fix | 修复 test_app.py 边界值断言和导入问题 |
| `a354efd` | docs | 完善 AI_PROMPTS.md — 详细记录 AI 交互全过程 |
| `c34b739` | docs | 更新 README 标题和简介 |
| `7ac1a4f` | feat | 添加 3D 信号柱状图 (pydeck ColumnLayer) |
| `727ba86` | fix | 移除 pydeck 3D 图，保留基础功能排查错误 |
| `0169eb2` | fix | 使用纯 Python 循环避免 pd.cut categorical 排序问题 |
| `06769c8` | fix | 使用 set_index 修复 RSRP 分布图表 |
| `c009066` | fix | 简化 RSRP 分布图表实现方式 |
| `6b18b7f` | fix | 修复信号强度分布图表报错 — 用 pd.cut 替代 hist |
| `99cca40` | chore | 添加 screenshots 目录 |
| `c59ae1c` | feat | 完成 5G 信号可视化看板开发（初始版本） |

---

*Made with ❤️ and AI*
