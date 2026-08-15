# 仿真器与噪声插件（Simulators & Noise Plugins）

> 噪声 Real2Sim 的"注入端"。以下仿真器/插件均支持（或可扩展支持）深度传感器噪声建模。链接为官方文档/仓库。

## 主流仿真器

| 仿真器 | 深度/ToF 传感器 | 内置噪声支持 | 备注 |
|---|---|---|---|
| **Habitat-Sim** | 深度（透视/全景） | ✅ `GaussianDepthNoiseModel`、`RedwoodDepthNoiseModel`（基于 Redwood 数据集的 Kinect 噪声统计）、bias 等 | 文档：[noise_models](https://aihabitat.org/docs/habitat-sim/habitat_sim.sensors.noise_models.html) · [RedwoodNoiseModel](https://aihabitat.org/docs/habitat-sim/habitat_sim.sensors.noise_models.RedwoodDepthNoiseModel.html) · 实现：[VisualSensor.cpp](https://github.com/facebookresearch/habitat-sim/blob/main/src/esp/sensor/VisualSensor.cpp) |
| **Gazebo / gz-sensors** | 深度相机（深度相机插件） | ✅ `ImageNoise`（高斯等）；生态插件 `gazebo_noisy_depth_camera`、`realsense_gazebo_plugin` | [gz-sensors ImageNoise](https://github.com/gazebosim/gz-sensors/blob/main/src/ImageNoise.cc) · [gazebo_noisy_depth_camera](https://github.com/peci1/gazebo_noisy_depth_camera) · [realsense_gazebo_plugin](https://github.com/PIC4SeR/realsense_gazebo_plugin) · 社区讨论：[Noise model for depth camera simulation](https://discourse.openrobotics.org/t/noise-model-for-depth-camera-simulation/36385) |
| **NVIDIA Isaac Sim** | ToF 相机传感器、深度 | ✅ 内置 ToF 传感器（含多径等物理仿真选项）；厂商集成 iToF（e-con、Orbbec） | 论坛：[Simulate Time-of-Flight 3D Sensor](https://forums.developer.nvidia.com/t/simulate-time-of-flight-3d-sensor/240304) · [e-con iToF in Isaac Sim](https://www.e-consystems.com/blog/camera/technology/robotics-development-just-got-faster-smarter-e-con-systems-itof-3d-camera-comes-to-nvidia-isaac-sim/) |
| **AirSim** | 深度/视差/法线视图 | ✅ 相机噪声与干扰（Camera noise & interference）设置 | [AirSim settings](https://microsoft.github.io/AirSim/settings/) |
| **CARLA** | LiDAR / 相机 | ✅ LiDAR 噪声参数（`dropoff_intensity_limit`、general noise 等） | [CARLA ref_sensors](https://github.com/carla-simulator/carla/blob/main/Docs/ref_sensors.md) |

## 可参考的"注入"实现范式

1. **解析模型注入**（最简单）：按 σ(d) 曲线 + 高斯/泊松噪声 + 缺失掩码 + 空间相关核，对渲染出的干净深度加噪。Habitat `RedwoodDepthNoiseModel` 即此类。
2. **物理仿真注入**（高保真）：用光线追踪/光子级仿真直接渲染带噪深度（ToF：Keller 2007、AMCW 2018；主动立体：T-RO 2023；LiDAR：arXiv:2512.05932）。
3. **学习式注入**（研究前沿）：
   - 生成式：扩散/流模型学真实噪声分布后采样注入（RGB 先例：RNSD、Noise Flow）；
   - 域适配：对抗式自适应噪声注入（CVPR 2023）；
   - 真实重合成：真实扫描重建场景后重渲染（LiDARsim，CVPR 2020）。
4. **混合式**（建议探索）：物理结构（如 σ(d)、多径模型）+ 学习参数/残差，兼顾保真与泛化。

## 建议的插件化工程路线

```
干净深度/点云（渲染器输出）
   │
   ├─ 噪声注入层（插件，可配置）：
   │    1) 距离相关随机误差 σ(d)        （解析 / 学习）
   │    2) 系统偏差 bias(d, T)          （解析 / 学习）
   │    3) 缺失掩码 p(d, reflectivity)  （解析 / 学习）
   │    4) 空间相关飞点（边缘/入射角）   （解析 / 学习）
   │    5) ToF：多径 / 卷绕（物理或学习）
   │
   └─ 输出：带噪深度图 / 点云 → 下游任务
```

> 目标：把噪声模型做成与传感器型号绑定的"配置文件/插件"，在 Gazebo / Isaac Sim / Habitat / AirSim 之间复用（可参考 Habitat 的 noise_models 模块设计）。
