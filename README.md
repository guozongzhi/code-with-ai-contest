# 📡 5G 信号可视化看板

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python" alt="Python 3.13">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/PyDeck-0.8+-green" alt="PyDeck">
  <img src="https://img.shields.io/badge/Test-12/12%20passed-success" alt="Tests">
  <img src="https://img.shields.io/badge/AI-Claude%20Code%20(DeepSeek%20V4)-purple" alt="AI Tool">
</p>

> **"Code with AI" 海选赛参赛作品**
>
> 面向 5G 网络优化工程师的交互式信号数据看板。支持 2D 热力地图、3D 柱状图、侧边栏实时联动筛选，帮助快速识别信号覆盖盲区和性能瓶颈。

---

## 📋 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [数据说明](#-数据说明)
- [项目结构](#-项目结构)
- [运行截图](#-运行截图)
- [技术架构](#-技术架构)
- [测试](#-测试)
- [AI 开发心得](#-ai-开发心得)

---

## ✨ 功能特性

### 🟢 基础关卡

| 功能 | 说明 |
|------|------|
| **数据加载** | 使用 `@st.cache_data` 缓存加载 CSV，避免重复 I/O |
| **2D 热力地图** | `st.map()` 渲染交互式地图，经纬度自动定位 |
| **信号颜色编码** | RSRP → RGBA 三段式映射 (绿/黄/红)，直观区分信号质量 |
| **频段分布统计** | 按频段 (n28/n41/n78) 聚合统计，柱状图展示基站数量分布 |

### 🔵 进阶关卡

| 功能 | 说明 |
|------|------|
| **联动筛选** | 侧边栏支持频段下拉 + RSRP 范围滑动条，所有图表实时联动更新 |
| **3D 柱状图** | 基于 PyDeck ColumnLayer，柱体高度编码下载速率，颜色编码信号强度 |
| **统计仪表盘** | 总采样点、基站数量、平均 RSRP、平均下载速率 4 项核心指标 |
| **原始数据查看** | 可展开的交互式数据表格，支持排序和搜索 |

### 📊 信号颜色编码规则

参照 3GPP 信号强度标准定义：

```
🟢 绿色    RSRP > -90 dBm          信号强 — 覆盖良好，用户体验优秀
🟡 黄色    -110 ≤ RSRP ≤ -90 dBm   信号中等 — 覆盖一般，需要关注
🔴 红色    RSRP < -110 dBm         信号弱 — 覆盖盲区，需要优化
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/guozongzhi/code-with-ai-contest.git
cd code-with-ai-contest

# 2. 创建虚拟环境
python3 -m venv env
source env/bin/activate      # macOS / Linux
# env\Scripts\activate       # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

### 依赖清单

| 依赖 | 版本 | 用途 |
|------|------|------|
| streamlit | ≥ 1.28.0 | Web 应用框架 |
| pandas | ≥ 2.0.0 | 数据处理与分析 |
| pydeck | ≥ 0.8.0 | 3D 地图可视化 |
| numpy | ≥ 1.24.0 | 数值计算 |
| pytest | ≥ 7.4.0 | 单元测试 |

### 启动

```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501`

```bash
# 运行测试
pytest test_app.py -v
```

---

## 📊 数据说明

数据文件位于 `data/signal_samples.csv`，为模拟的 5G 路测数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| `Latitude` | float | 纬度坐标 |
| `Longitude` | float | 经度坐标 |
| `CellID` | int | 基站唯一标识 |
| `Band` | string | 频段 (n28 / n41 / n78) |
| `RSRP_dBm` | float | 参考信号接收功率，范围约 -120 ~ -60 dBm |
| `SINR_dB` | float | 信干噪比，衡量信号质量 |
| `TerminalType` | string | 终端类型 (Smartphone / CPE / IoT) |
| `Download_Mbps` | float | 下载速率，单位 Mbps |

**示例数据：**

| Latitude | Longitude | CellID | Band | RSRP_dBm | SINR_dB | TerminalType | Download_Mbps |
|----------|-----------|--------|------|----------|---------|--------------|---------------|
| 31.2091 | 121.4829 | 1926 | n28 | -94.94 | 5.44 | Smartphone | 138.21 |
| 31.2142 | 121.4848 | 1457 | n78 | -105.47 | 20.67 | CPE | 837.84 |
| 31.2500 | 121.4536 | 1941 | n28 | -82.27 | 18.28 | Smartphone | 36.23 |

---

## 📁 项目结构

```
code-with-ai-contest/
├── app.py                 # Streamlit 主应用 (~200 行)
├── test_app.py            # Pytest 单元测试 (12 项)
├── requirements.txt       # Python 依赖
├── README.md              # 项目文档
├── AI_PROMPTS.md          # AI 交互全过程记录
├── data/
│   └── signal_samples.csv # 5G 信号样本数据
└── screenshots/
    ├── 2D map.png         # 2D 信号热力地图
    ├── 3D map.png         # 3D 信号柱状图
    ├── chart.png          # 频段统计 & 信号强度分布
    └── excel.png          # 原始数据表格视图
```

---

## 📸 运行截图

### 2D 信号热力地图

![2D 地图](screenshots/2D%20map.png)

*每个散点按 RSRP 值着色，绿色=强信号、黄色=中等、红色=弱信号*

### 3D 信号柱状图

![3D 地图](screenshots/3D%20map.png)

*柱体高度编码下载速率，颜色编码信号强度，白色底图展示道路和建筑信息*

### 统计图表

![统计图表](screenshots/chart.png)

*左侧：各频段基站数量分布；右侧：RSRP 信号强度区间统计*

### 原始数据视图

![数据视图](screenshots/excel.png)

*可展开、排序、搜索的交互式数据表格*

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit 页面层                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  侧边栏   │  │  2D 地图  │  │  3D 柱状图        │  │
│  │  筛选控件  │  │  st.map  │  │  PyDeck Column   │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  统计图表  │  │  指标卡片  │  │  数据表格        │  │
│  │  bar_chart │  │  metric  │  │  dataframe       │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────┤
│                    纯函数层 (可测试)                    │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ load_data  │  │get_signal_clr│  │ filter_data │ │
│  │ + @cache   │  │ RSRP→RGBA    │  │ Band+RSRP   │ │
│  └────────────┘  └──────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────┤
│                     数据层                            │
│  ┌────────────────────────────────────────────────┐ │
│  │         data/signal_samples.csv                 │ │
│  │  8 字段 × N 条记录 (Lat/Lon/Cell/Band/RSRP/...) │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**设计原则：**

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个函数只做一件事，`load_data` 只加载，`get_signal_color` 只映射 |
| **UI 与逻辑分离** | 三个核心函数无 Streamlit 依赖，可独立测试 |
| **无过度抽象** | 单文件应用，无需引入类、工厂模式等 |
| **可扩展** | `filter_data` 通过 mask 变量组合条件，新增筛选项只需一行 |

---

## 🧪 测试

### 运行

```bash
pytest test_app.py -v
```

### 结果

```text
test_app.py::TestDataLoading::test_load_data_returns_dataframe PASSED
test_app.py::TestDataLoading::test_load_data_has_required_columns PASSED
test_app.py::TestDataLoading::test_load_data_not_empty PASSED
test_app.py::TestSignalColor::test_strong_signal_green PASSED
test_app.py::TestSignalColor::test_weak_signal_red PASSED
test_app.py::TestSignalColor::test_medium_signal_yellow PASSED
test_app.py::TestSignalColor::test_boundary_high PASSED
test_app.py::TestSignalColor::test_boundary_low PASSED
test_app.py::TestDataFiltering::test_filter_by_band PASSED
test_app.py::TestDataFiltering::test_filter_by_rsrp_range PASSED
test_app.py::TestDataFiltering::test_filter_by_both PASSED
test_app.py::TestDataFiltering::test_filter_no_match PASSED

============================== 12 passed in 0.59s ==============================
```

### 覆盖范围

| 测试类 | 覆盖内容 | 用例数 |
|--------|----------|--------|
| `TestDataLoading` | 数据加载：返回类型、列完整性、非空校验 | 3 |
| `TestSignalColor` | 颜色映射：强/弱/中信号 + 两个边界值 | 5 |
| `TestDataFiltering` | 数据筛选：频段、RSRP 范围、组合条件、无匹配 | 4 |

- 筛选测试使用 `@pytest.fixture` 创建隔离样本数据，不依赖外部 CSV
- 边界值测试覆盖严格不等号的端点行为 (`-90` 和 `-110`)

---

## 💡 AI 开发心得

本项目在 **Claude Code (DeepSeek V4)** 辅助下完成开发。以下记录核心经验。

### 开发效率

AI 在样板代码、API 用法、测试模板方面效率极高，项目初始搭建时间从预计的 4-6 小时缩短到约 1 小时，开发者精力集中在核心可视化逻辑而非重复编码。

### 迭代模式

```
需求描述 → AI 生成 → 运行测试 → 问题诊断 → 人工审查 → 迭代循环
```

每轮聚焦一个功能，增量开发、即时验证。

### 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 缓存策略 | `@st.cache_data` | 避免重复 I/O，Streamlit 原生支持 |
| 3D 可视化 | PyDeck ColumnLayer | API 简洁，与 Streamlit 集成优于 Plotly 3D |
| 地图底图 | 内置 `"light"` 样式 | 零配置，无需 Mapbox API Token |
| 颜色映射 | 三段式分段函数 | 直观可维护，匹配 3GPP 信号标准 |
| 筛选逻辑 | `filter_data` 内聚"全部"处理 | 函数即单一入口，消除 UI 层分支 |
| RSRP 分布 | `pd.cut` + `.reindex()` | O(n) 复杂度，比手动循环更简洁 |

### 经验教训

1. **需求描述要精准** — 包含函数名、参数类型、返回值，AI 输出质量显著提升
2. **始终验证 AI 输出** — AI 倾向生成"理想情况"代码，边界条件需人工审查
3. **增量测试** — 每完成一个功能立刻运行测试，避免问题累积
4. **记录关键决策** — 标注"为什么这样选"，便于后续回溯和参赛答辩
5. **文档与代码同频更新** — 代码改动后及时同步文档，避免文档腐烂

> 详细 AI 交互过程见 [AI_PROMPTS.md](AI_PROMPTS.md)

---

## 📜 许可证

本项目为 **"Code with AI" 编程大赛** 参赛作品。

---


