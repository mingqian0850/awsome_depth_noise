# awsome_depth_noise 🎯

> **深度相机噪声研究清单** — 噪声表征 · 噪声压制（Denoising）· 噪声 Real2Sim（为仿真传感器注入符合真实物理的噪声）

An awesome list of research on **depth camera noise**: characterization & modeling, denoising, and **real2sim noise learning** — learning the noise pattern of a real depth sensor (ToF / structured-light / active stereo / LiDAR) and injecting physically-plausible noise into simulation.

**研究核心问题（Research Questions）**

1. **噪声压制**：能否用模型学习真实深度相机输出的噪声点云，从而对真实数据去噪（Denoising）？
2. **噪声 Real2Sim**：能否学出相机的噪声模式，给仿真传感器（Gazebo / Isaac Sim / Habitat / AirSim）添加符合真实物理的噪声，缩小 sim2real 差距？

**结论速览（TL;DR）**：✅ 方向可行且已有大量相关工作。真实深度噪声 ≈ **随机误差（距离相关）+ 系统偏差 + 空间相关误差（边缘/材质/入射角）+ 缺失/空洞 +（ToF）多径干扰 +（时间）抖动**。研究路线主要分三类：**解析/统计噪声模型**（可当插件直接注入仿真）、**物理仿真**（第一性原理、保真度高但标定难）、**数据驱动学习噪声**（GAN/扩散/流模型、自监督去噪、域适配、真实数据重合成——最贴合你的设想）。详见 [研究综述](docs/research_notes.md) 与 [研究路线图](docs/roadmap.md)。

---

## 📑 目录（Contents）

