# 📡 5G Signal Visualization Dashboard

> **"Code with AI" 海选赛参赛作品 — Built with Claude Code + Streamlit**
>
> 一个交互式 5G 路测信号可视化 Web 看板，支持 2D 热力散点图、3D 柱状地图、侧边栏实时联动筛选，以及完整单元测试。

## Project Overview

This project is a data visualization application designed for monitoring and analyzing 5G network signal quality. It provides interactive maps, 3D visualizations, and real-time filtering capabilities for signal data collected from multiple 5G base stations across different frequency bands.

本项目是一款数据可视化应用，用于监控和分析5G网络信号质量。它提供交互式地图、3D可视化和实时筛选功能，帮助用户直观了解不同频段基站的信号覆盖和性能表现。

## ✨ Features | 功能特性

### 🟢 Basic Features | 基础功能

| Feature | Description | 功能说明 |
|---------|-------------|----------|
| **Data Loading** | Load CSV signal data with pandas | 使用pandas读取CSV格式的信号样本数据 |
| **Signal Heatmap** | Interactive 2D map using `st.map()` | 使用`st.map()`渲染交互式2D地图 |
| **Color-Coded Signals** | Visual RSRP indication by color | RSRP信号强度颜色编码显示 |
| **Band Statistics** | Bar chart showing base station distribution | 柱状图展示各频段基站分布 |

### 🔵 Advanced Features | 进阶功能

| Feature | Description | 功能说明 |
|---------|-------------|----------|
| **Sidebar Filtering** | Real-time filtering by band and RSRP range | 侧边栏联动筛选（频段+RSRP范围） |
| **3D Visualization** | PyDeck 3D column chart with light map background | 3D柱状图（白色底图），高度随下载速率变化 |
| **Data Statistics** | Key metrics: sample count, base stations, avg RSRP, avg speed | 数据统计：采样点、基站数、平均RSRP/下载速率 |
| **Raw Data View** | Expandable data table | 可展开的原始数据表格 |

### 📊 Signal Color Coding | 信号颜色编码

```
🟢 Green  | RSRP > -90 dBm   | Strong Signal   | 信号强
🟡 Yellow | -110 ≤ RSRP ≤ -90 dBm | Medium Signal | 信号中等
🔴 Red    | RSRP < -110 dBm  | Weak Signal     | 信号弱
```

## 🛠️ Tech Stack | 技术栈

| Technology | Purpose | 用途 |
|-------------|---------|------|
| **Streamlit** | Web application framework | Web应用框架 |
| **Pandas** | Data processing and analysis | 数据处理与分析 |
| **PyDeck** | 3D map visualization | 3D地图可视化 |
| **NumPy** | Numerical computation | 数值计算 |
| **Pytest** | Unit testing | 单元测试 |

## 📥 Installation | 安装

### Prerequisites | 环境要求

- Python 3.8+
- pip package manager

### Steps | 安装步骤

```bash
# 1. Clone the repository | 克隆仓库
git clone https://github.com/your-repo/code-with-ai-contest.git
cd code-with-ai-contest

# 2. Create & activate virtual environment | 创建并激活虚拟环境
python3 -m venv env
source env/bin/activate  # Linux/Mac
# env\Scripts\activate   # Windows

# 3. Install dependencies | 安装依赖
pip install -r requirements.txt
```

### requirements.txt

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
pydeck>=0.8.0
pytest>=7.4.0
```

## 🚀 Running | 运行

### Start the Application | 启动应用

```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

看板访问地址：`http://localhost:8501`

### Run Tests | 运行测试

```bash
pytest test_app.py -v
```

## 📊 Data Format | 数据格式

The application expects a CSV file at `data/signal_samples.csv` with the following structure:

应用期望CSV文件包含以下字段：

| Column | Type | Description | 说明 |
|--------|------|-------------|------|
| `Latitude` | float | Latitude coordinate | 纬度 |
| `Longitude` | float | Longitude coordinate | 经度 |
| `CellID` | int | Base station identifier | 基站ID |
| `Band` | string | Frequency band (e.g., n28, n41, n78) | 频段 |
| `RSRP_dBm` | float | Reference Signal Received Power (dBm) | 参考信号接收功率 |
| `SINR_dB` | float | Signal to Interference plus Noise Ratio (dB) | 信干噪比 |
| `TerminalType` | string | Device type (Smartphone/CPE/IoT) | 终端类型 |
| `Download_Mbps` | float | Download speed (Mbps) | 下载速率 |

### Sample Data | 示例数据

```csv
Latitude,Longitude,CellID,Band,RSRP_dBm,SINR_dB,TerminalType,Download_Mbps
31.209143,121.482867,1926,n28,-94.94,5.44,Smartphone,138.21
31.214219,121.484829,1457,n78,-105.47,20.67,CPE,837.84
31.249965,121.453557,1941,n28,-82.27,18.28,Smartphone,36.23
```

