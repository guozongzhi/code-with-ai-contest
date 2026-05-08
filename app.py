"""
5G信号可视化看板 - Streamlit应用
功能：加载5G信号数据，渲染热力地图，支持侧边栏筛选和3D可视化
"""

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# ==========================================
# 配置与数据加载
# ==========================================

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    加载5G信号样本数据
    
    Args:
        file_path: CSV文件路径
        
    Returns:
        pd.DataFrame: 包含所有信号数据的DataFrame
    """
    df = pd.read_csv(file_path)
    return df


def get_signal_color(rsrp: float) -> list:
    """
    根据RSRP值返回信号颜色
    >-90dBm: 绿色(信号强)
    <-110dBm: 红色(信号弱)
    中间值: 黄色(信号中等)
    
    Args:
        rsrp: RSRP_dBm值
        
    Returns:
        list: [R, G, B, Alpha]颜色值
    """
    if rsrp > -90:
        return [0, 255, 0, 200]  # 绿色
    elif rsrp < -110:
        return [255, 0, 0, 200]  # 红色
    else:
        return [255, 255, 0, 200]  # 黄色


def filter_data(df: pd.DataFrame, band: str, rsrp_range: tuple) -> pd.DataFrame:
    """按频段和RSRP范围过滤数据，band为"全部"时不做频段筛选"""
    mask = (
        (df["RSRP_dBm"] >= rsrp_range[0]) &
        (df["RSRP_dBm"] <= rsrp_range[1])
    )
    if band != "全部":
        mask &= df["Band"] == band
    return df[mask]


# ==========================================
# 页面布局
# ==========================================

st.set_page_config(page_title="5G信号可视化看板", layout="wide")
st.title("📡 5G信号可视化看板")
st.markdown("实时监控5G基站信号强度与性能指标")

# 加载数据
df = load_data("data/signal_samples.csv")

# ==========================================
# 侧边栏筛选器
# ==========================================

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
    
    st.markdown("---")
    st.markdown("**筛选说明**:")
    st.caption("- RSRP > -90: 绿色(信号强)")
    st.caption("- RSRP < -110: 红色(信号弱)")
    st.caption("- 中间值: 黄色(信号中等)")

# 应用筛选
filtered_df = filter_data(df, selected_band, rsrp_range)

# ==========================================
# 地图可视化
# ==========================================

st.subheader("🗺️ 信号热力地图")

# 为每个数据点计算颜色
filtered_df["color"] = filtered_df["RSRP_dBm"].apply(get_signal_color)

# 2D地图 (st.map)
st.map(filtered_df, latitude="Latitude", longitude="Longitude", color="color")

# 3D柱状图 (pydeck)
st.subheader("📊 3D信号柱状图")

# 归一化下载速率用于柱体高度
max_speed = filtered_df["Download_Mbps"].max()
filtered_df["height"] = (filtered_df["Download_Mbps"] / max_speed) * 300

# 柱状图层：经纬度定位在地图上，高度=下载速率，颜色=信号强度
column_layer = pdk.Layer(
    "ColumnLayer",
    filtered_df,
    get_position=["Longitude", "Latitude"],
    get_elevation="height",
    get_fill_color="color",
    radius=30,
    elevation_scale=1,
    coverage=0.8,
    extruded=True,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=12,
    pitch=50,
    bearing=15,
)

st.pydeck_chart(pdk.Deck(
    map_style="light",
    initial_view_state=view_state,
    layers=[column_layer],
    tooltip={
        "html": "<b>频段: {Band}</b><br/>"
                "RSRP: {RSRP_dBm} dBm<br/>"
                "SINR: {SINR_dB} dB<br/>"
                "下载速率: {Download_Mbps} Mbps<br/>"
                "终端: {TerminalType}"
    },
))

# ==========================================
# 数据概览图表
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📶 频段分布统计")
    band_counts = df["Band"].value_counts().sort_index()
    st.bar_chart(band_counts, color="#4ECDC4")

with col2:
    st.subheader("📈 信号强度分布")
    # RSRP信号强度分布统计
    bins = [-120, -110, -100, -90, -80, -70, -60]
    labels = ['<-110', '-110~-100', '-100~-90', '-90~-80', '-80~-70', '>-70']
    counts = (
        pd.cut(df["RSRP_dBm"], bins=bins, labels=labels, right=False)
        .value_counts(sort=False)
        .reindex(labels, fill_value=0)
    )
    chart_data = pd.DataFrame({"区间": labels, "数量": counts.values}).set_index("区间")
    st.bar_chart(chart_data, color="#FF6B6B")

# ==========================================
# 数据统计信息
# ==========================================

st.markdown("---")
st.subheader("📋 数据统计概览")

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

# 显示原始数据
with st.expander("查看原始数据"):
    st.dataframe(filtered_df, use_container_width=True)
