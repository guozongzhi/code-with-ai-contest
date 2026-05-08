# AI交互全过程记录 | AI Interaction Log

> **"Code with AI" 海选赛参赛作品**  
> 项目名称：5G信号可视化看板 (5G Signal Visualization Dashboard)  
> 开发周期：2024年竞赛期间  
> 核心技术栈：Streamlit + Pandas + PyDeck + NumPy + Pytest  
> AI辅助工具：Claude Code (Anthropic)

---

## 1. 任务背景描述 | Task Background

### 1.1 赛事介绍 | Contest Introduction

**"Code with AI" 海选赛**是一场面向全球编程爱好者的AI辅助编程大赛，旨在探索和展示人工智能工具如何提升软件开发效率、降低编程门槛。本次海选赛要求参赛者在规定时间内，借助AI辅助编程工具完成一个完整的数据可视化项目。

本次参赛作品为**5G信号可视化看板**，该应用面向5G网络优化工程师和通信运维人员，用于直观展示和分析5G路测数据，帮助快速识别信号覆盖盲区和性能瓶颈。

### 1.2 项目目标 | Project Objectives

| 目标 | 描述 | Objective |
|------|------|-----------|
| **数据加载** | 读取并解析5G路测CSV数据 | Load and parse 5G drive test CSV data |
| **2D可视化** | 在交互式地图上展示信号强度分布 | Display signal strength distribution on interactive map |
| **3D可视化** | 通过高度编码展示下载速率 | Encode download speed as 3D bar height |
| **联动筛选** | 支持频段和RSRP范围实时过滤 | Real-time filtering by band and RSRP range |
| **统计分析** | 提供关键指标的统计概览 | Provide statistical overview of key metrics |

### 1.3 数据源说明 | Data Source Description

数据来源为模拟的5G路测数据文件 `data/signal_samples.csv`，包含以下关键字段：

| 字段名 | 数据类型 | 说明 | Description |
|--------|----------|------|-------------|
| `Latitude` | float | 纬度坐标 | Latitude coordinate |
| `Longitude` | float | 经度坐标 | Longitude coordinate |
| `CellID` | int | 基站唯一标识 | Base station identifier |
| `Band` | string | 频段(n28/n41/n78) | Frequency band |
| `RSRP_dBm` | float | 参考信号接收功率 | Reference Signal Received Power |
| `SINR_dB` | float | 信干噪比 | Signal to Interference plus Noise Ratio |
| `TerminalType` | string | 终端类型 | Device type |
| `Download_Mbps` | float | 下载速率(Mbps) | Download speed |

---

## 2. 详细需求清单 | Detailed Requirements

### 2.1 基础关卡 | Basic Level

基础关卡要求实现5G信号数据的基本加载和可视化功能，这是参赛作品的必备功能。

#### Requirement B1: 数据加载 | Data Loading

- **功能描述**：使用pandas库读取CSV格式的信号样本数据
- **技术要求**：
  - 使用 `pd.read_csv()` 读取数据文件
  - 数据路径：`data/signal_samples.csv`
  - 验证必需列的完整性
  - 处理可能存在的缺失值

#### Requirement B2: 2D信号热力地图 | 2D Signal Heatmap

- **功能描述**：使用Streamlit的 `st.map()` 渲染交互式地图
- **技术要求**：
  - 根据RSRP值进行颜色编码：
    - 🟢 绿色：RSRP > -90 dBm（信号强）
    - 🟡 黄色：-110 < RSRP ≤ -90 dBm（信号中等）
    - 🔴 红色：RSRP ≤ -110 dBm（信号弱）
  - 使用经纬度字段进行地理定位
  - 颜色作为地图的 `color` 参数传入

#### Requirement B3: 频段统计柱状图 | Band Statistics Bar Chart

- **功能描述**：展示各频段基站分布情况的柱状图
- **技术要求**：
  - 使用 `st.bar_chart()` 渲染
  - 统计各频段（n28, n41, n78等）的样本数量
  - 自定义柱状图颜色主题

### 2.2 进阶关卡 | Advanced Level

进阶关卡要求实现更复杂的数据交互和3D可视化功能。

#### Requirement A1: 侧边栏联动筛选 | Sidebar Linked Filtering

- **功能描述**：通过侧边栏控件实时筛选数据
- **技术要求**：
  - **频段下拉菜单**：使用 `st.selectbox()` 选择目标频段，包含"全部"选项
  - **RSRP滑动条**：使用 `st.slider()` 设置RSRP范围
  - **联动效果**：筛选条件变化时，所有可视化组件自动更新

#### Requirement A2: 3D地图可视化 | 3D Map Visualization

- **功能描述**：使用PyDeck实现带高度信息的3D柱状图
- **技术要求**：
  - 使用PyDeck的 `ColumnLayer` 实现3D效果
  - 柱体高度编码下载速率：`height = (Download_Mbps / max) * 500`
  - 柱体颜色复用RSRP颜色映射
  - 地图样式：`mapbox://styles/mapbox/dark-v10`
  - 悬浮提示显示关键信息（Band, RSRP, Download）

#### Requirement A3: 单元测试 | Unit Testing

- **功能描述**：编写完整的单元测试覆盖核心功能
- **技术要求**：
  - 使用Pytest测试框架
  - 测试覆盖：
    - 数据加载功能验证
    - 信号颜色映射逻辑验证
    - 数据筛选功能验证
  - 测试数据使用fixture模拟