- [论文分类清单（Awesome Papers）](#-论文分类清单)
  - [📊 A. 噪声表征与解析模型](#a-噪声表征与解析模型)
  - [🔬 B. 物理仿真（ToF / 主动立体 / LiDAR）](#b-物理仿真tof--主动立体--lidar)
  - [🤖 C. 数据驱动 Real2Sim（学习真实噪声并注入仿真）](#c-数据驱动-real2sim学习真实噪声并注入仿真)
  - [🧹 D. 噪声压制（深度图 / ToF / 点云去噪）](#d-噪声压制深度图--tof--点云去噪)
  - [🎲 E. 域随机化与 Sim2Real 方法学](#e-域随机化与-sim2real-方法学)
  - [📈 F. 鲁棒性评测与基准](#f-鲁棒性评测与基准)
  - [📚 G. 综述](#g-综述)
- [🗂️ 数据集与基准](docs/datasets.md)
- [🛠️ 仿真器与噪声插件](docs/simulators_tools.md)
- [📖 研究综述与可行性分析](docs/research_notes.md)
- [🧭 研究分类图谱（Taxonomy）](docs/taxonomy.md)
- [🗺️ 建议研究路线图](docs/roadmap.md)
- [📄 完整论文清单（含注释表格）](docs/papers.md)

---

## 📊 A. 噪声表征与解析模型

*对真实深度传感器噪声进行测量、建模（距离相关方差、空间相关性、系统偏差），是 Real2Sim 噪声注入的"原材料"。*

- **Accuracy and Resolution of Kinect Depth Data for Indoor Mapping Applications** — K. Khoshelham, S. O. Elberink · *Sensors* 12(2):1437, 2012 · [MDPI](https://www.mdpi.com/1424-8220/12/2/1437) · DOI 10.3390/s120201437
  - ⭐ 经典中的经典：随机误差 σ(d) 随距离非线性增长（多项式拟合），是所有后续噪声模型的基准。
- **Modeling Kinect Sensor Noise for Improved 3D Reconstruction and Tracking** — C. V. Nguyen, S. Izadi, D. Lovell · *3DIMPVT 2012* · DOI 10.1109/3DIMPVT.2012.84
  - 把噪声分解为**随机误差（σ(d)）+ 空间误差**两部分分别建模，给出低光照下噪声特征。
- **Characterizations of Noise in Kinect Depth Images: A Review** — T. Mallick, P. P. Das, A. K. Majumdar · *IEEE Sensors Journal*, 2014 · [IEEE](https://ieeexplore.ieee.org/abstract/document/6756961)
  - 噪声类型全面综述：散粒噪声、边缘误差、光照相关误差、运动误差等。
- **Statistical Models of Horizontal and Vertical Stochastic Noise for the Microsoft Kinect Sensor** — B. Y. Choo, M. D. DeVore · *IECON 2014* · DOI 10.1109/IECON.2014.7048876
  - 沿深度图像行/列的随机噪声统计模型。
- **Simulating Kinect Infrared and Depth Images** — M. J. Landau, B. Y. Choo, M. D. DeVore · *IEEE Trans. Cybernetics* 46(12):3018, 2016 · DOI 10.1109/TCYB.2015.2494877
  - ⭐ 从 IR 图像出发物理仿真 Kinect 深度图像（含散斑、噪声），是早期"仿真→真实"噪声管线。
- **Metrological and Critical Characterization of the Intel D415 Stereo Depth Camera** — M. Carfagni et al. · *Sensors* 19(3), 2019 · [MDPI](https://www.mdpi.com/1424-8220/19/3/489) · PMID 30691011
  - 主动立体（RealSense D415）噪声/精度系统表征。
- **Noise Analysis and Modeling of the PMD Flexx2 Depth Camera for Robotic Applications** — D. Plozza et al. · *COINS 2024* · [arXiv:2412.15040](https://arxiv.org/abs/2412.15040)
  - ⭐ 现代 iToF 相机（PMD Flexx2）的噪声分析：距离相关 + 强度相关，含完整建模流程，与"为仿真器建模"直接衔接。
- **Generation of Synthetic Kinect Depth Images Based on Empirical Noise Model** — T. M. Iversen, D. Kraft · *Electronics Letters*, 2017 · DOI 10.1049/el.2017.0392
  - ⭐ 经验噪声模型 → 合成深度图（早期 real2sim 噪声注入实证）。

## 🔬 B. 物理仿真（ToF / 主动立体 / LiDAR）

*第一性原理仿真传感器物理（光子飞行、多径、投影图案），训练数据保真度高，但要精确对齐真实器件需要标定。*

- **A Simulation Framework for Time-of-Flight Sensors** — M. Keller, J. Orthmann, A. Kolb · *SimVis 2007* · [Semantic Scholar](https://www.semanticscholar.org/paper/A-Simulation-Framework-for-Time-Of-Flight-Sensors-Keller-Orthmann/edf8ee02e4bb3412bb11511d942330a24dde3795)
  - 经典 ToF 传感器仿真框架。
- **Quantified, Interactive Simulation of AMCW ToF Camera Including Multipath Effects** — *Sensors* 18(1):13, 2018 · [MDPI](https://www.mdpi.com/1424-8220/18/1/13) · DOI 10.3390/s18010013
  - 量化、交互式 AMCW ToF 仿真，**包含多径效应**。
- **Close the Optical Sensing Domain Gap by Physics-Grounded Active Stereo Sensor Simulation** — J. Zhang, J. Xu et al. · *IEEE Trans. Robotics* 39(3):2429, 2023 · [arXiv:2201.11924](https://arxiv.org/abs/2201.11924) · DOI 10.1109/TRO.2023.3235591
  - ⭐⭐ 物理仿真 **RealSense 主动立体**（投影图案 + 噪声 + 去噪算法链），显著缩小深度传感器 sim2real 域差距 —— 与你的目标最接近的工作之一。
- **Physically-Based Simulation of Automotive LiDAR** — *arXiv:2512.05932*, 2025 · [arXiv](https://arxiv.org/abs/2512.05932)
  - 含 blooming、回波展宽、多回波等物理效应的车规 LiDAR 仿真。
- **DeepToF: Off-the-Shelf Real-Time Correction of Multipath Interference in Time-of-Flight Imaging** — *SIGGRAPH Asia 2018* · [arXiv:1805.09305](https://arxiv.org/abs/1805.09305)
  - ⭐ 用**物理仿真器生成训练数据** → 真实 ToF 多径校正：数据驱动 + 物理仿真的经典组合范式。
- **Dense Metric Depth Completion from Sparse Direct Time-of-Flight Sensors** — *CVPR 2026* · [arXiv:2608.04737](https://arxiv.org/abs/2608.04737)
  - 稀疏 dToF 传感器数据 → 稠密深度（面向手机/机器人 dToF 传感器）。

## 🤖 C. 数据驱动 Real2Sim（学习真实噪声并注入仿真）

*你的核心方向：让模型从真实深度输出中**学习噪声模式**，再把它**注入仿真**。*

- **LiDARsim: Realistic LiDAR Simulation by Leveraging the Real World** — S. Manivasagam et al. · *CVPR 2020* · [arXiv:2006.09348](https://arxiv.org/abs/2006.09348)
  - ⭐⭐ 用**真实 LiDAR 扫描重建场景**并重合成任意新位姿下的点云，天然保留真实噪声/强度/缺失模式 —— "把真实噪声搬进仿真"的最典型代表。
- **Realistic Noise Synthesis with Diffusion Models (RNSD)** — Q. Wu, M. Han et al. · *AAAI 2025* · [arXiv:2305.14022](https://arxiv.org/abs/2305.14022) · [Code](https://github.com/wuqi-coder/rnsd)
  - ⭐⭐ 扩散模型学习真实相机噪声分布并**按条件合成噪声**（RGB 域），方法论可直接迁移到深度/点云噪声。
- **Project to Adapt: Domain Adaptation for Depth Completion from Noisy and Sparse Sensor Data** — A. Lopez-Rodriguez et al. · *ACCV 2020* · [Paper](https://openaccess.thecvf.com/content/ACCV2020/html/Lopez-Rodriguez_Project_to_Adapt_Domain_Adaptation_for_Depth_Completion_from_Noisy_ACCV_2020_paper.html)
  - ⭐ 从**真实带噪稀疏传感器数据**出发做域适配（合成 → 真实），明确把"噪声"当作可迁移的域特征。
- **Adversarially Masking Synthetic to Mimic Real: Adaptive Noise Injection for Point Cloud Segmentation Adaptation** — *CVPR 2023* · [Paper](https://mlanthology.org/cvpr/2023/li2023cvpr-adversarially/)
  - ⭐ 自适应地向合成点云注入噪声以逼近真实分布（对抗式噪声注入）。
- **S2R-DepthNet: Learning a Generalizable Depth-Specific Structural Representation** — *CVPR 2021* · [arXiv:2104.00877](https://arxiv.org/abs/2104.00877)
  - 合成深度预训练 + 真实域适配，深度特有的结构表示学习。
- **Noise Flow: Noise Modeling with Normalizing Flows** — A. Abdelhamed et al. · *ICCV 2019*
  - ⭐ 用归一化流显式学习真实相机噪声分布（RGB），生成式噪声建模的代表方法。
- **A High-Quality Denoising Dataset for Smartphone Cameras (SIDD)** — A. Abdelhamed et al. · *CVPRW 2018*
  - 真实噪声数据采集协议参考（同一场景多次拍摄，真实传感器噪声）。
- **Unprocessing Images for Learned Raw Denoising** — T. Brooks et al. · *CVPR 2019*
  - 合成数据 + 物理逆处理，让合成噪声更接近真实 raw 噪声。
- **A Physics-Based Noise Formation Model for Extreme Low-Light RAW Denoising** — K. Wei et al. · *CVPR 2020*
  - 物理噪声形成模型（散粒噪声 + 读出噪声 + 暗电流）的可学习参数化。

## 🧹 D. 噪声压制（深度图 / ToF / 点云去噪）

*学习噪声的另一面：用模型把噪声从真实深度输出中剥离。*

**深度图 / ToF**

- **RADU: Ray-Aligned Depth Update Convolutions for ToF Data Denoising** — M. Schelling, P. Hermosilla, T. Ropinski · *CVPR 2022* · [PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Schelling_RADU_Ray-Aligned_Depth_Update_Convolutions_for_ToF_Data_Denoising_CVPR_2022_paper.pdf)
  - ToF 专用去噪网络（沿光线方向对齐的卷积）。
- **SelfReDepth: Self-Supervised Real-Time Depth Restoration for Consumer-Grade Sensors** — C. Moreira et al. · *JRTIP 2024* · [arXiv:2406.03388](https://arxiv.org/abs/2406.03388) · DOI 10.1007/s11554-024-01491-z
  - ⭐ 自监督深度修复（无需干净真值），面向消费级传感器，实时。
- **Self-Supervised Learning for RGB-Guided Depth Enhancement by Exploiting the Dependency between RGB and Depth** — *IEEE TIP*, 2022 · DOI 10.1109/TIP.2022.3226419
  - 自监督 RGB 引导深度增强。
- **Self-Supervised End-to-End ToF Imaging Based on RGB-D Cross-Modal Dependency** — [Semantic Scholar](https://www.semanticscholar.org/paper/Self-supervised-End-to-end-ToF-Imaging-Based-on-Wang-Wang/0dceed893a8eb320a95155d7a370f2d707386787)
  - 跨模态（RGB-D）依赖的自监督 ToF 成像。
- **iToF2dToF: A Robust and Flexible Representation for Data-Driven Time-of-Flight Imaging** — *CVPR 2021* · [arXiv:2103.07087](https://arxiv.org/abs/2103.07087)
  - 数据驱动 iToF 重建的鲁棒表示。
- **Learnable Fractional Reaction-Diffusion Dynamics for Under-Display ToF Imaging and Beyond** — *ICCV 2025*
  - 最新 ToF 成像学习（屏下 ToF）。
- **Noise2Noise: Learning Image Restoration without Clean Targets** — J. Lehtinen et al. · *ICML 2018*
  - ⭐ 自监督去噪的基石：成对独立噪声样本即可训练，深度噪声天然满足该假设（两次拍摄）。

**点云**

- **Total Denoising: Unsupervised Learning of 3D Point Cloud Cleaning** — P. Hermosilla et al. · *ICCV 2019* · [arXiv:1904.07615](https://arxiv.org/abs/1904.07615) · [Code](https://github.com/phermosilla/TotalDenoising)
  - ⭐ 无监督点云去噪（不需要干净真值）。
- **PointCleanNet: Learning to Denoise and Remove Outliers from Dense Point Clouds** — M.-J. Rakotosaona et al. · *ICCV 2019*
  - 点云去噪 + 离群点移除，经典监督方法。
- **Pointfilter: Point Cloud Filtering via Encoder-Decoder Modeling** — D. Zhang et al. · *IEEE TVCG*, 2020
  - 编码器-解码器点云滤波。
- **Score-Based Point Cloud Denoising** — S. Luo, W. Hu · *ICCV 2021*
  - 基于分数匹配生成模型的高质量点云去噪。
- **Noise2Score3D: Tweedie's Approach for Unsupervised Point Cloud Denoising** — *ICCV 2025* · [Code](https://github.com/Bobby645/Noise2Score3D)
  - 最新无监督点云去噪（Tweedie 公式 + 分数估计）。

## 🎲 E. 域随机化与 Sim2Real 方法学

- **Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World** — J. Tobin et al. · *IROS 2017*
  - 域随机化奠基工作：在仿真中随机化（含传感器噪声）让策略学到域不变特征。
- **Automatic Domain Randomization and Deep Reinforcement Learning: A Scalable Approximation for the Real World** — OpenAI · *arXiv:1910.07113*, 2019
  - ADR：自动扩增噪声/物理参数范围。

## 📈 F. 鲁棒性评测与基准

- **RoboDepth: Robust Out-of-Distribution Depth Estimation under Corruptions** — *NeurIPS 2023 (Datasets & Benchmarks)* · [arXiv:2310.15171](https://arxiv.org/abs/2310.15171)
  - ⭐ 深度估计在多种退化（含真实感深度噪声）下的鲁棒性评测协议，可作为"注入噪声是否逼真"的间接度量。

## 📚 G. 综述

- **A Survey of Deep Learning-based Point Cloud Denoising** — *arXiv:2508.17011*, 2025 · [arXiv](https://arxiv.org/abs/2508.17011)
- **Deep Learning for 3D Point Cloud Enhancement: A Survey** — *arXiv:2411.00857*, 2024 · [arXiv](https://arxiv.org/abs/2411.00857)

---

## 📎 快速导航

| 文档 | 内容 |
|---|---|
| [研究综述与可行性分析](docs/research_notes.md) | 噪声物理来源、方法分类、可行性结论、研究空白 |
| [研究分类图谱](docs/taxonomy.md) | Mermaid 分类图 + 方法论对比 |
| [完整论文清单](docs/papers.md) | 全部论文的表格化清单（含 arXiv/DOI/一句话注释） |
| [数据集与基准](docs/datasets.md) | 真实/合成深度数据集、噪声评测基准 |
| [仿真器与噪声插件](docs/simulators_tools.md) | Habitat / Gazebo / Isaac Sim / AirSim / CARLA 的噪声支持与插件 |
| [研究路线图](docs/roadmap.md) | 分阶段研究计划（数据采集 → 噪声建模 → 注入 → 去噪 → 评测） |

## 🤝 贡献

欢迎通过 PR 补充论文、工具、数据集或研究笔记。要求：条目需附可验证链接（arXiv / DOI / 官方页），并标注与本仓库两个核心问题（去噪 / real2sim）的相关性。可参考 [检索方法学](docs/research_notes.md#检索方法学) 记录检索日期与关键词。

## ⚠️ 说明

- 仓库名为 `awsome_depth_noise`（按创建者要求保留拼写），检索与整理日期见各文档。
- 链接以出版方/arXiv 官方页面为准；如发现失效链接请提 Issue。

## 📄 License

MIT — 见 [LICENSE](LICENSE)。
