# 研究分类图谱（Taxonomy）

深度相机噪声研究的整体分类，以及"学习真实噪声 → 噪声压制 / Real2Sim"两条主线在其中的位置。

## 1. 总览图

```mermaid
flowchart TB
    subgraph SRC["真实深度相机输出（噪声点云/深度图）"]
        A1["ToF（iToF / dToF）"]
        A2["结构光（Kinect v1）"]
        A3["主动立体（RealSense）"]
        A4["LiDAR（旋转 / 固态）"]
    end

    subgraph NOISE["噪声构成（物理来源）"]
        N1["随机误差 σ(d) ↑ 随距离"]
        N2["系统偏差 / 温度漂移"]
        N3["空间相关误差（边缘飞点、材质、入射角）"]
        N4["缺失 / 空洞（反射率、遮挡、量程）"]
        N5["ToF 特有：多径、卷绕、散粒噪声"]
        N6["时间抖动"]
    end

    subgraph MODELS["噪声建模方法"]
        M1["A. 解析/统计模型<br/>σ(d) 拟合、缺失率、相关核"]
        M2["B. 物理仿真<br/>光子飞行/多径/投影图案"]
        M3["C. 数据驱动学习<br/>生成式（扩散/流/GAN）· 自监督（Noise2Noise）· 域适配 · 真实重合成"]
        M4["D. 混合：物理结构 + 学习参数/残差"]
    end

    subgraph APPLY["两大应用"]
        APP1["噪声压制（Denoising）<br/>深度图/ToF 网络 · 点云去噪 · 自监督"]
        APP2["噪声 Real2Sim（噪声注入）<br/>Gazebo / Isaac / Habitat / AirSim 插件"]
    end

    SRC --> NOISE
    NOISE --> MODELS
    MODELS --> M4
    M1 --> APP1
    M2 --> APP1
    M3 --> APP1
    M4 --> APP1
    M1 --> APP2
    M2 --> APP2
    M3 --> APP2
    M4 --> APP2
```

## 2. 方法路线对比

| 路线 | 代表工作 | 保真度 | 成本 | 落地难度 | 适用传感器 |
|---|---|---|---|---|---|
| A. 解析/统计模型 | Khoshelham 2012；Nguyen 2012；Plozza 2024；Habitat Redwood 模型 | 中（随机误差好，缺失/多径差） | 极低 | 极低（直接做插件） | 全部（需逐型号标定） |
| B. 物理仿真 | Keller 2007；AMCW ToF 2018；主动立体 T-RO 2023；车规 LiDAR 2025 | 高 | 高（渲染+标定） | 中 | ToF、主动立体、LiDAR |
| C1. 生成式学噪声 | Noise Flow；RNSD（扩散）；SIDD | 高（学到的分布） | 中（需真实数据） | 中 | RGB 成熟，深度/点云空白 |
| C2. 自监督两帧 | Noise2Noise；SelfReDepth | 高（去噪目标） | 低（无需真值） | 低 | 深度图/点云 |
| C3. 域适配注入 | Project to Adapt；Adversarial Masking；S2R-DepthNet | 中高 | 中 | 中 | 深度、点云 |
| C4. 真实重合成 | LiDARsim | 高（噪声天然真实） | 高（需场景重建） | 中高 | LiDAR（可迁移至 RGB-D） |
| D. 混合 | 物理仿真 + 学习标定/残差（目前公开工作少） | 高 | 中高 | 中 | 全部（**建议重点探索**） |

## 3. 与"用户研究目标"的映射

```mermaid
flowchart LR
    U["研究目标"] --> T1["任务1：噪声压制<br/>从真实噪声点云学模式 → 去噪"]
    U --> T2["任务2：噪声 Real2Sim<br/>学噪声模式 → 注入仿真传感器"]
    T1 -.直接复用.-> C2["自监督两帧法<br/>Noise2Noise / SelfReDepth"]
    T1 -.参考.-> PC["点云去噪<br/>TotalDenoising / ScoreDenoise / Noise2Score3D"]
    T2 -.可落地.-> A["解析模型插件<br/>σ(d) + 缺失率 + 相关核"]
    T2 -.理想.-> C1["生成式学噪声<br/>扩散/流（条件：距离/反射率）"]
    T2 -.理想.-> C4["真实重合成<br/>NeRF/GS 重建 + 重渲染"]
    T2 -.高保真.-> B["物理仿真<br/>主动立体 T-RO 2023 / ToF 仿真"]
    T2 -.进阶.-> D["混合：物理+学习残差"]
```

> 推荐起点：**任务2 用路线 A 快速落地 + 路线 C1 做研究增量；任务1 用路线 C2 起步**。详见 [roadmap.md](roadmap.md)。