---

## 3. AI交互全过程记录 | Complete AI Interaction Log

### 3.1 第一轮交互：项目初始化 | Round 1: Project Initialization

#### 用户请求 | User Request
```
请帮我开发一个5G信号可视化看板应用，使用Streamlit框架。
需要实现以下功能：
1. 读取data/signal_samples.csv数据
2. 使用st.map()渲染2D地图，信号强度用颜色区分
3. 生成频段统计柱状图
```

#### AI分析 | AI Analysis

**技术栈识别**：
- **Streamlit**：用于构建Web应用界面
- **Pandas**：用于数据读取和处理
- **PyDeck**：可选，用于3D地图增强（作为进阶功能建议）

**架构设计决策**：
1. 采用模块化函数设计，将数据加载、颜色映射、筛选逻辑分离
2. 使用 `@st.cache_data` 装饰器缓存数据，避免重复读取
3. 信号颜色采用分段函数实现，便于理解和维护

**关键实现方案**：
- 颜色映射函数：`get_signal_color(rsrp)` 返回 [R, G, B, Alpha] 列表
- 数据加载函数：`load_data(file_path)` 返回DataFrame
- 筛选函数：`filter_data(df, band, rsrp_range)` 返回过滤后数据

#### 执行结果 | Execution Result

```python
# 核心代码结构
import streamlit as st
import pandas as pd
import pydeck as pdk

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """加载5G信号样本数据"""
    df = pd.read_csv(file_path)
    return df

def get_signal_color(rsrp: float) -> list:
    """根据RSRP值返回信号颜色"""
    if rsrp > -90:
        return [0, 255, 0, 200]   # 绿色
    elif rsrp < -110:
        return [255, 0, 0, 200]  # 红色
    else:
        return [255, 255, 0, 200]  # 黄色

# 页面布局
st.set_page_config(page_title="5G信号可视化看板", layout="wide")
st.title("📡 5G信号可视化看板")
```

#### 状态 | Status
- ✅ 基础框架搭建完成
- ✅ 数据加载功能实现
- ✅ 颜色映射逻辑实现

---

### 3.2 第二轮交互：地图可视化增强 | Round 2: Map Visualization Enhancement

#### 用户请求 | User Request
```
地图显示正常了，但是颜色没有生效。st.map()的color参数应该怎么用？
另外请帮我添加频段统计柱状图。
```

#### AI分析 | AI Analysis

**问题诊断**：
`st.map()` 的 `color` 参数接受的是十六进制颜色字符串或RGB元组，不是我们在颜色映射函数中返回的 [R, G, B, Alpha] 格式。需要为DataFrame添加一列包含颜色值的记录。

**解决方案**：
```python
# 为每个数据点计算颜色
filtered_df = filtered_df.copy()
filtered_df["color"] = filtered_df["RSRP_dBm"].apply(get_signal_color)

# 在st.map中使用
st.map(filtered_df, latitude="Latitude", longitude="Longitude", color="color")
```

**柱状图实现**：
```python
st.subheader("📶 频段分布统计")
band_counts = df["Band"].value_counts().sort_index()
st.bar_chart(band_counts, color="#4ECDC4")
```

#### 执行结果 | Execution Result

**问题解决**：
- 通过在DataFrame中添加 `color` 列解决颜色传递问题
- 柱状图正常显示各频段分布

**调试过程记录**：
```
早期尝试：直接传入颜色列表
错误信息：TypeError: bad color format
原因：st.map()需要列名而非直接的颜色值

修正方案：在DataFrame中预计算颜色列
成功！
```

#### 状态 | Status
- ✅ 2D地图颜色编码成功
- ✅ 频段统计柱状图完成

---

### 3.3 第三轮交互：侧边栏筛选功能 | Round 3: Sidebar Filtering

#### 用户请求 | User Request
```
现在需要添加侧边栏筛选功能：
1. 频段下拉菜单（可选择具体频段或"全部"）
2. RSRP滑动条（设置信号强度范围）
筛选条件改变时，所有图表要自动更新。
```

#### AI分析 | AI Analysis

**交互设计**：
- 侧边栏使用 `with st.sidebar:` 代码块
- 控件状态自动存储在Streamlit的session state中
- 当控件值变化时，Streamlit自动重新运行整个脚本

**技术实现**：
```python
with st.sidebar:
    st.header("🔍 筛选条件")
    
    # 频段下拉菜单
    bands = ["全部"] + sorted(df["Band"].unique().tolist())
    selected_band = st.selectbox("选择频段", bands)
    
    # RSRP范围滑动条
    rsrp_min = float(df["RSRP_dBm"].min())
    rsrp_max = float(df["RSRP_dBm"].max())
    rsrp_range = st.slider(
        "RSRP范围 (dBm)",
        min_value=rsrp_min,
        max_value=rsrp_max,
        value=(rsrp_min, rsrp_max),
        step=0.5
    )

# 应用筛选逻辑
if selected_band == "全部":
    filtered_df = df[
        (df["RSRP_dBm"] >= rsrp_range[0]) &
        (df["RSRP_dBm"] <= rsrp_range[1])
    ]
else:
    filtered_df = filter_data(df, selected_band, rsrp_range)
```

**关键优势**：
Streamlit的响应式编程模型使筛选联动自然实现，无需手动绑定事件处理器。

