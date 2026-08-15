# 完整论文清单（Papers）

> 相关性标注：⭐ = 与"学习真实噪声 → 去噪/Real2Sim"高度相关；标注检索日期见文末。所有链接均指向 arXiv / 出版方 / Semantic Scholar 官方页面。

## A. 噪声表征与解析模型

| 论文 | 会议/期刊 | 链接 | 一句话贡献 | 相关性 |
|---|---|---|---|---|
| Accuracy and Resolution of Kinect Depth Data for Indoor Mapping Applications（Khoshelham & Elberink） | Sensors 12(2):1437, 2012 | [MDPI](https://www.mdpi.com/1424-8220/12/2/1437) · DOI 10.3390/s120201437 | 经典 σ(d) 随机误差多项式模型 | ⭐⭐ |
| Modeling Kinect Sensor Noise for Improved 3D Reconstruction and Tracking（Nguyen et al.） | 3DIMPVT 2012 | DOI 10.1109/3DIMPVT.2012.84 | 随机误差 + 空间误差分解建模 | ⭐⭐ |
| Characterizations of Noise in Kinect Depth Images: A Review（Mallick et al.） | IEEE Sensors Journal, 2014 | [IEEE](https://ieeexplore.ieee.org/abstract/document/6756961) | 深度噪声类型综述（散粒/边缘/光照/运动） | ⭐ |
| Statistical Models of Horizontal and Vertical Stochastic Noise for the Microsoft Kinect Sensor（Choo & DeVore） | IECON 2014 | DOI 10.1109/IECON.2014.7048876 | 行列方向随机噪声统计模型 | ⭐ |
| Simulating Kinect Infrared and Depth Images（Landau, Choo, DeVore） | IEEE T-CYB 46(12):3018, 2016 | DOI 10.1109/TCYB.2015.2494877 | 从 IR 散斑物理仿真 Kinect 深度 | ⭐⭐ |
| Metrological and Critical Characterization of the Intel D415 Stereo Depth Camera（Carfagni et al.） | Sensors 19(3), 2019 | [MDPI](https://www.mdpi.com/1424-8220/19/3/489) · PMID 30691011 | 主动立体相机噪声/精度表征 | ⭐⭐ |
| Noise Analysis and Modeling of the PMD Flexx2 Depth Camera for Robotic Applications（Plozza et al.） | COINS 2024 | [arXiv:2412.15040](https://arxiv.org/abs/2412.15040) | 现代 iToF 距离/强度相关噪声建模 | ⭐⭐⭐ |
| Generation of Synthetic Kinect Depth Images Based on Empirical Noise Model（Iversen & Kraft） | Electronics Letters, 2017 | DOI 10.1049/el.2017.0392 | 经验噪声模型 → 合成深度图 | ⭐⭐⭐ |

## B. 物理仿真（ToF / 结构光 / 主动立体 / LiDAR）

| 论文 | 会议/期刊 | 链接 | 一句话贡献 | 相关性 |
|---|---|---|---|---|
| A Simulation Framework for Time-of-Flight Sensors（Keller, Orthmann, Kolb） | SimVis 2007 | [Semantic Scholar](https://www.semanticscholar.org/paper/A-Simulation-Framework-for-Time-Of-Flight-Sensors-Keller-Orthmann/edf8ee02e4bb3412bb11511d942330a24dde3795) | 经典 ToF 仿真框架 | ⭐⭐ |
| Quantified, Interactive Simulation of AMCW ToF Camera Including Multipath Effects | Sensors 18(1):13, 2018 | [MDPI](https://www.mdpi.com/1424-8220/18/1/13) · DOI 10.3390/s18010013 | 含多径效应的 AMCW ToF 仿真 | ⭐⭐ |
| Close the Optical Sensing Domain Gap by Physics-Grounded Active Stereo Sensor Simulation（Zhang, Xu et al.） | IEEE T-RO 39(3):2429, 2023 | [arXiv:2201.11924](https://arxiv.org/abs/2201.11924) · DOI 10.1109/TRO.2023.3235591 | RealSense 主动立体物理仿真，显著缩小深度 sim2real 差距 | ⭐⭐⭐ |
| **Close the Sim2real Gap via Physically-based Structured Light Synthetic Data Simulation**（Bai, Zhang, Chen, Wan, Zhang） | **ICRA 2024** | [arXiv:2407.12449](https://arxiv.org/abs/2407.12449) · DOI 10.48550/arXiv.2407.12449 · [IEEE](https://ieeexplore.ieee.org/document/10611401) · 📖 [精读笔记](../docs/paper_notes/close-sim2real-gap-structured-light.md) | 物理仿真格雷码结构光全链路，噪声由解码错误自然涌现，直接缩小 sim2real 差距 | ⭐⭐⭐ |
| **VIRTUS-FPP: Virtual Sensor Modeling for Fringe Projection Profilometry in NVIDIA Isaac Sim** | arXiv:2509.22685, 2025 | [arXiv](https://arxiv.org/abs/2509.22685) · [IEEE](https://ieeexplore.ieee.org/abstract/document/11554253) | 工业条纹投影（FPP）结构光在 Isaac Sim 的虚拟传感器建模 | ⭐⭐⭐ |
| **Comprehensive Machine Learning Benchmarking for Fringe Projection Profilometry with Photorealistic Synthetic Data** | SPIE 2025 | DOI 10.1117/12.3082257 · [arXiv:2601.08900](https://arxiv.org/abs/2601.08900) | 照片级真实合成数据的 FPP 机器学习基准 | ⭐⭐ |
| **Simulation of Structured Light 3D Scanning using Blender**（Puljcan & Zoraja） | 会议论文（萨格勒布大学 FER） | [Semantic Scholar](https://www.semanticscholar.org/paper/Simulation-of-Structured-Light-3D-Scanning-using-Puljcan-Zoraja/486ef08f4040486fce98f1eb00b4378ab46ef603) · [PDF](https://www.bib.irb.hr:8443/1242928/download/1242928.ID29_Simulation_of_Structured_Light_3D_Scanning_using_Blender_submission.pdf) | Blender 仿真结构光 3D 扫描 | ⭐⭐ |
| **Robust Single-shot Structured Light 3D Imaging via Neural Feature Decoding** | SIGGRAPH Asia 2025 | DOI 10.1145/3757377.3763924 | 数据驱动结构光解码（学习式结构光成像） | ⭐ |
| Physically-Based Simulation of Automotive LiDAR | arXiv:2512.05932, 2025 | [arXiv](https://arxiv.org/abs/2512.05932) | 含 blooming/回波展宽/多回波的 LiDAR 物理仿真 | ⭐ |
| DeepToF: Off-the-Shelf Real-Time Correction of Multipath Interference in Time-of-Flight Imaging | SIGGRAPH Asia 2018 | [arXiv:1805.09305](https://arxiv.org/abs/1805.09305) | 物理仿真造数据 → 真实 ToF 多径校正（sim2real 范式） | ⭐⭐⭐ |
| Dense Metric Depth Completion from Sparse Direct Time-of-Flight Sensors | CVPR 2026 | [arXiv:2608.04737](https://arxiv.org/abs/2608.04737) | 稀疏 dToF → 稠密深度 | ⭐ |

## C. 数据驱动 Real2Sim（学习真实噪声并注入仿真）

| 论文 | 会议/期刊 | 链接 | 一句话贡献 | 相关性 |
|---|---|---|---|---|
| LiDARsim: Realistic LiDAR Simulation by Leveraging the Real World（Manivasagam et al.） | CVPR 2020 | [arXiv:2006.09348](https://arxiv.org/abs/2006.09348) | 真实扫描重合成新位姿点云，噪声天然真实 | ⭐⭐⭐ |
| Realistic Noise Synthesis with Diffusion Models (RNSD)（Wu, Han et al.） | AAAI 2025 | [arXiv:2305.14022](https://arxiv.org/abs/2305.14022) · [Code](https://github.com/wuqi-coder/rnsd) | 扩散模型条件合成真实相机噪声（可迁移至深度域） | ⭐⭐⭐ |
| Project to Adapt: Domain Adaptation for Depth Completion from Noisy and Sparse Sensor Data（Lopez-Rodriguez et al.） | ACCV 2020 | [CVF](https://openaccess.thecvf.com/content/ACCV2020/html/Lopez-Rodriguez_Project_to_Adapt_Domain_Adaptation_for_Depth_Completion_from_Noisy_ACCV_2020_paper.html) | 从真实带噪稀疏数据学域迁移 | ⭐⭐⭐ |
| Adversarially Masking Synthetic to Mimic Real: Adaptive Noise Injection for Point Cloud Segmentation Adaptation | CVPR 2023 | [Paper](https://mlanthology.org/cvpr/2023/li2023cvpr-adversarially/) | 自适应对抗式噪声注入弥合点云 sim2real 差距 | ⭐⭐⭐ |
| S2R-DepthNet: Learning a Generalizable Depth-Specific Structural Representation | CVPR 2021 | [arXiv:2104.00877](https://arxiv.org/abs/2104.00877) | 合成深度预训练 + 真实域适配 | ⭐⭐ |
| **A Supervised Approach to Predicting Noise in Depth Images**（Sweeney et al.） | ICRA 2019 | DOI 10.1109/ICRA.2019.8793820 | 监督学习预测深度图像逐像素噪声（噪声模型/加权先验） | ⭐⭐⭐ |
| **Quasi-Balanced Self-Training on Noise-Aware Synthesis of Object Point Clouds for Closing Domain Gap** | arXiv:2203.03833, 2022 | [arXiv](https://arxiv.org/abs/2203.03833) | 主动立体（相机+投影仪）噪声感知点云合成 + 自训练 | ⭐⭐⭐ |
| **Digital-Twin-Driven Unambiguous Structured Light 3D Imaging with Physics-Aware Learning** | npj Nanophotonics, 2025 | [Paper](https://www.nature.com/articles/s44310-025-00096-z) | 结构光数字孪生 + 物理感知学习 | ⭐⭐ |
| Noise Flow: Noise Modeling with Normalizing Flows（Abdelhamed et al.） | ICCV 2019 | [Semantic Scholar](https://www.semanticscholar.org/paper/Noise-Flow-Noise-Modeling-with-Normalizing-Flows-Abdelhamed-Brubaker/aa495dd8a4eaff2fd5a67a1188c960ff9a693b3e) | 流模型显式学习真实相机噪声分布（RGB） | ⭐⭐⭐ |
| A High-Quality Denoising Dataset for Smartphone Cameras (SIDD)（Abdelhamed et al.） | CVPRW 2018 | [SIDD](https://abdokamel.github.io/sidd/) | 真实噪声采集协议与数据集 | ⭐⭐ |
| Unprocessing Images for Learned Raw Denoising（Brooks et al.） | CVPR 2019 | [arXiv:1811.11127](https://arxiv.org/abs/1811.11127) | 合成→真实 raw 噪声的物理逆处理 | ⭐⭐ |
| A Physics-Based Noise Formation Model for Extreme Low-Light RAW Denoising（Wei et al.） | CVPR 2020 | [arXiv:2003.12751](https://arxiv.org/abs/2003.12751) | 可学习参数的物理噪声形成模型（散粒/读出/暗电流） | ⭐⭐ |

## D. 噪声压制（深度图 / ToF / 点云去噪）

### D1. 深度图 / ToF

| 论文 | 会议/期刊 | 链接 | 一句话贡献 | 相关性 |
|---|---|---|---|---|
| RADU: Ray-Aligned Depth Update Convolutions for ToF Data Denoising（Schelling et al.） | CVPR 2022 | [PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Schelling_RADU_Ray-Aligned_Depth_Update_Convolutions_for_ToF_Data_Denoising_CVPR_2022_paper.pdf) | ToF 专用去噪（沿光线对齐卷积） | ⭐⭐ |
| SelfReDepth: Self-Supervised Real-Time Depth Restoration for Consumer-Grade Sensors（Moreira et al.） | JRTIP 2024 | [arXiv:2406.03388](https://arxiv.org/abs/2406.03388) · DOI 10.1007/s11554-024-01491-z | 自监督实时深度修复，无需干净真值 | ⭐⭐⭐ |
| Self-Supervised Learning for RGB-Guided Depth Enhancement by Exploiting the Dependency between RGB and Depth | IEEE TIP 2022 | DOI 10.1109/TIP.2022.3226419 | 自监督 RGB 引导深度增强 | ⭐⭐ |
| Self-Supervised End-to-End ToF Imaging Based on RGB-D Cross-Modal Dependency | 预印本 | [Semantic Scholar](https://www.semanticscholar.org/paper/Self-supervised-End-to-end-ToF-Imaging-Based-on-Wang-Wang/0dceed893a8eb320a95155d7a370f2d707386787) | 跨模态依赖的自监督 ToF 成像 | ⭐⭐ |
| iToF2dToF: A Robust and Flexible Representation for Data-Driven Time-of-Flight Imaging | CVPR 2021 | [arXiv:2103.07087](https://arxiv.org/abs/2103.07087) | 数据驱动 iToF 重建的鲁棒表示 | ⭐⭐ |
| Learnable Fractional Reaction-Diffusion Dynamics for Under-Display ToF Imaging and Beyond | ICCV 2025 | [Paper](https://mlanthology.org/iccv/2025/qiao2025iccv-learnable/) | 屏下 ToF 成像学习 | ⭐ |
| Noise2Noise: Learning Image Restoration without Clean Targets（Lehtinen et al.） | ICML 2018 | [arXiv:1803.04189](https://arxiv.org/abs/1803.04189) | 自监督去噪基石（两帧独立噪声） | ⭐⭐⭐ |

### D2. 点云

| 论文 | 会议/期刊 | 链接 | 一句话贡献 | 相关性 |
|---|---|---|---|---|
| Total Denoising: Unsupervised Learning of 3D Point Cloud Cleaning（Hermosilla et al.） | ICCV 2019 | [arXiv:1904.07615](https://arxiv.org/abs/1904.07615) · [Code](https://github.com/phermosilla/TotalDenoising) | 无监督点云去噪（无需干净真值） | ⭐⭐⭐ |
| PointCleanNet: Learning to Denoise and Remove Outliers from Dense Point Clouds（Rakotosaona et al.） | ICCV 2019 | [arXiv:1906.10832](https://arxiv.org/abs/1906.10832) | 点云去噪 + 离群点移除（监督） | ⭐⭐ |
| Pointfilter: Point Cloud Filtering via Encoder-Decoder Modeling（Zhang et al.） | IEEE TVCG 2020 | [arXiv:1910.08274](https://arxiv.org/abs/1910.08274) | 编码器-解码器点云滤波 | ⭐⭐ |
| Score-Based Point Cloud Denoising（Luo & Hu） | ICCV 2021 | [CVF](https://openaccess.thecvf.com/content/ICCV2021/html/Luo_Score-Based_Point_Cloud_Denoising_ICCV_2021_paper.html) | 分数匹配生成模型点云去噪 | ⭐⭐ |
| Noise2Score3D: Tweedie's Approach for Unsupervised Point Cloud Denoising | ICCV 2025 | [Code](https://github.com/Bobby645/Noise2Score3D) | 无监督点云去噪（Tweedie + 分数估计） | ⭐⭐⭐ |

## E. 域随机化与 Sim2Real 方法学

| 论文 | 会议/期刊 | 链接 | 一句话贡献 |
|---|---|---|---|
| Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World（Tobin et al.） | IROS 2017 | [arXiv:1703.06907](https://arxiv.org/abs/1703.06907) | 域随机化奠基工作 |
| Automatic Domain Randomization and Deep Reinforcement Learning: A Scalable Approximation for the Real World（OpenAI） | arXiv 2019 | [arXiv:1910.07113](https://arxiv.org/abs/1910.07113) | 自适应扩增随机化范围 |

## F. 鲁棒性评测与基准

| 论文 | 会议/期刊 | 链接 | 一句话贡献 |
|---|---|---|---|
| RoboDepth: Robust Out-of-Distribution Depth Estimation under Corruptions | NeurIPS 2023 D&B | [arXiv:2310.15171](https://arxiv.org/abs/2310.15171) | 深度估计鲁棒性基准（含真实感深度退化） |

## G. 综述

| 论文 | 链接 |
|---|---|
| A Survey of Deep Learning-based Point Cloud Denoising（2025） | [arXiv:2508.17011](https://arxiv.org/abs/2508.17011) |
| Deep Learning for 3D Point Cloud Enhancement: A Survey（2024） | [arXiv:2411.00857](https://arxiv.org/abs/2411.00857) |
| Characterizations of Noise in Kinect Depth Images: A Review（2014） | [IEEE](https://ieeexplore.ieee.org/abstract/document/6756961) |

---

**整理日期**：2026（首批条目）；条目元数据（venue/arXiv/DOI）均已逐一核对链接，如发现变更请提 Issue 或 PR 修正。
