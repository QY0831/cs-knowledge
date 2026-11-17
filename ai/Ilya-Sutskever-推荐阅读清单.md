# Ilya Sutskever 推荐阅读清单（Deep Learning Reading List）

> 来源：Ilya Sutskever 给 John Carmack 的一份约 30 篇论文的阅读清单，并附言：
> "If you really learn all of these, you'll know 90% of what matters today."
>
> 原仓库：[dzyim/ilya-sutskever-recommended-reading](https://github.com/dzyim/ilya-sutskever-recommended-reading)（源自 [Twitter 帖](https://twitter.com/keshavchan/status/1787861946173186062)）
> 本文在原清单基础上补充了缺失的原文链接、年份与一句话导读。

## 清单总览

| # | 论文 / 文章 | 主题 | 年份 |
|---|---|---|---|
| 1 | The Annotated Transformer | Transformer 逐行实现 | 2018 |
| 2 | The First Law of Complexodynamics | 复杂度与熵 | 2011 |
| 3 | The Unreasonable Effectiveness of RNNs | 字符级语言模型 | 2015 |
| 4 | Understanding LSTM Networks | LSTM 直觉 | 2015 |
| 5 | Recurrent Neural Network Regularization | Dropout 用于 RNN | 2014 |
| 6 | Keeping NN Simple by Minimizing Description Length | 权重的最小描述长度 | 1993 |
| 7 | Pointer Networks | 指针/输出词表可变 | 2015 |
| 8 | ImageNet Classification with Deep CNNs (AlexNet) | 深度学习复兴 | 2012 |
| 9 | Order Matters: Seq2seq for Sets | 集合的顺序不变性 | 2015 |
| 10 | GPipe | 流水线并行 | 2018 |
| 11 | Deep Residual Learning (ResNet) | 残差连接 | 2015 |
| 12 | Multi-Scale Context Aggregation by Dilated Convolutions | 空洞卷积 | 2015 |
| 13 | Neural Message Passing for Quantum Chemistry | 图神经网络 | 2017 |
| 14 | Attention Is All You Need | Transformer | 2017 |
| 15 | NMT by Jointly Learning to Align and Translate | 注意力机制起源 | 2014 |
| 16 | Identity Mappings in Deep Residual Networks | Pre-activation ResNet | 2016 |
| 17 | A Simple NN Module for Relational Reasoning | Relation Network | 2017 |
| 18 | Variational Lossy Autoencoder | VAE + 自回归 | 2016 |
| 19 | Relational Recurrent Neural Networks | 记忆与关系推理 | 2018 |
| 20 | Quantifying the Rise and Fall of Complexity (Coffee Automaton) | 复杂度演化 | 2014 |
| 21 | Neural Turing Machines | 外部记忆 | 2014 |
| 22 | Deep Speech 2 | 端到端语音识别 | 2015 |
| 23 | Scaling Laws for Neural Language Models | 缩放定律 | 2020 |
| 24 | A Tutorial Introduction to MDL | 最小描述长度 | 2004 |
| 25 | Machine Super Intelligence | 通用智能理论 | 2008 |
| 26 | Kolmogorov Complexity and Algorithmic Randomness | 柯氏复杂度 | 2017 |
| 27 | CS231n | CNN 与视觉课程 | 2015+ |

---

## 一、序列建模与 RNN 时代

### 3. The Unreasonable Effectiveness of Recurrent Neural Networks
Andrej Karpathy, 2015. [[Blog]](https://karpathy.github.io/2015/05/21/rnn-effectiveness/) [[Code]](https://github.com/karpathy/char-rnn)

字符级 RNN 语言模型的"顿悟文"。展示了 RNN 能无中生有地学出 LaTeX、C 代码、莎士比亚文风的结构——说明**只要建模 `p(next token | prefix)`，结构就会从数据里涌现**。这就是今天 LLM 的思想原型。

### 4. Understanding LSTM Networks
Christopher Olah, 2015. [[Blog]](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)

用图和直觉讲清 LSTM 三门（输入门/遗忘门/输出门）与 cell state 加法式更新。理解"为什么梯度能沿 cell state 稳定流传"，是理解后来残差连接与状态空间模型的前置知识。

### 5. Recurrent Neural Network Regularization
Wojciech Zaremba, Ilya Sutskever, Oriol Vinyals, 2014. [[ArXiv]](https://arxiv.org/abs/1409.2329) [[pdf]](https://arxiv.org/pdf/1409.2329) [[Code]](https://github.com/wojzaremba/lstm)

提出**只对非循环连接施加 dropout**（同一时间步的不同层之间共享 mask，循环权重不 dropout），否则噪声会沿时间步累积破坏长期记忆。一个"正则化必须尊重模型结构"的经典案例，也是深度学习工程直觉的范本。

---

## 二、卷积网络与视觉

### 8. ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)
Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton, 2012. [[Paper]](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) [[pdf]](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)

深度学习的引爆点。两个 GPU 上训练 8 层 CNN 拿下 ILSVRC 2012，用 ReLU、数据增强、dropout、GPU 实现把"规模 + 算力 + 简单算法"的路线坐实。

### 11. Deep Residual Learning for Image Recognition (ResNet)
Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun, 2015. [[ArXiv]](https://arxiv.org/abs/1512.03385) [[pdf]](https://arxiv.org/pdf/1512.03385)

残差连接 `y = F(x) + x`：让"学恒等映射"变得平凡，从而把网络轻松堆到 100+ 层。**这一条捷径（skip connection）几乎出现在后面所有架构中**——Transformer 的 residual stream、U-Net、扩散模型都依赖它。

### 16. Identity Mappings in Deep Residual Networks (ResNet v2)
Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun, 2016. [[ArXiv]](https://arxiv.org/abs/1603.05027) [[pdf]](https://arxiv.org/pdf/1603.05027)

前激活（pre-activation）版本：把 BN + ReLU 移到卷积分支内部，让主干保持纯恒等映射，信号可以在极深网络里"无阻地"前向与反向传播。是对 ResNet 为什么有效的机理解释。

### 12. Multi-Scale Context Aggregation by Dilated Convolutions
Fisher Yu, Vladlen Koltun, 2015. [[ArXiv]](https://arxiv.org/abs/1511.07122) [[pdf]](https://arxiv.org/pdf/1511.07122)

空洞/膨胀卷积：不增加参数与降采样就指数级扩大感受野，保留分辨率做密集预测（语义分割）。现代 CNN 与音频/序列卷积里仍是基础工具。

### 27. CS231n: Convolutional Neural Networks for Visual Recognition
Stanford 课程. [[Site]](http://cs231n.stanford.edu/)

CNN 与视觉识别的系统课程，含反向传播、优化、正则化、可视化、检测分割的手写作业。清单里唯一"课"级材料，用来补齐工程细节。

---

## 三、注意力与 Transformer

### 15. Neural Machine Translation by Jointly Learning to Align and Translate
Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, 2014. [[ArXiv]](https://arxiv.org/abs/1409.0473) [[pdf]](https://arxiv.org/pdf/1409.0473)

注意力机制的起点：解码每一步时用 soft alignment 动态聚合编码器所有隐状态，取代把整句压进一个定长向量。**"查询-键-值加权求和"的原始形式就在这里**。

### 14. Attention Is All You Need
Ashish Vaswani, et al., 2017. [[ArXiv]](https://arxiv.org/abs/1706.03762) [[pdf]](https://arxiv.org/pdf/1706.03762)

Transformer：删掉循环，只留注意力 + FFN + 残差 + LayerNorm。可高度并行、可任意建长程依赖，成为今天一切大模型（GPT / BERT / ViT / 扩散主干）的基座。

### 1. The Annotated Transformer
Sasha Rush, et al., 2018. [[Blog]](https://nlp.seas.harvard.edu/annotated-transformer/) [[Code]](https://github.com/harvardnlp/annotated-transformer/)

"论文即 notebook"：把整篇 Transformer 逐段变成可运行 PyTorch 代码。读它比读论文更快获得可执行的心智模型，是复现类文本的样板。

### 23. Scaling Laws for Neural Language Models
Jared Kaplan, et al., 2020. [[ArXiv]](https://arxiv.org/abs/2001.08361) [[pdf]](https://arxiv.org/pdf/2001.08361)

语言模型损失与参数量/数据量/算力呈幂律关系，且对架构细节不敏感。给出了"用多大模型、喂多少 token"的定量依据，是大模型时代的工程指南针。

### 10. GPipe: Easy Scaling with Micro-Batch Pipeline Parallelism
Yanping Huang, et al., 2018. [[ArXiv]](https://arxiv.org/abs/1811.06965) [[pdf]](https://arxiv.org/pdf/1811.06965)

把大模型切层分到多设备，用 micro-batch 流水线填满气泡（以 batch 换并行度）。模型并行/流水线并行的入门必读，也是"大模型怎么训得动"的系统答案。

---

## 四、架构与推理模块（Ilya 特别偏爱的"结构化归纳偏置"）

### 7. Pointer Networks
Oriol Vinyals, Meirong Fortunato, Navdeep Jaitly, 2015. [[Paper]](https://papers.nips.cc/paper/5866-pointer-networks) [[pdf]](https://arxiv.org/pdf/1506.03134)

用注意力权重直接"指向"输入中的位置作为输出，解决输出词表随输入长度变化的问题（排序、TSP、凸包）。注意力 = 指针的思想源头。

### 9. Order Matters: Sequence to Sequence for Sets
Oriol Vinyals, Samy Bengio, Manjunath Kudlur, 2015. [[ArXiv]](https://arxiv.org/abs/1511.06391) [[pdf]](https://arxiv.org/pdf/1511.06391)

读集合、写序列：输入用对称（顺序无关）的注意力编码，输出由解码顺序决定。讲清**什么该有顺序、什么该顺序不变**这一关键的归纳偏置。

### 17. A Simple Neural Network Module for Relational Reasoning
Adam Santoro, et al., 2017. [[ArXiv]](https://arxiv.org/abs/1706.01427) [[pdf]](https://arxiv.org/pdf/1706.01427)

Relation Network：把推理拆成"两两配对 → 求和/池化 → 再推理"的显式模块，在 CLEVR 上大幅领先 LSTM。说明某些能力靠架构结构比靠规模更省力。

### 19. Relational Recurrent Neural Networks
Adam Santoro, et al., 2018. [[ArXiv]](https://arxiv.org/abs/1806.01822) [[pdf]](https://arxiv.org/pdf/1806.01822)

把多头点积注意力（关系记忆）插进 LSTM 的记忆更新里，让循环网络能做跨时间步的关系推理。RNN 与注意力的桥梁之一。

### 13. Neural Message Passing for Quantum Chemistry
Justin Gilmer, et al., 2017. [[ArXiv]](https://arxiv.org/abs/1704.01212) [[pdf]](https://arxiv.org/pdf/1704.01212)

提出消息传递神经网络（MPNN）：统一了多种图神经网络，边/节点特征迭代聚合，在分子能量预测上超越手工特征方法。图表示学习的标准框架。

### 21. Neural Turing Machines
Alex Graves, Greg Wayne, Ivo Danihelka, 2014. [[ArXiv]](https://arxiv.org/abs/1410.5401) [[pdf]](https://arxiv.org/pdf/1410.5401)

给网络外接可微的读写记忆矩阵，端到端学会排序、复制、联想回忆。**"计算与存储分离、可微外部记忆"**的先声，也是今天记忆/检索增强与状态空间讨论的祖本。

### 18. Variational Lossy Autoencoder
Xi Chen, et al., 2016. [[ArXiv]](https://arxiv.org/abs/1611.02731) [[pdf]](https://arxiv.org/pdf/1611.02731)

用强自回归解码器 + 限制隐变量容量，让 VAE 隐变量专心编码全局信息、局部细节交给自回归。对"隐变量该记什么、不该记什么"给了信息论解释，是离散/连续表征争论的必修。

### 22. Deep Speech 2: End-to-End Speech Recognition in English and Mandarin
Dario Amodei, et al., 2015. [[ArXiv]](https://arxiv.org/abs/1512.02595) [[pdf]](https://arxiv.org/pdf/1512.02595)

把端到端 CNN+RNN+CTC 做到生产级（同一套架构学英语与中文），并系统讨论批归一化、数据流水线、规模化训练配方。深度学习"工业落地"的经典报告。

---

## 五、复杂度、信息论与"智能"的理论侧

> Ilya 反复强调：要理解学习，必须理解**压缩即理解**（compression = prediction = intelligence）。

### 6. Keeping Neural Networks Simple by Minimizing the Description Length of the Weights
Geoffrey Hinton, Drew van Camp, 1993. [[Paper]](https://dl.acm.org/doi/10.1145/168304.168306) [[pdf]](https://www.cs.toronto.edu/~hinton/absps/colt93.pdf)

用 MDL 给权重加"编码代价"，等价于把权重限制为粗粒度的少数表示 → 得到**贝叶斯风格的软正则化**，并把权重编码长度视为泛化能力的度量。反向传播 + MDL 的早期合流。

### 24. A Tutorial Introduction to the Minimum Description Length Principle
Peter Grünwald, 2004. [[ArXiv]](https://arxiv.org/abs/math/0406077) [[pdf]](https://arxiv.org/pdf/math/0406077)

MDL 入门：把"学习"形式化为"找最短的数据生成说明"。是理解 Occam 剃刀、泛化界、"为什么小模型/短程序更好"的统一语言。

### 26. Kolmogorov Complexity and Algorithmic Randomness
A. Shen, V. A. Uspensky, N. Vereshchagin, 2017. [[Book]](https://www.lirmm.fr/~ashen/kolmbook-eng.pdf)

柯尔莫哥洛夫复杂度的教科书版：最短描述长度定义、不可压缩性与随机性、与信息论的关系。给出"复杂度"不可计算但仍然有意义的严格讨论。

### 2. The First Law of Complexodynamics
Scott Aaronson, 2011. [[Blog]](https://scottaaronson.blog/?p=762)

一个幽默而认真的猜想：封闭系统的"复杂度"（比对"熵"更细的量）先升后降。讨论为什么会先出现秩序再瓦解，以及怎么定义"有趣"。

### 20. Quantifying the Rise and Fall of Complexity in Closed Systems: The Coffee Automaton
Scott Aaronson, Sean Carroll, Lauren Ouellette, 2014. [[ArXiv]](https://arxiv.org/abs/1405.6903) [[pdf]](https://arxiv.org/pdf/1405.6903)

把"复杂度先升后降"做成可计算实验（咖啡搅拌的格子自动机）。与上一篇文章配对阅读，是"为什么宇宙/神经网络会自发产生结构"的抽象思考。

### 25. Machine Super Intelligence
Shane Legg, PhD Thesis, 2008（导师 Marcus Hutter）. [[Thesis]](https://sonar.ch/global/documents/317954) [[Publications]](http://www.vetta.org/publications/)

用 Hutter 的 AIXI 框架讨论通用智能的**度量问题**：定义"智能"为在广泛环境族上的期望性能，并推出"压缩即智能"的论证。AIXI 也是"预测一切可计算模式的贝叶斯最优体"。

---

## 阅读建议

1. **先建立主干**：Karpathy RNN → Olah LSTM → Bahdanau 注意力 → Transformer（配 Annotated Transformer 敲一遍）→ ResNet → Scaling Laws。这条线能在几天内把 2014–2020 的技术主轴串起来。
2. **再补归纳偏置**：Pointer Networks / Order Matters / Relation Networks / NTMs，理解"什么结构值得写进架构"。
3. **最后读理论侧**：Hinton 1993、MDL、Kolmogorov、Aaronson 两篇、Legg 论文。这部分不是工具书，而是 Ilya 反复讲的"学习 = 压缩"的哲学底盘。
4. 逐篇读完优于泛读。每篇尝试写一段"它解决了什么、用什么机制、留下了什么"。

## 与原清单的差异

- 补齐了原仓库中仅列标题（11–27 项）的链接，按 arXiv / 会议 / 作者主页选取可访问地址，均已核对可打开。
- 增加年份、主题、中文导读与阅读路线。
- `Machine Super Intelligence` 原文 `vetta.org` 直链现已返回 401，改用 Lugano 官方机构库（sonar.ch）条目。

## 相关笔记

- [Ilya Sutskever 之外的另一条线：Karpathy 从零实现](llm/andrej-karparthy-nn/) — 和清单里的 RNN/LSTM/Transformer 论文对照着看
- [吴恩达 Deep Learning 笔记](吴恩达%20Deep%20Learning%20笔记.md) — 基础概念补齐
- [Grokking Deep Learning](grokking-deep-learning/) — 从零手写梯度