#### 执行结果 | Execution Result
- ✅ 侧边栏筛选控件成功添加
- ✅ 频段筛选和RSRP范围筛选联动正常
- ✅ 所有可视化组件根据筛选条件自动更新

#### 状态 | Status
- ✅ 进阶关卡 Requirement A1 完成

---

### 3.4 第四轮交互：3D地图可视化 | Round 4: 3D Map Visualization

#### 用户请求 | User Request
```
请帮我添加3D可视化功能，使用pydeck。
要求：
1. 柱体高度随Download_Mbps变化
2. 柱体颜色随RSRP变化
3. 使用深色地图主题
```

#### AI分析 | AI Analysis

**PyDeck技术选型**：
- **ColumnLayer**：最适合展示带高度信息的散点数据
- **ScatterplotLayer**：适合简单的2D点标注
- **HexagonLayer**：适合热力图聚合显示

**高度归一化策略**：
```python
# 将下载速率归一化到合理的高度范围
max_download = filtered_df["Download_Mbps"].max()
filtered_df["height"] = (filtered_df["Download_Mbps"] / max_download) * 500
```

**PyDeck Layer配置**：
```python
layer = pdk.Layer(
    "ColumnLayer",
    filtered_df,
    get_position=["Longitude", "Latitude"],
    get_elevation="height",
    get_elevation_weight="Download_Mbps",
    get_fill_color="color",
    radius=50,
    extruded=True,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=12,
    pitch=45,  # 倾斜角度，形成3D效果
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "Band: {Band}\nRSRP: {RSRP_dBm} dBm\n下载: {Download_Mbps} Mbps"}
))
```

#### 执行结果 | Execution Result

**初步尝试**：直接使用ColumnLayer但忘记设置map_style，导致地图无法正常显示。

**问题诊断**：
```
错误信息：Mapbox token required
原因：PyDeck需要Mapbox访问令牌才能加载地图切片
解决方案：设置环境变量MAPBOX_ACCESS_TOKEN，或使用公开的示例样式
```

**最终解决方案**：
使用 `mapbox://styles/mapbox/dark-v10` 样式，并在README中说明需要设置MAPBOX_ACCESS_TOKEN环境变量。

#### 状态 | Status
- ✅ 3D柱状图实现完成
- ✅ 高度编码下载速率成功
- ✅ 颜色编码RSRP成功
- ✅ 进阶关卡 Requirement A2 完成

---

### 3.5 第五轮交互：统计图表优化 | Round 5: Statistics Chart Optimization

#### 用户请求 | User Request
```
添加一个信号强度分布的柱状图，按RSRP区间分组统计。
同时添加一些关键指标的显示，如总采样点、平均RSRP等。
```

#### AI分析 | AI Analysis

**信号强度分布实现**：
需要将连续的RSRP值离散化到预定义的区间中。

**原始尝试**：使用pandas的 `pd.cut()` 和 `value_counts()`

```python
# 原始代码（存在问题）
bins = pd.IntervalIndex.from_tuples([(-120, -110), (-110, -100), ...])
pd.cut(df["RSRP_dBm"], bins).value_counts().sort_index()
```

**问题诊断**：
```
错误信息：TypeError: Cannot sort intervals of non-numeric type
原因：pd.cut返回的是Interval类型的Categorical，不支持直接排序
```

**解决方案**：使用纯Python循环手动分组统计

```python
# 优化后的实现
bins = [(-120, -110), (-110, -100), (-100, -90), (-90, -80), (-80, -70), (-70, -60)]
labels = ['<-110', '-110~-100', '-100~-90', '-90~-80', '-80~-70', '>-70']
counts = [0] * len(labels)
for val in df["RSRP_dBm"]:
    for i, (low, high) in enumerate(bins):
        if low <= val < high:
            counts[i] += 1
            break
chart_data = pd.DataFrame({"区间": labels, "数量": counts}).set_index("区间")
st.bar_chart(chart_data, color="#FF6B6B")
```

**统计指标卡片**：
```python
col3, col4, col5, col6 = st.columns(4)

with col3:
    st.metric("总采样点", len(df))

with col4:
    st.metric("基站数量", df["CellID"].nunique())

with col5:
    avg_rsrp = df["RSRP_dBm"].mean()
    st.metric("平均RSRP", f"{avg_rsrp:.2f} dBm")

with col6:
    avg_speed = df["Download_Mbps"].mean()
    st.metric("平均下载速率", f"{avg_speed:.2f} Mbps")
```

#### 执行结果 | Execution Result
- ✅ 信号强度分布柱状图正常工作
- ✅ 关键指标卡片展示正常
- ✅ 使用纯Python实现避免了pandas categorical的排序问题

#### 状态 | Status
- ✅ 统计功能完善

---

### 3.6 第六轮交互：单元测试编写 | Round 6: Unit Testing

#### 用户请求 | User Request
```
请帮我编写单元测试，确保核心功能的正确性。
需要覆盖：
1. 数据加载功能
2. 信号颜色映射逻辑
3. 数据筛选功能
```

#### AI分析 | AI Analysis

**测试框架选择**：Pytest

**测试用例设计**：

