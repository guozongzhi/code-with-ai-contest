"""
5G信号可视化看板 - 单元测试
测试数据加载、信号着色和筛选功能
"""

import pytest
import pandas as pd
from app import load_data, get_signal_color, filter_data


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
    
    def test_load_data_not_empty(self):
        """验证数据不为空"""
        df = load_data("data/signal_samples.csv")
        assert len(df) > 0


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
        """边界值测试 (-90): 等于-90时不属于大于-90范围，应返回黄色"""
        color = get_signal_color(-90)
        assert color == [255, 255, 0, 200]
    
    def test_boundary_low(self):
        """边界值测试 (-110): 等于-110时不属于小于-110范围，应返回黄色"""
        color = get_signal_color(-110)
        assert color == [255, 255, 0, 200]


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
        assert all(result["Band"] == "n28")
    
    def test_filter_by_rsrp_range(self, sample_df):
        """测试按RSRP范围筛选: -95.0在(-100,-90)范围内，仅1行"""
        result = filter_data(sample_df, "n28", (-100, -90))
        assert len(result) == 1
        assert result.iloc[0]["RSRP_dBm"] == -95.0
    
    def test_filter_by_both(self, sample_df):
        """测试组合筛选"""
        result = filter_data(sample_df, "n28", (-100, -90))
        assert len(result) == 1
    
    def test_filter_no_match(self, sample_df):
        """测试无匹配情况"""
        result = filter_data(sample_df, "n78", (-120, 0))
        assert len(result) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
