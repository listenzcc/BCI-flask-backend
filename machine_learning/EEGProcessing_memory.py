import numpy as np
import scipy.signal as signal
import nolds
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import random
import threading 

class EEGProcessor:
    def __init__(self, fs=250):
        """
        初始化 EEG 处理类，包括参数设定和模型训练
        """
        # 采样率和数据窗口
        self.fs = fs
        self.segment_length = 5 * fs  # 5 秒数据窗口
        self.step_size = 5 * fs        # 滑动窗口步长

        # 频带设置
        self.theta_band = (4, 8)
        self.alpha_band = (8, 13)
        self.beta_band = (13, 30)


        # 归一化参数
        #self.best_feature_idx = None  # 记录最优特征索引
        self.mean_fp1 = None
        self.max_fp1 = None
        self.min_fp1 = None
        self.mean_fp2 = None
        self.max_fp2 = None
        self.min_fp2 = None

        #新增数据缓存相关属性
        # self.scores_cache = [] #数据缓存队列
        # self.window_size = 2 #滑动窗口
        # self._rlock = threading.RLock()

    def preprocess(self, data):
        """
        预处理:50Hz Notch 滤波 + 1-30Hz 带通滤波
        """
        # 50Hz Notch 滤波
        # notch_freq = 50  # 工频干扰
        # b_notch, a_notch = signal.iirnotch(notch_freq, 30, self.fs)
        # data = signal.filtfilt(b_notch, a_notch, data)

        # 1-30Hz 带通滤波
        bandpass = (1, 30)
        b_band, a_band = signal.butter(
            3, [bandpass[0] / (0.5 * self.fs), bandpass[1] / (0.5 * self.fs)], btype='bandpass')
        data = signal.filtfilt(b_band, a_band, data)
        print("preprocessed data shape is", data.shape)

        return data

    def bandpower(self, data, band):
        """
        计算指定频段的功率
        """
        low, high = band
        b, a = signal.butter(
            3, [low / (0.5 * self.fs), high / (0.5 * self.fs)], btype='bandpass')
        # print(data)
        filtered = signal.filtfilt(b, a, data)
        # print(filtered)
        freqs, psd = signal.welch(filtered, self.fs)
        band_psd = psd[(freqs >= low) & (freqs <= high)]
        print(band_psd, freqs[(freqs >= low) & (freqs <= high)])
        return np.trapz(band_psd, freqs[(freqs >= low) & (freqs <= high)])


    def extract_features(self, segment):
        """
        提取 EEG 片段的特征:alpha/theta ratio
        """
        # 预处理 EEG 片段
        #segment = np.ravel(segment)
        print("data shape:", segment.shape)
        segment = self.preprocess(segment)

        theta_power = self.bandpower(segment, self.theta_band)
        alpha_power = self.bandpower(segment, self.alpha_band)
        # alpha_power = self.bandpower(segment, self.alpha_band)
        # print(theta_power.shape, theta_power)
        # print(alpha_power.shape, alpha_power)
        alpha_theta_ratio = alpha_power / theta_power if theta_power != 0 else 0

        return alpha_theta_ratio


    def train(self, non_memory_data, memory_data):
        """
        计算 FP1 和 FP2 通道的 alpha/theta ratio，并存储均值、最小值、最大值，以及两者的平均值
        """
        # 提取 FP1 (ch=1) 和 FP2 (ch=2) 通道的 theta/beta ratio
        alpha_theta_fp1_memory = np.array([self.extract_features(memory_data[i, 1, :]) for i in range(len(memory_data))])
        alpha_theta_fp2_memory = np.array([self.extract_features(memory_data[i, 2, :]) for i in range(len(memory_data))])

        alpha_theta_fp1_nomemory = np.array([self.extract_features(non_memory_data[i, 1, :]) for i in range(len(non_memory_data))])
        alpha_theta_fp2_nomemory = np.array([self.extract_features(non_memory_data[i, 2, :]) for i in range(len(non_memory_data))])

        # 合并两个类别的数据
        alpha_theta_fp1 = np.hstack((alpha_theta_fp1_memory, alpha_theta_fp1_nomemory))  # FP1 通道
        alpha_theta_fp2 = np.hstack((alpha_theta_fp2_memory, alpha_theta_fp2_nomemory))  # FP2 通道

        # 计算均值、最小值、最大值
        self.mean_fp1 = np.mean(alpha_theta_fp1)
        self.min_fp1 = np.min(alpha_theta_fp1)
        self.max_fp1 = np.max(alpha_theta_fp1)

        self.mean_fp2 = np.mean(alpha_theta_fp2)
        self.min_fp2 = np.min(alpha_theta_fp2)
        self.max_fp2 = np.max(alpha_theta_fp2)

   

    def normalize_and_map(self, value, mean_val, min_val, max_val):
        """
        对单个通道的值进行归一化，并映射到 Sigmoid 记忆力得分
        """
        # 先减去训练时的均值
        value_centered = value - mean_val  # 先去均值
        # 避免除零错误
        if max_val == min_val:
            print(f"Warning: min and max are equal for value {value}. Using default score.")
            norm_value = random.uniform(-2, 2)
        else:
            norm_value = (value_centered - min_val) / (max_val - min_val) * (2 - (-2)) + (-2)

        # 取反，使数值越大记忆力越高
        norm_value = -1 * norm_value

        # 通过 Sigmoid 映射到 0-1 之间
        sigmoid_value = 1 / (1 + np.exp(-norm_value))

        return sigmoid_value  # 返回 0-1 之间的记忆力得分

    def process_online(self, eeg_segment):
        """
        实时处理 EEG 片段，分别计算 FP1 和 FP2 的记忆力得分，然后取平均
        """
        # 计算 FP1 和 FP2 的 theta/beta ratio
        alpha_theta_fp1 = self.extract_features(eeg_segment[1, :])  
        alpha_theta_fp2 = self.extract_features(eeg_segment[2, :])  

        # 分别计算 FP1 和 FP2 的记忆力得分
        memory_score_fp1 = self.normalize_and_map(alpha_theta_fp1, self.mean_fp1, self.min_fp1, self.max_fp1)
        memory_score_fp2 = self.normalize_and_map(alpha_theta_fp2, self.mean_fp2, self.min_fp2, self.max_fp2)

        # 计算 FP1 和 FP2 的平均记忆力得分
        memory_score_avg = (memory_score_fp1 + memory_score_fp2) / 2

        # 转换为 0-100 之间的整数
        memory_score = int(100 * memory_score_avg)

        print(f"FP1 alpha/theta: {alpha_theta_fp1:.2f}, FP2 alpha/theta: {alpha_theta_fp2:.2f}")
        print(f"FP1 归一化得分: {memory_score_fp1:.2f}, FP2 归一化得分: {memory_score_fp2:.2f}")
        print(f"FP1+FP2 平均记忆力得分: {memory_score}")

        return memory_score


    



