import numpy as np
from scipy.signal import welch
from typing import List, Dict, Union

def analyze_eeg(data: List[float], fs: float = 250.0) -> Dict[str, Union[Dict, float]]:
    """
    分析 EEG 數據中的 alpha 和 theta 波段
    
    參數:
    data: EEG 數據數組
    fs: 採樣率 (Hz)
    
    返回:
    包含 alpha 和 theta 功率的字典
    """
    try:
        # 確保數據是數字數組
        data = np.array(data, dtype=np.float64)
    except (ValueError, TypeError) as e:
        return {"error": f"數據轉換錯誤：{str(e)}"}
    
    # 檢查數據長度
    if len(data) < 5:
        return {
            "error": "數據點太少，無法進行有效的頻譜分析",
            "min_required": 5,
            "current_length": len(data)
        }
    
    # 定義頻段
    theta_range = (4, 8)   # theta: 4-8 Hz
    alpha_range = (8, 13)  # alpha: 8-13 Hz
    
    # 使用 Welch 方法進行頻譜分析
    nperseg = min(len(data), fs//2)  # 使用 0.5 秒或更短的窗口
    if nperseg < 5:
        nperseg = len(data)
    
    try:
        freqs, psd = welch(data, fs=fs, nperseg=nperseg, noverlap=nperseg//2)
    except ValueError as e:
        return {"error": f"頻譜分析失敗：{str(e)}"}
    
    # 計算各頻段的功率
    def get_band_power(band_range):
        idx = np.logical_and(freqs >= band_range[0], freqs <= band_range[1])
        return np.mean(psd[idx]) if np.any(idx) else 0
    
    theta_power = get_band_power(theta_range)
    alpha_power = get_band_power(alpha_range)
    
    # 計算相對功率
    total_power = np.sum(psd)
    relative_theta = theta_power / total_power if total_power > 0 else 0
    relative_alpha = alpha_power / total_power if total_power > 0 else 0
    
    # 計算 alpha/theta 比率
    alpha_theta_ratio = alpha_power / theta_power if theta_power > 0 else 0
    
    return {
        "absolute_power": {
            "theta": float(theta_power),
            "alpha": float(alpha_power)
        },
        "relative_power": {
            "theta": float(relative_theta),
            "alpha": float(relative_alpha)
        },
        "alpha_theta_ratio": float(alpha_theta_ratio),
        "data_info": {
            "data_length": len(data),
            "frequency_resolution": float(fs/len(freqs)),
            "max_frequency": float(fs/2),
            "analysis_method": "welch"
        }
    } 