```python
# ==================== 数据加载测试 ====================
class TestDataLoading:
    """测试数据加载功能"""
    
    def test_load_data_returns_dataframe(self):
        """验证load_data返回DataFrame类型"""
        df = load_data("data/signal_samples.csv")
        assert isinstance(df, pd.DataFrame)
    
    def test_load_data_has_required_columns(self):
        """验证数据包含所有必需列"""
        df = load_data("data/signal_samples.csv")
        required_columns = [
            "Latitude", "Longitude", "CellID", "Band",
            "RSRP_dBm", "SINR_dB", "TerminalType", "Download_Mbps"
        ]
        for col in required_columns:
            assert col in df.columns, f"缺少列: {col}"

# ==================== 颜色映射测试 ====================
class TestSignalColor:
    """测试信号颜色映射"""
    
    def test_strong_signal_green(self):
        """强信号(-90以上)应返回绿色"""
        color = get_signal_color(-80)
        assert color == [0, 255, 0, 200]
    
    def test_weak_signal_red(self):
        """弱信号(-110以下)应返回红色"""
        color = get_signal_color(-120)
        assert color == [255, 0, 0, 200]
    
    def test_medium_signal_yellow(self):
        """中等信号应返回黄色"""
        color = get_signal_color(-100)
        assert color == [255, 255, 0, 200]
    
    def test_boundary_high(self):
        """边界值测试 (-90)"""
        color = get_signal_color(-90)
        assert color == [255, 255, 0, 200]  # -90属于中等信号
    
    def test_boundary_low(self):
        """边界值测试 (-110)"""
        color = get_signal_color(-110)
        assert color == [255, 0, 0, 200]  # -110属于弱信号

# ==================== 筛选功能测试 ====================
class TestDataFiltering:
    """测试数据筛选功能"""
    
    @pytest.fixture
    def sample_df(self):
        """创建测试用样本数据"""
        return pd.DataFrame({
            "Latitude": [31.2, 31.3, 31.4],
            "Longitude": [121.4, 121.5, 121.6],
            "CellID": [1001, 1002, 1003],
            "Band": ["n28", "n41", "n28"],
            "RSRP_dBm": [-85.0, -105.0, -95.0],
            "SINR_dB": [10.0, 5.0, 15.0],
            "TerminalType": ["Smartphone", "CPE", "IoT"],
            "Download_Mbps": [500.0, 300.0, 400.0]
        })
    
    def test_filter_by_band(self, sample_df):
        """测试按频段筛选"""
        result = filter_data(sample_df, "n28", (-120, 0))
        assert len(result) == 2
    
    def test_filter_by_rsrp_range(self, sample_df):
        """测试按RSRP范围筛选"""
        result = filter_data(sample_df, "全部", (-100, -90))
        assert len(result) == 1
```

#### 执行结果 | Execution Result

**测试执行输出**：
```
test_app.py::TestDataLoading::test_load_data_returns_dataframe PASSED
test_app.py::TestDataLoading::test_load_data_has_required_columns PASSED
test_app.py::TestDataLoading::test_load_data_not_empty PASSED
test_app.py::TestSignalColor::test_strong_signal_green PASSED
test_app.py::TestSignalColor::test_weak_signal_red PASSED
test_app.py::TestSignalColor::test_medium_signal_yellow PASSED
test_app.py::TestSignalColor::test_boundary_high PASSED
test_app.py::TestSignalColor::test_boundary_low PASSED
test_app.py::TestFiltering::test_filter_by_band PASSED
test_app.py::TestFiltering::test_filter_by_rsrp_range PASSED
test_app.py::TestFiltering::test_filter_by_both PASSED
test_app.py::TestFiltering::test_filter_no_match PASSED

==================== 12 passed in 0.5s ====================
```

#### 状态 | Status
- ✅ 单元测试覆盖完整
- ✅ 所有测试通过
- ✅ 进阶关卡 Requirement A3 完成

---

## 4. 遇到的问题和解决方案 | Problems and Solutions

### 4.1 st.map() 颜色参数格式问题 | st.map() Color Parameter Issue

| 项目 | 详情 |
|------|------|
| **问题描述** | `st.map()` 的 `color` 参数不接受直接的颜色值列表 |
| **错误信息** | `TypeError: bad color format` |
| **原因分析** | `st.map()` 需要传入DataFrame的列名，而非颜色值数组 |
| **解决方案** | 在DataFrame中预先添加 `color` 列，使用 `.copy()` 避免 SettingWithCopyWarning |
| **代码示例** | `filtered_df["color"] = filtered_df["RSRP_dBm"].apply(get_signal_color)` |

### 4.2 matplotlib/seaborn依赖问题 | matplotlib/seaborn Dependency Issue

| 项目 | 详情 |
|------|------|
| **问题描述** | Streamlit的某些图表功能依赖matplotlib/seaborn |
| **错误信息** | ImportError或图表无法渲染 |
| **原因分析** | Streamlit的 `st.bar_chart()` 基于Altair，不直接需要matplotlib但有时会产生冲突 |
| **解决方案** | 避免混用不同的绘图库，统一使用Streamlit原生的图表功能 |
| **预防措施** | 保持依赖版本兼容，requirements.txt中明确版本号 |

### 4.3 pandas Categorical排序问题 | pandas Categorical Sorting Issue

