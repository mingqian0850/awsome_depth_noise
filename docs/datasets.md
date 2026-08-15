# 数据集与基准（Datasets & Benchmarks）

> 用于：噪声表征分析、去噪训练/评测、Real2Sim 注入效果的对比评估。标注链接均为官方页面。

## 真实 RGB-D / 深度数据集（含真实传感器噪声）

| 数据集 | 传感器 | 说明 | 链接 |
|---|---|---|---|
| NYU Depth V2 | Kinect v1（结构光） | 室内 RGB-D，单目深度估计/去噪常用 | [NYU](https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html) |
| TUM RGB-D SLAM Benchmark | Kinect v1 | SLAM 评估，含真实深度噪声的序列 | [TUM](https://cvg.cit.tum.de/data/datasets/rgbd-dataset) |
| Redwood | Kinect v1 | 室内重建数据集；其噪声统计被 Habitat-Sim 用作 `RedwoodDepthNoiseModel` | [Redwood](http://redwood-data.org/) |
| ScanNet | Structure Sensor | 大规模室内 RGB-D | [ScanNet](http://www.scan-net.org/) |
| SUN RGB-D | 多传感器（Kinect/RealSense/Asus） | 多传感器 RGB-D 基准 | [SUN RGB-D](https://rgbd.cs.princeton.edu/) |
| Matterport3D | Matterport（结构化扫描） | 室内 RGB-D 全景 | [Matterport3D](https://niessner.github.io/Matterport/) |
| ARKitScenes | iPad LiDAR / RGB-D | 室内场景，含深度噪声与相机位姿 | [ARKitScenes](https://github.com/apple/ARKitScenes) |
| KITTI Depth | Velodyne LiDAR | 自动驾驶深度/补全基准 | [KITTI](https://www.cvlibs.net/datasets/kitti/eval_depth.php) |
| nuScenes / SemanticKITTI | 多线 LiDAR | 点云感知与域适应常用 | [nuScenes](https://www.nuscenes.org/) · [SemanticKITTI](http://www.semantic-kitti.org/) |

## 合成深度 / 仿真数据集（适合验证"注入噪声"管线）

| 数据集 | 说明 | 链接 |
|---|---|---|
| Virtual KITTI | 合成自动驾驶深度/RGB | [Virtual KITTI](https://europe.naverlabs.com/research/computer-vision/proxy-virtual-worlds/) |
| TartanAir | 合成 SLAM 数据集（深度/光流/分割） | [TartanAir](http://theairlab.org/tartanair-dataset/) |
| IRS | 合成室内机器人场景（深度等模态） | [IRS](https://ylwhz.github.io/irs/) |
| DIODE | 室内外稠密深度（激光扫描真值） | [DIODE](https://diode-dataset.github.io/) |

## 噪声评测 / 鲁棒性基准

| 基准 | 说明 | 链接 |
|---|---|---|
| RoboDepth | 深度估计在 15 类退化（含真实感深度噪声）下的鲁棒性评估 | [arXiv:2310.15171](https://arxiv.org/abs/2310.15171) |
| SIDD（RGB 参考） | 真实手机相机噪声（去噪训练/评测），可作为"真实噪声采集协议"参考 | [SIDD](https://abdokamel.github.io/sidd/) |

## 建议的自建数据协议（研究用）

1. **静态场景多次采样**：固定相机与场景，连续拍摄 N≥100 帧 → 均值/中值作为 pseudo-GT，残差即噪声样本（可直接用于 Noise2Noise 两帧训练）。
2. **距离标定板**：平面板在不同距离（0.5–5 m）采集 → 拟合 σ(d) 曲线与系统偏差。
3. **材质/反射率扫描**：黑白灰阶靶、不同粗糙度材质 → 估计缺失率 p(d, reflectivity) 与飞点概率。
4. **与高精度真值对比**：结构光投影仪 + 标定、或激光扫描仪，获得逐像素真值用于监督评估。
