# 5G信号可视化看板

实时可视化5G基站信号强度与性能指标的Streamlit应用。

## 功能特性

### 基础功能
- 📊 **数据加载**: 使用pandas读取CSV格式的信号样本数据
- 🗺️ **信号热力地图**: 使用st.map()渲染交互式地图
- 📈 **信号颜色编码**: 
  - 绿色: RSRP > -90 dBm (信号强)
  - 黄色: -110 dBm < RSRP ≤ -90 dBm (信号中等)
  - 红色: RSRP ≤ -110 dBm (信号弱)
- 📶 **频段统计**: 柱状图展示各频段基站分布

### 进阶功能
- 🔍 **侧边栏筛选**: 支持按频段和RSRP范围实时筛选
- 📊 **3D柱状图**: 使用pydeck渲染，高度随下载速率变化
- 📋 **数据统计**: 显示采样点数量、基站数量、平均RSRP和下载速率

## 技术栈

- **Streamlit**: Web应用框架
- **Pandas**: 数据处理
- **PyDeck**: 3D地图可视化
- **NumPy**: 数值计算

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
streamlit run app.py
```

## 数据格式

CSV文件需包含以下字段：
- `Latitude`: 纬度
- `Longitude`: 经度
- `CellID`: 基站ID
- `Band`: 频段 (如 n28, n41, n78)
- `RSRP_dBm`: 参考信号接收功率
- `SINR_dB`: 信号与干扰加噪声比
- `TerminalType`: 终端类型
- `Download_Mbps`: 下载速率

## 项目结构

```
.
├── app.py              # 主应用
├── test_app.py         # 单元测试
├── requirements.txt    # 依赖列表
├── README.md           # 文档
├── AI_PROMPTS.md       # AI交互日志
└── data/
    └── signal_samples.csv  # 样本数据
```

## 测试

```bash
pytest test_app.py -v
```