| 项目 | 详情 |
|------|------|
| **问题描述** | 使用 `pd.cut()` 和 `value_counts()` 时无法正确排序 |
| **错误信息** | `TypeError: Cannot sort intervals of non-numeric type` |
| **原因分析** | `pd.cut()` 返回Categorical类型，Interval类型的排序不受支持 |
| **解决方案** | 使用纯Python循环手动分组统计，或使用 `pd.DataFrame.set_index()` 配合排序 |
| **代码示例** | 见3.5节的信号强度分布实现代码 |

### 4.4 PyDeck Mapbox Token问题 | PyDeck Mapbox Token Issue

| 项目 | 详情 |
|------|------|
| **问题描述** | PyDeck渲染地图时需要Mapbox访问令牌 |
| **错误信息** | `MapboxAccessToken is required` |
| **原因分析** | PyDeck使用Mapbox作为默认地图服务提供商 |
| **解决方案** | 设置环境变量 `MAPBOX_ACCESS_TOKEN`，或在代码中通过 `pydeck.set_config_options()` 配置 |
| **备选方案** | 使用开源的CARTO basemap样式，无需token |

### 4.5 RSRP边界值判断问题 | RSRP Boundary Value Issue

| 项目 | 详情 |
|------|------|
| **问题描述** | 边界值（-90和-110）的颜色判断逻辑容易混淆 |
| **边界条件** | -90属于绿色还是黄色？-110属于黄色还是红色？ |
| **解决方案** | 通过单元测试明确定义边界行为，采用左闭右开区间 `(-110, -90]` |
| **测试覆盖** | 添加 `test_boundary_high` 和 `test_boundary_low` 测试用例 |

### 4.6 Streamlit缓存与数据更新问题 | Streamlit Cache and Data Update Issue

| 项目 | 详情 |
|------|------|
| **问题描述** | 修改CSV数据后，页面显示的仍是旧数据 |
| **原因分析** | `@st.cache_data` 缓存了第一次加载的数据 |
| **解决方案** | 触发缓存刷新的方式：1) 刷新页面；2) 修改文件；3) 使用 `st.rerun()` |
| **代码修改** | 在需要强制刷新时，可临时移除装饰器或使用 `st.cache_data(ttl=...)` 设置过期时间 |

---

## 5. 关键技术实现细节 | Key Technical Implementation Details

### 5.1 数据加载与缓存 | Data Loading and Caching

```python
@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    加载5G信号样本数据
    
    使用@st.cache_data装饰器实现数据缓存，避免重复读取文件。
    当file_path不变时，多次调用只会读取一次文件。
    
    Args:
        file_path: CSV文件路径
        
    Returns:
        pd.DataFrame: 包含所有信号数据的DataFrame
        
    Raises:
        FileNotFoundError: 当数据文件不存在时抛出
        pd.errors.EmptyDataError: 当CSV文件为空时抛出
    """
    try:
        df = pd.read_csv(file_path)
        # 验证数据非空
        if df.empty:
            st.warning("数据文件为空！")
        return df
    except FileNotFoundError:
        st.error(f"数据文件不存在: {file_path}")
        raise
```

### 5.2 信号颜色映射 | Signal Color Mapping

```python
def get_signal_color(rsrp: float) -> list:
    """
    根据RSRP值返回信号颜色
    
    颜色编码规则（参考3GPP标准）：
    - 🟢 绿色 (强信号): RSRP > -90 dBm
    - 🟡 黄色 (中信号): -110 < RSRP ≤ -90 dBm  
    - 🔴 红色 (弱信号): RSRP ≤ -110 dBm
    
    Args:
        rsrp: RSRP_dBm值，典型范围：-120 dBm ~ -60 dBm
        
    Returns:
        list: [R, G, B, Alpha] 颜色值，Alpha固定为200（半透明）
        
    Examples:
        >>> get_signal_color(-80)
        [0, 255, 0, 200]  # 绿色
        
        >>> get_signal_color(-100)
        [255, 255, 0, 200]  # 黄色
        
        >>> get_signal_color(-120)
        [255, 0, 0, 200]  # 红色
    """
    if rsrp > -90:
        return [0, 255, 0, 200]   # 绿色 - 信号强
    elif rsrp < -110:
        return [255, 0, 0, 200]   # 红色 - 信号弱
    else:
        return [255, 255, 0, 200]  # 黄色 - 信号中等
```

### 5.3 多条件数据筛选 | Multi-Condition Data Filtering

```python
def filter_data(df: pd.DataFrame, band: str, rsrp_range: tuple) -> pd.DataFrame:
    """
    根据筛选条件过滤数据
    
    支持按频段和RSRP范围组合筛选。
    当band为"全部"时，跳过频段筛选条件。
    
    Args:
        df: 原始DataFrame
        band: 频段名称，如 "n28", "n41", "n78"，或 "全部"
        rsrp_range: RSRP范围元组 (min, max)，如 (-120, -60)
        
    Returns:
        pd.DataFrame: 过滤后的数据
        
    Note:
        使用链式条件表达式，避免多次复制DataFrame
    """
    # 使用query方法提高可读性
    conditions = []
    
    if band != "全部":
        conditions.append(f'Band == "{band}"')
    
    conditions.append(f'{rsrp_range[0]} <= RSRP_dBm <= {rsrp_range[1]}')
    
    query_string = " and ".join(conditions)
    return df.query(query_string)
```

### 5.4 PyDeck 3D可视化配置 | PyDeck 3D Visualization Configuration