## 📁 Project Structure | 项目结构

```
code-with-ai-contest/
├── app.py                 # Main Streamlit application | 主应用
├── test_app.py            # Unit tests | 单元测试
├── requirements.txt       # Python dependencies | Python依赖
├── README.md              # This file | 项目文档
├── AI_PROMPTS.md          # AI interaction log | AI交互日志
├── data/
│   └── signal_samples.csv # Sample signal data | 信号样本数据
└── screenshots/           # Application screenshots | 应用截图
    └── (user screenshots)
```

## 📸 Screenshots | 运行截图

> **Note | 注意**: Please run the application and take your own screenshots to populate this directory.
> 
> 请运行应用后自行截图放入此目录。

Expected screenshots should include:
- Main dashboard with 2D signal heatmap
- 3D pydeck visualization
- Sidebar filtering controls
- Statistics overview

预期截图应包含：
- 主仪表盘与2D信号热力图
- 3D PyDeck可视化
- 侧边栏筛选控件
- 统计概览

## 🧪 Testing | 测试方法

### Run All Tests | 运行所有测试

```bash
pytest test_app.py -v
```

### Test Coverage | 测试覆盖

| Test Class | Coverage | 覆盖内容 |
|------------|----------|----------|
| `TestDataLoading` | Data loading and validation | 数据加载与验证 |
| `TestSignalColor` | Signal color mapping logic | 信号颜色映射逻辑 |
| `TestDataFiltering` | Data filtering functionality | 数据筛选功能 |

### Sample Test Output | 测试输出示例

```
test_app.py::TestDataLoading::test_load_data_returns_dataframe PASSED
test_app.py::TestDataLoading::test_load_data_has_required_columns PASSED
test_app.py::TestSignalColor::test_strong_signal_green PASSED
test_app.py::TestSignalColor::test_weak_signal_red PASSED
test_app.py::TestFiltering::test_filter_by_band PASSED
```

## 💡 Contest Experience | 参赛心得

### AI-Assisted Programming Experience | AI辅助编程经验分享

This project was developed with significant assistance from AI coding tools. Here are our key takeaways:

本项目在AI辅助下完成开发，以下是我们的关键心得：

#### 1. Rapid Prototyping | 快速原型开发

AI helped us quickly generate the initial application structure and boilerplate code, allowing us to focus on the core visualization logic rather than spending time on repetitive code patterns.

AI帮助我们快速生成初始应用结构和样板代码，使我们能够专注于核心可视化逻辑，而不是在重复代码模式上花费时间。

#### 2. Iterative Improvement | 迭代式改进

The development process followed an iterative pattern:
1. **Describe requirement** → AI generates code
2. **Test and identify issues** → Human review
3. **Refine requirements** → AI improves code
4. **Repeat**

开发过程遵循迭代模式：
1. **描述需求** → AI生成代码
2. **测试并发现问题** → 人工审查
3. **优化需求** → AI改进代码
4. **重复**

#### 3. Key Decisions Made with AI | 与AI协作的关键决策

| Decision | Rationale | 决策理由 |
|----------|-----------|----------|
| Use `@st.cache_data` | Improves performance by caching loaded data | 缓存数据加载，提升性能 |
| PyDeck ColumnLayer for 3D | Best balance of visual appeal and code simplicity | 视觉效果和代码简洁性的最佳平衡 |
| Separate filtering functions | Better code organization and testability | 更好的代码组织和可测试性 |

#### 4. Challenges and Solutions | 挑战与解决方案

**Challenge 1**: Initial 3D visualization was too dense
- **Solution**: Added slider filtering to reduce data points

**挑战1**: 初始3D可视化过于密集
- **解决方案**: 添加滑动条筛选减少数据点

**Challenge 2**: Color mapping boundary conditions
- **Solution**: Carefully defined threshold values with unit tests

**挑战2**: 颜色映射边界条件
- **解决方案**: 通过单元测试明确定义阈值

#### 5. Lessons Learned | 经验教训

1. **Be specific in prompts**: Clear requirements lead to better AI-generated code
2. **Always review AI output**: AI suggestions need human verification
3. **Test incrementally**: Build and test each feature as it's added
4. **Document decisions**: Keep track of why certain approaches were chosen

1. **提示要具体**: 清晰的需求会带来更好的AI生成代码
2. **始终审查AI输出**: AI建议需要人工验证
3. **增量测试**: 每次添加功能时都进行构建和测试
4. **记录决策**: 跟踪选择特定方法的原因

## 📜 License | 许可证

This project was created for the "Code with AI" programming contest.

本项目为"AI辅助编程"大赛参赛作品。

## 🙏 Acknowledgments | 致谢

- Streamlit Team for the amazing framework
- All contest organizers and volunteers

---

**Made with ❤️ and AI | 用心和AI共同打造**
