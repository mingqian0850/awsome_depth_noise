# 精读笔记：Manipulation as in Simulation — Enabling Accurate Geometry Perception in Robots

> **阅读目的**：ByteDance Seed 的"学习深度相机噪声模式"工业级实践。与"噪声注入仿真"（real2sim）形成对照：它选择**学噪声 → 训练去噪插件 → 把真实数据变成"仿真级"**，让纯仿真训练的策略零样本部署到真实机器人。

## 元数据

| 项 | 值 |
|---|---|
| 标题 | Manipulation as in Simulation: Enabling Accurate Geometry Perception in Robots |
| 作者 | Minghuan Liu, Zhengbang Zhu, Xiaoshen Han, Peng Hu, Haotong Lin, Xinyao Li, Jingxiao Chen, Jiafeng Xu, Yichu Yang, Yunfeng Lin, Xinghang Li, Yong Yu, Weinan Zhang, Tao Kong, Bingyi Kang（**ByteDance Seed** + 上海交大 + 浙大 + 清华） |
| 发表 | **ICLR 2026**（poster） |
| arXiv | [arXiv:2509.02530](https://arxiv.org/abs/2509.02530)（2025-09-02，32 页） |
| 项目页 | https://manipulation-as-in-simulation.github.io/ |
| 类别 | cs.RO / cs.CV；传感器：RealSense D405/D415/D435/D455/L515、ZED 2i、Azure Kinect（10 种深度模式） |

## TL;DR

深度相机噪声大 → 提出 **Camera Depth Model (CDM)** 插件：输入 RGB + 原始深度，输出干净公制深度。CDM 的训练数据来自**神经数据引擎**：先用神经网络从真实多相机数据**自动学习两种噪声模式**（value noise 数值噪声 + hole noise 空洞噪声），再在仿真合成数据集上按学到的噪声模式合成带噪深度，得到 (RGB, 带噪深度, 真值深度) 配对数据。效果：**仅在仿真中训练（不加噪声、无真实微调）的 depth-only 策略，零样本部署到真实 UR5**，两个长时程任务（厨房、食堂）成功率与仿真相当。

## 方法与"噪声学习"细节

1. **噪声分类**（Fig.2）：`hole noise` = 深度缺失（立体匹配/光照/材质导致，如玻璃门、镜面、边界）；`value noise` = 其余一切（每台相机的 bias、模糊、抖动、畸变）。噪声模式依赖相机内参和物理安装 → 必须**逐相机建模**（camera-specific）。
2. **Hole 噪声模型**：DINOv2 backbone + DPT head，输入 RGB → 预测逐像素有效掩码（二分类，式 4）。
3. **Value 噪声模型**：微调 Depth Anything V2，把带噪深度视为"风格化相对深度"预测目标（仿射不变归一化 + L1，式 5）；**引导滤波**（guided filter）修复合成数据的公制尺度错配（式 7–8），随机核大小作为增强；手工规则补充高频噪声（神经网络难学高频）。
4. **合成管线**：`D̃ = μ(V(I)) · (H(I) < 0.5)`（式 6）——在 4 个开放合成数据集（HyperSim、DREDS、HISS、IRS，共 28 万+ 图）上合成带噪深度。
5. **ByteCameraDepth 数据集**：7 相机共轴支架同时采集（7 场景 × 每相机 1.7 万+ 帧，5Hz 采样）。
6. **CDM 结构**：双分支 ViT（RGB 分支 + 深度分支，DINOv2 初始化）+ 逐 token 融合（MHA）+ DPT 解码；直接吃原始带孔深度，无需 hole-filling；L1 + 梯度损失（式 9–10）。

## 关键结果

**深度指标（Hammer 数据集，零样本，无后处理对齐）**

| 设置 | L1 ↓ | RMSE ↓ | AbsRel ↓ |
|---|---|---|---|
| D435 原始深度 | 0.0550 | 0.1458 | 0.0708 |
| **CDM-D435** | **0.0258** | **0.0404** | **0.0312** |
| L515 原始深度 | 0.0312 | 0.0813 | 0.0475 |
| **CDM-L515** | **0.0156** | **0.0297** | **0.0229** |

- 跨相机泛化：CDM-L515 在 D435 数据上表现良好；两者对未见过的 iToF（Helios）零样本泛化更好（学到的噪声有共性）。
- 无 hole-filling 时 PromptDA/PriorDA 直接失效，CDM 不需要预处理。

**仿真→真实零样本操作（UR5 + Robotiq，各 30 次测试）**

| 相机 / 深度模型 | Kitchen（碗→微波炉→关玻璃门） | Canteen（叉子+盘子倾倒） |
|---|---|---|
| 仿真上界（Sim, D435 view） | ~30/50 | ~21/50 |
| None（原始深度直用） | 0/30 | 0/30 |
| PromptDA | 0/30 | 1/30 |
| PriorDA | 7/30 | 0/30 |
| **CDM-D435（D435 相机）** | **26/30** | **14/30** |
| **CDM-L515（L515 相机）** | 14/30 | 0/30（跨相机失配） |
| CDM-L515（L515 相机，用 CDM-L515） | 18/30 | 22/30 |

- 真实成功率 ≈ 仿真水平（"little to no performance degradation"），首次证明**无需加噪/真实微调**的纯仿真训练可行。
- 尺寸泛化：只有 CDM 让 Stack-Bowls 策略泛化到 4 种未见尺寸。
- 延迟：CDM 0.151s/帧（4090）→ 策略 >6Hz。

## 与"研究核心问题"的关系（⭐ 最重要）

| 维度 | 分析 |
|---|---|
| "学习真实噪声" | ⭐⭐⭐ 工业级实证：value/hole 双噪声模型从**真实多相机数据**学习，再用于仿真数据合成 |
| 与"噪声注入"（real2sim）的关系 | ⭐⭐ **对照路线**：论文明确主张"给仿真加噪声是下策，会损害几何信息"；选择**学噪声→训练去噪器→把真实数据降噪到仿真级**。两条路线共享"噪声学习"基础，部署方向相反——这是研究设计中必须论证的路线选择 |
| 对"噪声压制" | ⭐⭐⭐ 它就是"深度相机噪声压制"的 SOTA 级实践（CDM 即逐相机去噪插件） |
| 对"VLA 成功率" | 策略为 depth-only 扩散策略（非语言条件 VLA），但来自 ByteDance Seed Robotics，未来工作指向机器人基础模型（VLA 时代）的数据利用；可视为"提升操作策略成功率"的几何感知前置插件 |

## 局限与可改进点（研究机会）

1. 策略仅用深度（无语言/无 RGB 输入），未与 VLA 端到端结合；
2. 噪声模型学的是"模式"而非显式分布（无 σ(d) 曲线、无反射率条件缺失率等可解释参数）；
3. 高频噪声需手工规则补充（神经网络学习局限）；
4. 跨相机泛化有边界（CDM-D435 用于 L515 时 Canteen 全失败）；
5. ByteCameraDepth 数据集未声明开源；
6. 逐相机建模成本高（每台相机都要采集+训练）。

## 延伸阅读（仓库内）

- [结构光物理仿真（ICRA 2024，Bai et al.）](close-sim2real-gap-structured-light.md) — "仿真链路让噪声涌现"的对照范式
- [主动立体物理仿真（T-RO 2023，arXiv:2201.11924）](../papers.md)
- [噪声表征基线：Khoshelham 2012 / Plozza 2024（PMD Flexx2）](../papers.md)
- [RoboDepth（NeurIPS 2023）：深度退化鲁棒性评测](../papers.md)