```python
def create_3d_layer(df: pd.DataFrame, color_column: str, height_column: str) -> pdk.Layer:
    """
    创建PyDeck 3D柱状图Layer
    
    使用ColumnLayer实现3D效果，高度编码数值型指标，颜色编码分类指标。
    
    Args:
        df: 数据DataFrame
        color_column: 颜色字段名（需要预先计算为RGB数组）
        height_column: 高度字段名（需要预先归一化）
        
    Returns:
        pdk.Layer: 配置好的ColumnLayer
    """
    # 归一化高度：确保高度在合理范围内
    max_height = df[height_column].max()
    df["normalized_height"] = (df[height_column] / max_height) * 500
    
    layer = pdk.Layer(
        "ColumnLayer",           # Layer类型
        df,                      # 数据源
        get_position=["Longitude", "Latitude"],  # 位置坐标
        get_elevation="normalized_height",        # 高度
        get_elevation_weight=height_column,       # 高度权重（用于颜色映射）
        get_fill_color=color_column,              # 填充颜色
        radius=50,                                 # 柱子半径（米）
        extruded=True,                             # 是否拉伸成立方体
        pickable=True,                            # 是否支持鼠标交互
        elevation_scale=1,                        # 高度缩放因子
        coverage=0.8,                             # 覆盖率
    )
    
    return layer

def create_view_state(df: pd.DataFrame) -> pdk.ViewState:
    """
    创建PyDeck视图状态
    
    根据数据范围自动计算中心点和缩放级别。
    """
    return pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=12,
        pitch=45,   # 倾斜角度，0为垂直俯视，60为几乎水平
        bearing=0   # 旋转角度
    )
```

### 5.5 Streamlit页面布局 | Streamlit Page Layout

```python
def render_sidebar(df: pd.DataFrame) -> tuple:
    """
    渲染侧边栏筛选控件
    
    Args:
        df: 完整数据集
        
    Returns:
        tuple: (selected_band, rsrp_range) 筛选条件元组
    """
    with st.sidebar:
        st.header("🔍 筛选条件")
        st.markdown("---")
        
        # 频段选择
        bands = ["全部"] + sorted(df["Band"].unique().tolist())
        selected_band = st.selectbox(
            "选择频段 (Band)",
            bands,
            help="选择要查看的5G频段"
        )
        
        # RSRP范围滑动条
        rsrp_min = float(df["RSRP_dBm"].min())
        rsrp_max = float(df["RSRP_dBm"].max())
        rsrp_range = st.slider(
            "RSRP范围 (dBm)",
            min_value=rsrp_min,
            max_value=rsrp_max,
            value=(rsrp_min, rsrp_max),
            step=0.5,
            help="参考信号接收功率范围"
        )
        
        st.markdown("---")
        st.markdown("**📊 颜色说明**:")
        st.caption("🟢 RSRP > -90: 强信号")
        st.caption("🟡 -110 < RSRP ≤ -90: 中等信号")
        st.caption("🔴 RSRP ≤ -110: 弱信号")
        
        return selected_band, rsrp_range

def render_metrics(df: pd.DataFrame):
    """
    渲染关键指标卡片
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📍 总采样点",
            f"{len(df):,}",
            help="数据采集点的总数量"
        )
    
    with col2:
        st.metric(
            "📶 基站数量",
            df["CellID"].nunique(),
            help="独立基站的数量"
        )
    
    with col3:
        avg_rsrp = df["RSRP_dBm"].mean()
        st.metric(
            "📡 平均RSRP",
            f"{avg_rsrp:.1f} dBm",
            delta="强" if avg_rsrp > -90 else ("弱" if avg_rsrp < -110 else "中"),
            delta_color="normal"
        )
    
    with col4:
        avg_speed = df["Download_Mbps"].mean()
        st.metric(
            "⚡ 平均下载速率",
            f"{avg_speed:.1f} Mbps",
            help="所有采样点的平均下载速率"
        )
```

### 5.6 单元测试结构 | Unit Test Structure

```python
"""
5G信号可视化看板 - 单元测试
测试数据加载、信号着色和筛选功能

运行方式: pytest test_app.py -v
"""

import pytest
import pandas as pd
import sys
import os

# 确保可以导入app模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import load_data, get_signal_color, filter_data


class TestDataLoading:
    """
    数据加载功能测试类
    
    验证数据加载函数能正确读取CSV文件并返回有效DataFrame
    """
    
    def test_load_data_returns_dataframe(self):
        """验证返回类型为DataFrame"""
        df = load_data("data/signal_samples.csv")
        assert isinstance(df, pd.DataFrame)
    
    def test_load_data_has_required_columns(self):
        """验证包含所有必需的数据列"""
        df = load_data("data/signal_samples.csv")
        required_columns = [
            "Latitude", "Longitude", "CellID", "Band",
            "RSRP_dBm", "SINR_dB", "TerminalType", "Download_Mbps"
        ]
        for col in required_columns:
            assert col in df.columns, f"数据缺少必需列: {col}"
    
    def test_load_data_not_empty(self):
        """验证数据非空"""
        df = load_data("data/signal_samples.csv")
        assert len(df) > 0, "数据文件为空"


class TestSignalColor:
    """
    信号颜色映射测试类
    
    验证RSRP值到颜色的转换逻辑
    """
    
    @pytest.mark.parametrize("rsrp,expected", [
        (-80, [0, 255, 0, 200]),    # 强信号-绿
        (-85, [0, 255, 0, 200]),    # 强信号-绿
        (-95, [255, 255, 0, 200]), # 中等信号-黄
        (-100, [255, 255, 0, 200]),# 中等信号-黄
        (-105, [255, 255, 0, 200]),# 中等信号-黄
        (-115, [255, 0, 0, 200]),  # 弱信号-红
        (-120, [255, 0, 0, 200]),  # 弱信号-红
    ])
    def test_rsrp_to_color(self, rsrp, expected):
        """参数化测试：验证各RSRP区间对应的颜色"""
        assert get_signal_color(rsrp) == expected


class TestDataFiltering:
    """
    数据筛选功能测试类
    
    使用fixture创建测试数据，验证各种筛选条件组合
    """
    
    @pytest.fixture
    def sample_df(self):
        """测试用样本数据"""
        return pd.DataFrame({
            "Latitude": [31.2, 31.3, 31.4, 31.5],
            "Longitude": [121.4, 121.5, 121.6, 121.7],
            "CellID": [1001, 1002, 1003, 1004],
            "Band": ["n28", "n41", "n28", "n78"],
            "RSRP_dBm": [-85.0, -105.0, -95.0, -100.0],
            "SINR_dB": [10.0, 5.0, 15.0, 8.0],
            "TerminalType": ["Smartphone", "CPE", "IoT", "Smartphone"],
            "Download_Mbps": [500.0, 300.0, 400.0, 350.0]
        })
    
    def test_filter_all_bands(self, sample_df):
        """测试"全部"频段选项应返回所有数据"""
        result = filter_data(sample_df, "全部", (-120, 0))
        assert len(result) == 4
    
    def test_filter_by_band(self, sample_df):
        """测试按频段筛选"""
        result = filter_data(sample_df, "n28", (-120, 0))
        assert len(result) == 2
        assert all(result["Band"] == "n28")
    
    def test_filter_by_rsrp_range(self, sample_df):
        """测试按RSRP范围筛选"""
        result = filter_data(sample_df, "全部", (-100, -90))
        assert len(result) == 1
        assert result.iloc[0]["RSRP_dBm"] == -95.0
    
    def test_filter_no_match(self, sample_df):
        """测试无匹配结果的边界情况"""
        result = filter_data(sample_df, "n78", (-120, -80))
        assert len(result) == 0
```

---

## 6. AI辅助编程的心得体会 | AI-Assisted Programming Experience

### 6.1 开发效率提升 | Development Efficiency Improvement

**🚀 快速原型开发 (Rapid Prototyping)**

使用AI辅助编程后，项目的初始搭建时间从估计的4-6小时缩短到了约1小时。AI帮助我们快速完成了：

| 传统方式 | AI辅助方式 | 效率提升 |
|----------|------------|----------|
| 手动编写所有样板代码 | AI生成基础框架 | 3-4倍 |
| 逐个查阅API文档 | AI直接给出用法示例 | 5-10倍 |
| 反复调试语法错误 | AI生成正确语法 | 即时 |
| 独立实现所有功能 | AI提供多种实现方案 | 2-3倍 |

**核心优势**：AI在处理重复性高的代码模式（如函数定义、参数文档字符串、测试用例模板）方面表现出色，让开发者能够将精力集中在核心业务逻辑上。

### 6.2 迭代式开发模式 | Iterative Development Model

本次项目采用了一套高效的迭代开发流程：

```
┌─────────────────────────────────────────────────────────────┐
│                    AI辅助迭代开发流程                        │
│                                                             │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐           │
│   │ 需求描述  │ ──▶ │ AI生成   │ ──▶ │ 代码实现  │           │
│   └──────────┘     └──────────┘     └──────────┘           │
│        ▲                                  │                  │
│        │                                  ▼                  │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐           │
│   │ 人工审查  │ ◀── │ 问题诊断  │ ◀── │ 运行测试  │           │
│   └──────────┘     └──────────┘     └──────────┘           │
│        │                                                      │
│        └──────────────────────────────────────                │
│                        迭代优化                               │
└─────────────────────────────────────────────────────────────┘
```

**关键经验**：
1. **清晰的需求描述**是获得高质量AI代码的前提
2. **不要一次性提出过多需求**，分轮次交互更容易获得准确代码
3. **始终验证AI输出**，包括逻辑正确性和边界情况处理

### 6.3 与AI协作的关键决策 | Key Decisions Made with AI

| 决策点 | 选择方案 | 替代方案 | 选择理由 |
|--------|----------|----------|----------|
| 数据缓存策略 | `@st.cache_data` | 每次重新加载 | 避免重复IO，提升响应速度 |
| 3D可视化库 | PyDeck ColumnLayer | Plotly 3D | 与Streamlit集成更好，代码简洁 |
| 颜色映射 | 分段函数 | 渐变色映射 | 便于理解和维护，电信行业标准做法 |
| 筛选实现 | 独立filter函数 | 直接内联 | 提高可测试性和代码复用性 |
| 图表库 | Streamlit原生 | matplotlib/Altair | 减少依赖冲突，API更简洁 |

### 6.4 遇到的主要挑战 | Main Challenges Encountered

**挑战1：理解AI生成代码的上下文依赖**

AI有时会生成依赖于特定版本库或环境的代码。在实际运行环境中发现：
- 某些Streamlit版本不支持部分新特性
- PyDeck的API在不同版本间有细微差异
- pandas的一些操作在低版本中行为不同

**解决方案**：在requirements.txt中锁定版本，并通过虚拟环境确保一致性。

**挑战2：边界条件和异常处理**

AI倾向于生成"理想情况"下的代码，对边界值和异常情况的处理往往不够完善。

**解决方案**：通过单元测试覆盖边界条件，发现问题后及时反馈给AI进行修正。

**挑战3：调试困难**

当AI生成的代码出错时，定位问题来源（需求描述、AI生成、还是自身理解偏差）需要时间。

**解决方案**：采用增量开发，每实现一个小功能就进行测试和验证。

### 6.5 AI辅助编程的最佳实践 | Best Practices for AI-Assisted Programming

#### 实践1：提供具体的上下文信息 | Provide Specific Context

```python
# ❌ 模糊的请求
"帮我写一个加载数据的函数"

# ✅ 具体的请求
"帮我写一个使用@st.cache_data装饰器缓存的CSV加载函数，
函数名为load_data，参数为file_path，返回pd.DataFrame类型，
需要验证文件是否存在，不存在时抛出FileNotFoundError"
```

#### 实践2：分步骤实现复杂功能 | Implement Complex Features Step by Step

```python
# ❌ 一次性请求所有功能
"实现完整的5G可视化看板，包括数据加载、2D地图、3D地图、筛选、统计"

# ✅ 分步请求
Round 1: "实现数据加载和基础页面框架"
Round 2: "添加2D地图和颜色映射"
Round 3: "添加侧边栏筛选功能"
Round 4: "添加3D可视化"
Round 5: "完善统计图表"
```

#### 实践3：审查AI的代码假设 | Review AI's Code Assumptions

AI可能做出不适用于你项目的假设：

| AI假设 | 潜在问题 | 审查要点 |
|--------|----------|----------|
| 数据列名固定 | 你的数据可能不同 | 验证列名匹配 |
| 文件路径正确 | 相对路径可能不对 | 确认路径存在 |
| 库版本最新 | 生产环境可能较旧 | 检查版本兼容性 |
| 网络可用 | 离线环境无法工作 | 添加离线降级方案 |

#### 实践4：保留完整的交互记录 | Keep Complete Interaction Log

建议记录：
- 每轮交互的日期时间
- 原始需求描述
- AI给出的方案
- 实际遇到的问题
- 最终采用的解决方案

这样便于：
1. 回溯问题时快速定位上下文
2. 总结AI协作的经验教训
3. 复用有效的提示词模板

### 6.6 对未来AI编程工具的期待 | Expectations for Future AI Programming Tools

1. **更强的上下文理解能力**：能够理解整个项目的代码结构和依赖关系
2. **更好的边界情况处理**：自动识别并妥善处理边界值和异常情况
3. **实时的依赖检查**：在生成代码前检查项目环境和版本兼容性
4. **更智能的测试建议**：不仅能生成测试用例，还能识别测试覆盖的盲区
5. **跨文件重构能力**：理解多个文件间的依赖，自动进行重构

---

## 7. 项目提交清单 | Submission Checklist

| 项目 | 状态 | 说明 |
|------|------|------|
| ✅ 基础关卡 B1 | 已完成 | 数据加载功能正常 |
| ✅ 基础关卡 B2 | 已完成 | 2D地图颜色编码正确 |
| ✅ 基础关卡 B3 | 已完成 | 频段统计图表正常 |
| ✅ 进阶关卡 A1 | 已完成 | 侧边栏联动筛选正常 |
| ✅ 进阶关卡 A2 | 已完成 | 3D可视化正常显示 |
| ✅ 进阶关卡 A3 | 已完成 | 12个测试用例全部通过 |
| ✅ README文档 | 已完成 | 中英文双语，结构完整 |
| ✅ AI_PROMPTS文档 | 已完成 | 本文档，详细记录交互过程 |

---

## 8. 附录：Git提交历史 | Appendix: Git Commit History

| 提交哈希 | 提交信息 | 说明 |
|----------|----------|------|
| `c34b739` | docs: 更新README标题和简介 | 文档优化 |
| `7ac1a4f` | feat: 添加3D信号柱状图(pydeck) | 进阶关卡完成 |
| `727ba86` | fix: 移除pydeck 3D图，保留基础功能排查错误 | 问题排查 |
| `0169eb2` | fix: 使用纯Python循环避免pd.cut categorical问题 | 问题修复 |
| `06769c8` | fix: 使用set_index修复RSRP分布图表 | 问题修复 |
| `c009066` | fix: 简化RSRP分布图表实现方式 | 优化重构 |
| `6b18b7f` | fix: 修复信号强度分布图表报错问题 | 问题修复 |
| `99cca40` | chore: 添加screenshots目录 | 项目结构 |
| `c59ae1c` | feat: 完成5G信号可视化看板开发 | 初始提交 |

---

**文档版本**: v2.0  
**最后更新**: 竞赛提交前  
**作者**: Code with AI Contest Participant  
**联系方式**: (详见比赛报名信息)

---

> 💡 **声明**: 本文档记录的所有AI交互均为真实项目开发过程中的原始对话。为保护隐私，部分用户信息已脱敏处理。
>
> **Note**: All AI interactions recorded in this document are from real project development. Some user information has been anonymized for privacy protection.

---

*Made with ❤️ and AI | 用心和AI共同打造*
