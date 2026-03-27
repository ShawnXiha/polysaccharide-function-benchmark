# 多糖（Polysaccharides）数据资源、知识图谱、近五年研究进展与机器学习机会深度研究报告

## 执行摘要

多糖研究的核心矛盾是“结构极其复杂且异质（组成、糖苷键、分支、修饰、分子量分布）”与“可计算、可共享、可复现的数据与标准不足”之间的张力：一方面，结构表征在近五年持续向高通量与多模态融合推进，NMR在多维、固态与复杂体系中的应用成为热点，MS（含IM‑MS、MALDI‑ISD等）在保持高信息量的同时提升了对复杂多糖的解析能力，并出现面向糖苷键解析的更系统化谱库/流程；另一方面，数据库生态呈现“糖链（glycan）资源丰富但以寡糖/糖蛋白糖链为主、真正聚焦长链多糖（polysaccharide）且携带可靠功能标签的数据稀缺”的结构性不平衡。GlyTouCan作为国际糖链注册库强调以统一ID覆盖从“单糖组成”到“完全定义结构”的不同解析分辨率，并支撑多库互联；GlyGen以集成与知识图谱（SPARQL端点）为特色；UniCarb‑DB提供人工注释的谱图证据；CSDB偏向天然糖类（尤其微生物/植物）结构与NMR信息；而面向“多糖结构‑健康功能/证据”的新型资源DoLPHiN（Food Chemistry 2025）与面向多糖三维结构的PolySac3DB为多糖机器学习提供了罕见的“可监督信号入口”。[\[1\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821)

机器学习方面，糖科学（更广义glycobiology/glycomics）已形成一批可复现的代表性工作：以图神经网络学习糖链表示的SweetNet（并提供代码）；以“分支语言”建模的glyBERT；以及从LC‑MS/MS端到端预测糖结构的CandyCrunch（Nature Methods 2024，报告约90% top‑1准确率，并开放代码）。与此同时，社区开始推动基准化（如GlycanML、GlycoGym）与工具化（glycowork数据集与模型接口），但这些方法多数仍围绕“糖链（寡糖/糖蛋白糖链）”任务而非“长链多糖”本体问题（分子量分布、重复单元、统计/不确定连接、修饰位点密度等）。[\[2\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161)

基于数据与方法的现实约束，本报告提出六条可落地的机器学习研究方向：①面向DoLPHiN/CSDB等的“多糖结构‑功能”多任务预测（GNN/Transformer）；②多模态“谱图→结构”端到端学习（MS+NMR+链接分析）；③加入CAZy与合成/改造约束的生成模型设计新多糖；④多源融合的多糖知识图谱（KG）驱动功能挖掘与证据追踪；⑤应对稀缺与高成本实验的主动学习/小样本学习闭环；⑥多糖/糖链“基础模型”式自监督预训练与跨任务迁移。我们给出每个方向的目标、数据、模型、指标、风险与缓解，并提供18个月里程碑甘特图、优先级评分与交付物清单（论文/数据集/代码/KG）。

## 范围界定与假设

本报告的“多糖（polysaccharides）”默认指由单糖通过糖苷键连接形成的长链碳水化合物材料与生物大分子，既包含同多糖与杂多糖，也包含常见修饰（如硫酸化、乙酰化、甲基化、羧基化等）以及“重复单元（repeating unit）”与“统计/不确定结构”的情况；结构表征维度覆盖单糖组成与比例、糖苷键连接方式（位点、α/β构型）、分支结构、分子量与分布（如Mw、Mn与PDI的概念映射到生物多糖语境），并将其与功能/应用（生物活性、材料学、药用、食品科学）以及合成与改造（化学/酶法/生物合成）相联系。该范围与GlyTouCan对“从组成到完全结构、允许不同分辨率登记”的设计理念一致，可用于解释为何数据库经常同时收录寡糖与多糖片段/重复单元描述。[\[3\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821)

由于用户未限定来源与应用领域，本报告采用“全覆盖”假设：天然来源涵盖植物、微生物（含细菌/真菌外多糖等）、海洋来源（海藻/海洋微生物等）与相关生物材料；应用覆盖食品（膳食纤维/胶体/发酵底物）、药用与健康（免疫调节、抗病毒、抗肿瘤等）、材料与生物医用（多糖水凝胶、创面敷料、组织工程等）、以及疫苗/糖缀合物相关场景。[\[4\]](https://www.mdpi.com/2072-6643/14/19/4116)

时间窗口按用户要求覆盖2018–2026（截至本报告撰写日2026‑03‑25，Asia/Seoul）。对2026年的“最新状态”类信息，优先引用可直接反映更新日期/版本的官方来源（例如CAZy主页显示最近更新日期）。[\[5\]](https://www.cazy.org/)

明确未指定项与边界：  
本报告会在涉及“糖链（glycan）”数据库与机器学习时，解释其与“多糖（polysaccharide）”的交叉：许多基础标准、表示法、谱图算法与数据生态来自糖蛋白糖链/寡糖领域，但其方法学（图表示、分支语法、谱图→结构）对多糖同样关键；然而，长链多糖的关键挑战（分子量分布、重复单元统计性、样品纯度与批间差）在现有glycan‑centric方法中往往被弱化或忽略，这正是本报告提出研究机会的主要动机之一。[\[6\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161)

## 数据资源与知识图谱生态

多糖/糖链数据生态可按“结构注册与标准化→证据（谱图/3D/文献）→功能与表型→酶与合成/生物路径→集成与知识图谱”分层理解。GlyTouCan提供全球唯一的糖链结构登录与ID体系，强调能处理结构不确定性并覆盖不同解析分辨率；GlyGen定位为多源整合与分发，并提供基于RDF三元组库的SPARQL端点以支持程序化查询；UniCarb‑DB强调人工注释并与实验谱图相绑定；CSDB聚焦天然糖类结构、分类学与NMR等文献整理；DoLPHiN则把“长链天然多糖的结构要素 \+ 健康功能证据”组织成可检索条目；PolySac3DB专注多糖三维结构条目；CAZy从“形成/改造/降解糖苷键的酶”视角组织家族、结构域与基因组注释，与多糖合成与改造强相关。[\[7\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821)

### 主要数据库与知识图谱对比

下表将“糖链资源（glycan‑centric）”与“多糖资源（polysaccharide‑centric）”并列比较，重点关注数据类型、覆盖范围、访问方式（Web/API/SPARQL/下载）、质量控制与许可（若官方页面/权威汇总显式给出则记录；若未明确则标注“需进一步核查”）。

| 资源 | 主要对象 | 数据类型与证据链 | 覆盖与偏好 | 访问方式（API/下载/图谱） | 质量控制特征 | 许可与可用性要点 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| GlyTouCan | 糖链结构注册库（含不同分辨率/不确定结构） | 结构、motif、统一ID；支持从单糖组成到完全定义结构登记；多库互联枢纽 | 面向广义glycan；可作为多糖片段/重复单元的结构锚点 | Web检索与服务端实现（有公开代码仓库/服务端实现）；与合作库自动互链 | 登记时做一致性检查；更偏“注册/分配ID”而非生物学意义强审稿式 curated | 许可在权威汇总中给出CC类许可（需在使用前核对具体条款）；维护稳定[\[8\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821) |
| GlyGen | 集成型糖科学知识库/图谱 | 整合多国际数据源，提供统一检索；RDF三元组、SPARQL端点支持知识图谱查询 | 面向糖链/糖缀合物与相关蛋白等；适合作为跨源KG“骨架层” | Web；SPARQL端点（sparql.glygen.org）；配套数据模型论文 | 强调集成、标准化与可追溯数据模型 | 权威汇总给出CC‑BY‑4.0；适合再利用与构建下游KG[\[9\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292) |
| GlyCosmos | 糖科学门户（含多库入口与工具） | 聚糖相关数据门户，提供格式转换等API入口（如GlycanFormatConverter） | 面向聚糖科学生态；可作为工具与数据入口 | Web；公开API（GlycanFormatConverter API 等） | 作为门户与工具集合，质量依赖上游数据源 | 有公开API版本与支持周期说明；便于工程化接入[\[10\]](https://glycosmos.org/) |
| UniCarb‑DB | 实验谱图驱动的糖组数据库 | 人工注释、实验验证的LC‑MS/MS谱图与结构条目；支持谱库匹配 | 偏游离糖/糖蛋白糖链；对“谱图证据”建模价值高 | Web；同时强调可下载版本/便于集成 | “人工注释 \+ 实验验证谱图”是其核心卖点 | 许可需单独核查；适合训练/评测谱图相关模型[\[11\]](https://unicarb-db.expasy.org/) |
| CSDB（Carbohydrate Structure Database） | 天然糖类结构（偏细菌/植物/真菌等） | 手工整理的天然糖结构、分类学、文献、NMR信号等 | 官方页面给出覆盖更新到2023（细菌/古菌/真菌/原生生物更完整；植物较早） | Web检索 | “手工整理/文献驱动”并给出覆盖范围说明 | 许可需核查；对天然多糖结构抽取与NMR信息很关键[\[12\]](https://csdb.glycoscience.ru/database/) |
| CarbBank / CCSD（历史） | 历史糖结构与文献数据库 | 1995年前后文献覆盖较多，属于早期糖结构数据库体系 | 历史性资源；与现代库（如GlycomeDB/CSDB）存在继承关系 | 多为档案/项目描述 | 主要价值在历史数据与演化脉络 | 以档案方式引用，注意可用性与格式迁移成本[\[13\]](https://cordis.europa.eu/project/id/BIO2930001) |
| GlycomeDB（历史/过渡） | 糖结构元数据库（已并入生态） | 曾整合多糖库并统一结构/分类信息；其站点明确“任务随GlyTouCan出现而终止/并入” | 作为“整合思路与历史接口”仍有参考价值 | Web；有NAR论文描述集成范围（含PDB碳水化合物） | 强调统一与整合 | 站点明确已并入GlyTouCan生态；用于理解数据整合策略[\[14\]](https://www.glycome-db.org/) |
| PDB糖链数据 \+ 工具（GLYCAM‑Web, pdb‑care, Privateer） | 3D结构中的糖/糖链（含糖蛋白糖链与糖配体） | PDB中糖残基/糖链建模、验证与质量控制；支持查找与验证糖链建模 | 偏结构生物学中的糖链；对“3D表示/验证/约束”重要 | GLYCAM‑Web提供PDB糖链检索；pdb‑care与Privateer用于识别与验证 | 指向“建模一致性、残基码/连接正确性”问题 | 许可需分别看工具；对构建3D数据集与评估至关重要[\[15\]](https://glycam.org/portal/gf_home/) |
| PolySac3DB | 多糖三维结构数据库 | 多糖3D结构条目（数据库简介提到约157条目） | 明确面向“polysaccharide 3D structures” | Web检索 | 3D条目规模较小但高价值（适合3D/构象学习） | 许可需核查；适合高质量小数据集研究[\[16\]](https://polysac3db.cermav.cnrs.fr/) |
| DoLPHiN（中国团队主导） | 天然长链多糖结构‑健康功能数据库 | 条目含来源物种、单糖组成比例、分子量、糖苷键、NMR信息与健康功能/证据等；论文与站点给出可检索维度 | 明确偏“天然功能多糖/健康益处”；条目规模（站点显示约5085条） | Web开放访问；按多维条件检索 | 声明数据来自同行评议原始论文并做规范化 | 对多糖ML最关键的“结构‑功能监督信号”之一[\[17\]](https://www.sciencedirect.com/science/article/pii/S0308814625037860) |
| CAZy | 碳水化合物活性酶家族库 | 按家族组织降解/修饰/合成糖苷键相关酶及CBM等模块，含基因组注释入口 | 与多糖合成与改造、降解机理直接相关 | Web；基因组/家族浏览 | 依家族与功能域体系维护；主页显示更新日期（2026‑03‑04） | 适合将“可合成/可改造的结构空间”引入生成模型与路线规划[\[18\]](https://www.cazy.org/) |

### 表示标准、格式转换与知识图谱关键技术

多糖/糖链的机器学习与跨库融合高度依赖表示标准。GlycoCT被提出为统一序列格式，含condensed与XML等变体，并支持一定程度的结构歧义与重复子单元表达；WURCS体系强调对歧义与重复单元等情况的表达能力，社区亦有专门工作组推进指南与实现；SNFG规范了以符号系统可视化单糖与复杂糖链（利于人工标注/可视化工具）。[\[19\]](https://www.sciencedirect.com/science/article/pii/S0008621508001353)

工程上，GlycanFormatConverter以API形式提供多格式互转并可联动检索GlyTouCan ID；同时，Python生态中glypy提供糖结构读写与操作，并提到可通过SPARQL与GlyTouCan/UniCarbKB等交互；这样可将数据管道从“网页下载/手工整理”转到“可复现的程序化ETL”。[\[20\]](https://api.glycosmos.org/glycanformatconverter/)

知识图谱层面，GlyGen论文明确其使用Virtuoso三元组库并提供SPARQL端点用于程序化访问；若自建多糖KG，可采用RML/R2RML映射把关系型/JSON等异构数据物化为RDF（例如morph‑kgc提供从异构表格/JSON构建RDF知识图谱的开源引擎思路）。[\[21\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292)

### 视觉示意：多糖数据到知识图谱的集成路径（示意图）

flowchart TB  
  A\[原始来源\<br/\>文献/数据库/实验数据\] \--\> B\[结构标准化\<br/\>GlycoCT/WURCS/IUPAC\]  
  B \--\> C\[实体对齐与消歧\<br/\>ID映射:GlyTouCan等\]  
  A \--\> D\[证据/模态数据\<br/\>MS/NMR/色谱/3D/生物活性\]  
  C \--\> E\[多糖知识图谱(KG)\<br/\>RDF/Property Graph\]  
  D \--\> E  
  E \--\> F\[下游任务\<br/\>检索/推理/ML训练/生成设计\]  
  F \--\> G\[实验验证闭环\<br/\>提取-纯化-结构确认-功能测定\]  
  G \--\> E

## 近五年研究进展与研究空白（2018–2026）

### 结构解析与表征技术进展

NMR方面，多糖结构与构象研究持续受益于多维NMR方法、固态/原位分析思路及与复杂体系（如细胞壁、食品体系）结合的解析框架。Food Hydrocolloids的综述系统总结了多糖结构与构象NMR分析的进展、挑战与展望，并指出“原位细胞壁结构解析”等应用是热点之一。[\[22\]](https://www.sciencedirect.com/science/article/pii/S0963996921001897)

MS方面，近年出现面向“完整多糖（intact polysaccharides）”的MS结构表征综述，强调MS常与化学/酶法降解联用以解决复杂度；同时，离子淌度‑质谱（IM‑MS）被用于辅助解析多糖连接方式与构型信息，并出现小型标准/数据库构建以支持到达时间分布与碎裂模式比对。[\[23\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685)

糖苷键/连接方式解析方面，传统甲基化‑GC‑MS仍是基础技术路线之一；近年出现更系统化的“甲基化分析库/衍生物库”工作以缓解标准不足与异构体多样造成的识别困难，从而更好支撑复杂多糖连接方式鉴定。[\[24\]](https://www.sciencedirect.com/science/article/pii/S0144861725006150)

研究空白（结构解析）：  
多糖解析仍高度依赖“多手段组合 \+ 专家经验”，缺少像蛋白/核酸那样统一的端到端自动化结构解析工作流；尤其在样品异质、结构歧义（统计连接/重复单元长度分布）、以及不同模态数据（NMR、MS、色谱、链接分析）之间的对齐与联合推断方面，仍缺乏公认的标准数据集与评测体系。[\[25\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685)

### 功能研究热点：免疫调节、肠道菌群与抗病毒

膳食多糖‑肠道菌群‑健康相关研究持续升温，多篇综述总结了膳食多糖如何调节菌群组成并影响宿主健康、代谢物（如SCFAs）与免疫状态。此类研究推动了“结构‑发酵利用‑代谢物‑健康效应”的链条化理解，但也暴露出结构注释粗粒度、实验体系异质、以及因果识别困难等问题。[\[26\]](https://www.mdpi.com/2072-6643/14/19/4116)

真菌、细菌与藻类多糖的免疫调节与抗肿瘤活性亦是热点方向之一。相关综述强调食用菌多糖具有多种生物活性并聚焦免疫调节机制整理；同时，硫酸化多糖的抗病毒活性及其构效关系被系统评述，形成“来源‑结构特征‑机制假说”的研究框架。[\[27\]](https://www.sciencedirect.com/science/article/pii/S2213453021000483)

研究空白（功能与构效）：  
该方向普遍存在“结构表征不充分/不可比”“杂质（蛋白、内毒素）干扰活性判读”“不同实验模型的效果难以量化对齐”“临床与真实人群证据不足”等问题。DoLPHiN尝试把结构要素（单糖组成、分子量、糖苷键、NMR信息）与健康功能条目化，是向“可计算构效知识”迈进的重要一步，但仍需要更严格的证据分级与实验可复现性元数据。[\[28\]](https://www.dolphindatabase.net/)

### 合成、改造与制造：从重复单元到规模化与质量控制

化学合成与自动化组装在“病原体荚膜多糖重复单元/糖疫苗相关结构”的精确定义材料制备上持续推进，例如自动化糖组装（AGA）用于拼装肺炎链球菌等重复单元框架，并可与酶促修饰联用完成更复杂结构的合成路线。[\[29\]](https://pubs.rsc.org/en/content/articlelanding/2020/ra/d0ra01803a)

同时，“化学改造‑表征‑活性”仍是多糖材料提高功能与拓展应用的主航道之一。针对多糖结构改造（含方法与活性影响）的综述指出结构‑活性与改造多糖将继续成为研究重点。[\[30\]](https://www.mdpi.com/1420-3049/28/14/5416)

研究空白（合成与改造）：  
可规模化获得“长度与分支可控、修饰位点可控、批间一致”的多糖仍然困难；在制造与质量控制上，缺少可对比的“结构指纹”（跨NMR/MS/色谱）与可监管的放行指标体系，进而限制临床与工业转化。[\[31\]](https://www.sciencedirect.com/science/article/pii/S1001841720305969)

### 材料与生物医用：多糖水凝胶与组织修复

多糖基水凝胶在创面修复、组织工程、药物递送等应用中持续活跃。多篇综述从结构功能化、宏观构筑、以及组织修复和异物反应缓解等角度总结了多糖水凝胶的设计与局限。[\[32\]](https://www.sciencedirect.com/science/article/pii/S0144861721013394)

研究空白（材料）：  
材料性能（力学、降解、黏附、释药）与多糖微结构之间的定量映射仍不足，尤其缺少跨实验室可比的结构表征与材料性能数据集；这使得“数据驱动材料设计”在多糖领域落后于一些合成高分子/小分子药物的材料信息学进展。[\[33\]](https://www.sciencedirect.com/science/article/pii/S0144861721013394)

### 临床/药物与疫苗：糖缀合物与生物合成路线优化

多糖缀合疫苗仍是经典且持续迭代的临床转化方向。综述系统介绍了市场上多糖缀合疫苗、载体蛋白、偶联化学与质量控制要点；与此同时，合成生物学驱动的“多糖基糖缀合疫苗生物合成”也在近年得到综述，聚焦生产优化策略。[\[34\]](https://www.sciencedirect.com/science/article/pii/S1001841720305969)

研究空白（临床/药物）：  
瓶颈集中在规模化生产与一致性、复杂结构的精准表征与放行、以及免疫原性与安全性评价的标准化；这些问题对数据标准与可复现流程提出更高要求。[\[34\]](https://www.sciencedirect.com/science/article/pii/S1001841720305969)

## 机器学习在多糖领域的应用现状与方法谱系

### 表示学习：从“序列/树/图”到“3D/谱图/多模态”

糖链（及多糖子结构）天然是分支结构，图表示更贴近化学本体。SweetNet使用图卷积神经网络学习糖链表示，并在多类任务上展示优于基线的预测性能，同时提供开源代码，成为“图表示学习+糖科学”的里程碑之一。[\[35\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161)

语言模型路线则尝试把分支结构编码进“序列化语言”。glyBERT提出用注意力机制建模糖链全局与局部上下文（并有代码仓库），而SweetBERT在2025 ICLR提出面向IUPAC糖序列的BERT式编码并显式纳入分支信息，反映了社区在“糖语言建模”上的持续探索。[\[36\]](https://www.biorxiv.org/content/10.1101/2021.10.15.464532v1.full.pdf)

从实验数据直接学习方面，CandyCrunch（Nature Methods 2024）以深度学习从LC‑MS/MS预测糖结构，基于大规模标注谱图训练并报告约90% top‑1准确率，同时开放代码与推理管线，代表了“谱图→结构”端到端学习的标志性进展。[\[37\]](https://www.nature.com/articles/s41592-024-02314-6.pdf)

面向基准与可比性，GlycanML与GlycoGym等工作提出多任务、多表示结构（序列与图）或跨域监督任务的基准套件，为后续方法迭代提供了更清晰的对照系。[\[38\]](https://arxiv.org/html/2405.16206v1)

需要强调：上述方法多以“glycan”（常见为寡糖/糖蛋白糖链）为对象；真正长链多糖还涉及分子量分布、重复单元统计结构、样品批次差异等额外维度。DoLPHiN与PolySac3DB等资源的出现，使得把机器学习更直接落到“多糖结构‑功能/3D构象”成为可能，但相对糖链领域仍属于早期阶段。[\[39\]](https://www.sciencedirect.com/science/article/pii/S0308814625037860)

### 代表性工作与可复现性对比表

| 工作/工具 | 输入数据与表示 | 任务类型 | 报告性能/指标（示例） | 数据集来源与规模线索 | 可复现性与局限 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| SweetNet（Burkholz et al., 2021） | 糖链图结构（分支图） | 分类/回归（糖链属性等） | 论文称在报告任务上优于对照方法 | 代码仓库提供训练与模型资源 | 代码开源（MIT）；更偏glycan任务，未显式处理长链多糖分子量分布等[\[35\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161) |
| glyBERT（bioRxiv） | 分支“语言”+注意力模型 | 表示学习/下游预测 | 以注意力学习全局/局部结构语义 | 代码仓库可用 | 预印本性质；任务与数据仍偏glycan；对多糖“重复单元统计性”需扩展[\[40\]](https://www.biorxiv.org/content/10.1101/2021.10.15.464532v1.full.pdf) |
| CandyCrunch（Nature Methods 2024） | LC‑MS/MS谱图 → 深度网络 | 结构预测/注释自动化 | 报告约90% top‑1准确率；训练集约50万谱图（论文摘要与报道线索） | 大规模标注谱图集合 | 代码开源；主要针对糖链MS注释，迁移到多糖需解决更高复杂度与标注稀缺[\[37\]](https://www.nature.com/articles/s41592-024-02314-6.pdf) |
| GlycanML（arXiv 2024） | 序列与图两类表示 | 多任务基准 | 给出多模型baseline与任务设置 | 作为基准套件整合 | 促进可比性；但任务仍以glycan场景为主[\[41\]](https://arxiv.org/html/2405.16206v1) |
| GlycoGym（MLSB 2025） | 多任务、多域监督任务集合 | 基准评测 | 六类监督任务（含MS碎裂预测等） | 会议论文提供套件描述 | 推动基准化；对多糖方向可借鉴其任务设计框架[\[42\]](https://www.mlsb.io/papers_2025/132.pdf) |
| glycowork（工具与数据集） | IUPAC等糖序列、绑定数据、标签数据 | 数据处理+模型接口 | 提供约50,500糖序列与多类标签、\>79万蛋白‑糖结合数据，并包含SweetNet等模型接口 | 官方文档给出数据与模型概览 | 强工程可用性；对多糖需补充长链结构、分子量与功能/材料数据[\[43\]](https://bojarlab.github.io/glycowork/) |
| 多糖产率预测（工业/生物过程建模示例） | 工艺参数/酶参数等结构化特征 | 回归/可解释建模 | 提出ML框架用于产率预测与参数优化 | 工程场景数据集（论文） | 显示“多糖制造过程数据”可作为ML切入点；但与“结构‑功能”不同模态，需要桥接[\[44\]](https://www.sciencedirect.com/science/article/pii/S2666498423000868) |

### 关键局限与“多糖特有”方法缺口

多糖机器学习的瓶颈通常不是模型容量，而是数据与表示：  
其一，结构表示存在多标准并存、跨库不一致的问题，尽管GlycoCT/WURCS与格式转换工具已在改善现状，但多糖“重复单元 \+ 统计连接 \+ 分子量分布”仍缺乏主流表示与基准数据。[\[45\]](https://www.sciencedirect.com/science/article/pii/S0008621508001353)  
其二，高质量监督标签稀缺；DoLPHiN把结构要素与健康功能条目化是重要进展，但材料性能、临床证据等级、实验条件元数据仍不完整。[\[46\]](https://www.sciencedirect.com/science/article/pii/S0308814625037860)  
其三，多模态数据（MS/NMR/色谱/链接分析/3D）之间缺少统一对齐与联合推断框架，导致“谱图→结构→功能”的闭环尚未形成。[\[47\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685)

## 研究机会、数据与实验路线图、优先级评估与交付物

### 面向多糖的机器学习研究方向（至少五项，含风险与里程碑）

以下方向以“可落地”为原则，按数据可获得性（DoLPHiN/CSDB/PolySac3DB/CAZy/GlyGen等）、工程可实现性（现有开源工具链）与潜在影响力综合设计。每一方向都给出目标、数据、模型、指标、风险与缓解，并在后续甘特图中统一排期。

**方向A：基于图神经网络/Transformer的多糖结构‑功能多任务预测（DoLPHiN驱动）**  
研究目标：构建“多糖结构要素→健康功能/疾病关联/菌群调节”等多任务预测模型，形成可解释的构效规则与候选多糖筛选器，优先从DoLPHiN的5085条结构‑功能条目出发并与CSDB的结构/NMR信息补全结构细节。[\[48\]](https://www.dolphindatabase.net/)  
所需数据：DoLPHiN条目（单糖组成比例、分子量、糖苷键、是否有NMR信息、功能标签等）；必要时补充CSDB条目中的结构与NMR信号信息；为减少标签噪声，应保留来源DOI与实验类型元数据作为“证据权重”。[\[49\]](https://www.dolphindatabase.net/detail/32734)  
模型建议：图表示优先（多糖主链/侧链可抽象为有重复单元的层次图），可借鉴SweetNet对分支结构的GNN建模；同时并行训练“序列化表示（IUPAC/WURCS）+Transformer”作为对照。[\[50\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161)  
评估指标：分类任务用AUROC/AUPRC、宏平均F1；回归（如抗氧化强度等量化指标若可获得）用RMSE/MAE；重点增加“跨来源/跨物种”外推测试（leave‑one‑genus/leave‑one‑species‑out）。  
潜在风险：功能标签异质与偏倚（不同实验体系、剂量、纯度）；结构字段可能不完整或粒度不一致。  
缓解策略：做证据分级（in vitro/动物/临床）并在损失函数中加权；引入“不确定标签学习/噪声鲁棒学习”；输出可解释子结构（motif/链接）贡献以辅助人工复核。  
里程碑：M3完成ETL与结构表示；M6完成基线模型与可重复评测；M9形成可解释构效图谱；M12提交方法论文/公开基准子集。

**方向B：多模态端到端“谱图→结构”学习（面向多糖的MS+NMR+链接分析融合）**  
研究目标：把多糖结构解析从“专家多手段拼图”推进到“模型辅助的联合推断”，优先解决两个子任务：B1（MS/IM‑MS→连接方式/构型判别），B2（NMR/链接分析→结构片段约束），最终输出符合GlycoCT/WURCS的结构或重复单元描述。近年针对完整多糖MS表征的综述、IM‑MS在多糖连接/构型解析中的案例，以及连接分析库的出现，为建立训练/验证集提供了方法学基础。[\[51\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685)  
所需数据：公开MS数据（可从UniCarb‑DB获得谱图‑结构对照以训练谱图编码器，但需迁移学习到多糖）；多糖NMR谱图与结构对照（可从文献与CSDB/DoLPHiN标注“是否有NMR结构信息”条目起步）；链接分析GC‑MS数据与衍生物库（用于连接方式标签）。[\[52\]](https://unicarb-db.expasy.org/)  
模型建议：谱图编码器可参考CandyCrunch“从LC‑MS/MS直接预测结构”的端到端思路；在多糖场景可采用“多模态Transformer/对比学习”把MS与NMR嵌入对齐，再用结构解码器（图生成/约束搜索）输出候选结构集合而非单一答案。[\[53\]](https://www.nature.com/articles/s41592-024-02314-6.pdf)  
评估指标：top‑k准确率、结构编辑距离、关键键型识别准确率（linkage‑level accuracy），以及“人机协同节省时间”指标（单位样品解析工时）。  
风险：公开“多糖谱图‑结构对照”数据量不足；跨仪器/条件域偏移严重。  
缓解：迁移学习（先用糖链大谱库预训练谱图编码器，如CandyCrunch路线），再用少量高质量多糖对照数据微调；域自适应/仪器条件作为条件输入。  
里程碑：M6完成多模态数据规范与小规模对照集；M9完成B1/B2子模型；M15完成联合解码与专家盲测评估；M18投稿谱图解析/计算糖科学方向论文。

**方向C：带“可合成/可改造约束”的生成模型设计新多糖（生成式材料/药用多糖发现）**  
研究目标：在结构‑功能预测模型基础上，用生成模型提出满足目标性质（免疫调节、抗病毒、黏弹性、凝胶强度等）的候选多糖结构/重复单元，并将“可实现性”作为硬约束：例如引入CAZy提供的酶家族信息作为生物合成可行性先验，或把常见改造反应（硫酸化/羧甲基化等）作为离散操作。CAZy作为糖苷键形成/改造/降解酶家族库，为把“生物可达结构空间”引入生成提供了抓手。[\[54\]](https://www.cazy.org/)  
所需数据：结构语料（GlyTouCan/CSDB/DoLPHiN）；功能标签（DoLPHiN与文献）；生物合成/改造规则（CAZy家族‑反应类型映射需自行整理）。[\[55\]](https://glytoucan.org/)  
模型建议：条件生成（graph diffusion/graph VAE/constraint‑based generation）；约束可通过KG规则或强化学习奖励实现。  
评估指标：有效性（化学/表示合法率）、新颖性、多样性、目标性质预测分数、可合成/可改造可行性评分（基于规则或酶覆盖度）。  
风险：生成结构“看起来好”但不可合成或生物不可达；目标性质模型本身偏差导致“奖赏黑客”。  
缓解：双重过滤（性质预测+合成可行性+专家规则）；加入不确定性与反事实评估；小规模实验闭环验证。  
里程碑：M9完成结构合法性与约束体系；M12形成候选库与体外筛选优先级；M18完成至少1–2个候选的实验验证与专利草案。

**方向D：多源融合多糖知识图谱（KG）用于功能挖掘、证据追踪与可解释推理**  
研究目标：构建“多糖实体‑结构要素‑来源物种‑实验表征证据‑功能/疾病‑相关酶/生物途径”的多糖KG，支持（1）可解释检索与证据链追踪，（2）基于图的链接预测发现潜在功能，（3）为方向A/C提供结构与功能的高质量对齐。GlyGen已提供SPARQL端点并以三元组库方式组织糖科学数据，是构建下游KG的现实起点；DoLPHiN提供多糖结构‑功能条目；CSDB补充天然结构与NMR；GlyTouCan提供统一ID锚点。[\[56\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292)  
所需数据：GlyGen SPARQL导出；GlyTouCan结构与ID；DoLPHiN条目；CSDB结构与NMR信息；必要时对接PDB糖链3D与验证工具数据。[\[57\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292)  
模型建议：图谱构建用RDF/Property Graph双栈；推理用可解释规则（SHACL/本体规则）+ 图表示学习（KG embeddings, GNN）；映射ETL可参考RML类工具的做法（如morph‑kgc）。[\[58\]](https://github.com/morph-kgc/morph-kgc)  
评估指标：实体对齐准确率、覆盖率、证据可追溯性（provenance completeness）、链接预测Hits@k/MRR，以及面向具体问题的检索/问答成功率。  
风险：跨库ID与表示不一致；许可条款不同导致共享受限。  
缓解：统一到WURCS或canonical IUPAC（可借助格式转换）；对每个来源保留原始字段与许可元数据；公开发布时提供“可复现构建脚本 \+ 可公开子集”。[\[59\]](https://api.glycosmos.org/glycanformatconverter/)  
里程碑：M3完成数据模式与本体草案；M6完成第一版KG与SPARQL/图数据库接口；M12开放可下载子集与演示应用；M18完成KG驱动的新功能假设验证。

**方向E：主动学习与小样本学习，构建“计算‑实验闭环”应对数据稀缺与实验昂贵**  
研究目标：把多糖研究常见的高成本步骤（提取‑纯化‑表征‑功能测定）纳入主动学习闭环，优先用于两类场景：E1 功能性多糖筛选（方向A/C的候选验证），E2 工艺/产率优化（如已有研究用ML预测多糖产率并寻找最优参数组合）。[\[60\]](https://www.sciencedirect.com/science/article/pii/S2666498423000868)  
所需数据：历史实验记录（包含提取工艺参数、原料信息、产率/纯度、表征摘要与功能测定）；可从公开论文/自建实验逐步累积。  
模型建议：贝叶斯优化/不确定性估计（deep ensembles/MC dropout）+ 小样本学习（meta‑learning/原型网络）+ 代价敏感主动学习。  
评估指标：单位实验成本下的性能提升（learning efficiency）、达到目标性能所需实验次数、候选命中率。  
风险：实验噪声与批次差异掩盖真实规律；闭环系统工程复杂。  
缓解：严格记录元数据与批次；采用层次模型区分“实验室/批次随机效应”；从单一体系（如同一类多糖水凝胶或同一类健康功能测定）开始。[\[61\]](https://www.sciencedirect.com/science/article/pii/S0144861721013394)  
里程碑：M6完成闭环原型（模拟+小规模真实实验）；M12在一个垂直体系内证明可节省实验；M18扩展到第二个体系并形成方法论文。

**方向F：面向多糖/糖链的自监督“基础模型”与跨任务迁移（结构语料+工具链支撑）**  
研究目标：利用GlyTouCan等提供的海量结构语料进行自监督预训练（masked modeling/对比学习），学习可迁移的结构表征，再微调到多糖任务（方向A/B/C/D）。glycowork提供较大规模糖序列与标签数据概览，并集成SweetNet等模型接口，为快速迭代提供工程底座。[\[62\]](https://glytoucan.org/)  
所需数据：GlyTouCan结构语料；统一到WURCS或canonical IUPAC（可借助格式转换与新近提出的自动命名转换框架）；必要时引入CSDB/DoLPHiN的高质量标签做微调。[\[63\]](https://api.glycosmos.org/glycanformatconverter/)  
模型建议：图对比学习（GNN）与分支语法Transformer并行；加入“重复单元/统计连接”的专用token或层次结构编码。  
评估指标：下游任务平均迁移收益、少样本性能、表示对结构相似性的保序性（如结构编辑距离相关）。  
风险：预训练语料偏向糖蛋白糖链导致偏移；多糖特征（分子量/分布）不在语料中。  
缓解：在预训练中引入“合成的聚合/重复单元增强”；与DoLPHiN等多糖标签联合多任务预训练。  
里程碑：M9完成预训练与公开权重；M12实现2–3个下游任务显著提升；M18形成“多糖基础模型+基准”论文与开源发布。

### 数据与实验路线图

**数据获取与ETL（建议优先级由高到低）**：  
优先抓取/下载DoLPHiN（结构‑功能监督标签最直接）与CSDB（天然结构与NMR信息）、并以GlyTouCan作为统一结构ID锚点；同时接入GlyGen SPARQL作为跨库实体与注释的骨架层；谱图类任务则引入UniCarb‑DB与公开MS工具链；三维结构方面以PolySac3DB及PDB糖链工具（GLYCAM‑Web/Privateer等）构建小而精的3D集合。[\[64\]](https://www.dolphindatabase.net/)

**预处理与标准化**：  
将多源结构统一到一种“训练主表示”（建议WURCS或canonical IUPAC），保留原始表示作为可追溯字段；使用GlycanFormatConverter进行格式互转与ID检索；对可视化与人工审核采用SNFG规范。[\[65\]](https://api.glycosmos.org/glycanformatconverter/)

**标注与增强策略**：  
对功能标签做证据分级与噪声建模（in vitro/动物/临床）；结构增强可用“子结构motif抽取”“重复单元扩展/缩短”“随机遮蔽链接/修饰”进行自监督增强；谱图任务可做峰位抖动、强度归一化、以及条件（仪器/碎裂方式）作为domain token输入。CandyCrunch路线表明大规模谱图与深度模型结合能显著提高结构注释自动化程度，可借鉴其训推一体化思路。[\[66\]](https://www.nature.com/articles/s41592-024-02314-6.pdf)

**开源工具与Python生态建议（按模块）**：  
结构与格式：glypy（读写与操作糖结构，含与数据库交互线索）、GlycanFormatConverter（API/核心库）、glycowork（清洗与画糖、数据与模型接口）。[\[67\]](https://glypy.readthedocs.io/en/latest/index.html)  
知识图谱：RDFLib、SPARQL客户端（对接GlyGen SPARQL）、以及RML映射工具链思想（morph‑kgc）。[\[21\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292)  
模型训练：PyTorch/torch‑geometric（GNN）、Transformers生态；谱图可结合pyOpenMS等（此处属常用工具建议，需按实际数据格式选型）。  
可视化：SNFG符号体系可通过相关工具或库生成（标准依据SNFG指南）。[\[68\]](https://academic.oup.com/glycob/article/29/9/620/5513705)

**计算资源估算（经验型、需按数据规模调整）**：  
方向A/D的GNN/多任务模型：单卡GPU即可完成原型（中小规模）；方向B/F涉及大规模谱图或预训练时可能需要多GPU与更高存储吞吐（CandyCrunch基于大规模谱图训练的经验表明，数据规模上来后训练成本显著上升）。[\[69\]](https://www.nature.com/articles/s41592-024-02314-6.pdf)

**可复现性与共享建议**：  
为每个数据源保留“原始下载时间/版本/许可声明/字段映射”；发布时优先提供（1）可公开的派生子集，（2）全流程ETL脚本与哈希校验，（3）模型权重与推理脚本，（4）KG的RDF dump与SPARQL示例查询，并在文档中清晰区分“原始数据许可”与“派生数据/模型许可”。GlyGen明确提供SPARQL端点与CC‑BY‑4.0信息，有利于下游再利用与复现。[\[70\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292)

### 统一排期甘特图（18个月示例）

gantt  
  title 多糖机器学习研究计划（示例：18个月）  
  dateFormat  YYYY-MM-DD  
  axisFormat  %m

  section 数据与标准化  
  数据源盘点与许可核查           :a1, 2026-04-01, 60d  
  ETL与结构表示统一（WURCS/IUPAC） :a2, after a1, 90d  
  初版多糖KG（GlyGen+DoLPHiN+CSDB）:a3, after a2, 90d

  section 方向A 结构-功能预测  
  基线模型与评测（GNN/Transformer） :b1, 2026-06-15, 120d  
  可解释构效分析与外推验证          :b2, after b1, 120d

  section 方向B 谱图→结构多模态  
  小规模多模态对照集构建            :c1, 2026-07-01, 120d  
  多模态编码器与结构解码器原型      :c2, after c1, 150d

  section 方向D 知识图谱挖掘  
  KG查询/推理与链接预测              :d1, 2026-09-01, 150d

  section 方向E 主动学习闭环  
  闭环原型（模拟+小规模实验）        :e1, 2026-10-01, 180d

  section 方向F 基础模型预训练  
  自监督预训练与迁移评测              :f1, 2026-10-15, 210d

  section 交付与发布  
  开源数据子集+代码v1                :z1, 2027-01-15, 60d  
  论文投稿（方法+资源）               :z2, 2027-03-01, 90d

### 方向优先级与可行性评分（建议顺序）

评分维度：影响力（对领域贡献/可推广性）、可行性（数据与工程难度）、资源需求（算力/实验成本，分数越高表示越省资源）、时间成本（分数越高表示越快）。总分为加权示例（影响力40%+可行性30%+资源需求15%+时间成本15%），可按团队实际调整。

| 方向 | 影响力 | 可行性 | 资源需求（高=省） | 时间成本（高=快） | 加权总分 | 推荐顺序 |
| :---- | ----: | ----: | ----: | ----: | ----: | :---- |
| A 结构‑功能多任务预测（DoLPHiN驱动） | 5 | 4 | 4 | 4 | 4.45 | 1 |
| D 多源融合多糖KG（含证据链） | 4 | 4 | 3 | 3 | 3.75 | 2 |
| B 多模态谱图→结构端到端学习 | 5 | 3 | 2 | 2 | 3.55 | 3 |
| E 主动学习/小样本闭环 | 4 | 3 | 2 | 2 | 3.10 | 4 |
| F 多糖/糖链基础模型预训练 | 4 | 3 | 2 | 2 | 3.10 | 5 |
| C 生成模型设计新多糖（带可行性约束） | 5 | 2 | 2 | 2 | 3.05 | 6 |

解释：  
A之所以优先，是因为DoLPHiN提供相对稀缺的“结构‑功能条目化监督信号”，可快速形成可评测的基线并产出可解释结论；D有助于系统性解决跨库融合与证据追踪，是后续B/C/F的底座；B/C/F虽影响潜力大，但受高质量对照数据与算力/工程复杂度制约，建议在A/D产出高质量结构表示与对齐后并行推进。[\[71\]](https://www.dolphindatabase.net/)

### 交付物清单与时间节点（建议）

在18个月节奏下，建议把交付物拆为“资源型（数据/KG/工具）”与“方法型（模型/论文/专利）”两条主线：

* 第6个月：发布可公开数据子集v0（DoLPHiN衍生特征与匿名化证据字段、结构标准化脚本）、多糖结构表示规范文档（WURCS/IUPAC主表示与字段映射）、以及KG schema草案（RDF/属性图双栈）。[\[72\]](https://www.dolphindatabase.net/)

* 第12个月：提交/发布（1）方向A论文（多糖结构‑功能多任务预测+可解释构效）、（2）多糖KG v1（含SPARQL示例查询与证据追踪Demo）、（3）基准评测脚本（参考GlycanML/GlycoGym的任务化思路进行多糖版本改造）。[\[73\]](https://arxiv.org/html/2405.16206v1)

* 第18个月：提交/发布（1）方向B论文（多模态谱图→结构推断；对比CandyCrunch路线并给出多糖迁移策略）、（2）生成候选多糖的可行性报告与1项专利草案（若实验验证到位）、（3）开源工具包v1（ETL+训练+推理+KG构建一体化）。[\[74\]](https://www.nature.com/articles/s41592-024-02314-6.pdf)

### 可下载/可访问的关键资源链接清单（便于后续落地）

说明：根据平台限制，链接以代码块形式给出（便于复制）；具体许可条款请在使用前逐一核对各站点声明。

GlyTouCan（糖链注册库）:  
https://glytoucan.org/  
GlyTouCan v3.0 (NAR)：  
https://academic.oup.com/nar/article/49/D1/D1529/5943821

GlyGen（集成知识库 \+ SPARQL端点）:  
https://www.glygen.org/  
GlyGen数据模型论文（含SPARQL端点说明）:  
https://academic.oup.com/bioinformatics/article/36/12/3941/5824292

UniCarb-DB（人工注释MS/MS谱图库）:  
https://unicarb-db.expasy.org/  
UniCarb-DB协议/方法章节（Springer）:  
https://link.springer.com/protocol/10.1007/978-1-0716-4007-4\_6

CSDB（天然糖结构，含NMR/分类学等）:  
https://csdb.glycoscience.ru/database/index.html

DoLPHiN（天然多糖结构-健康功能数据库，Food Chemistry 2025）:  
https://www.dolphindatabase.net/  
DoLPHiN论文（ScienceDirect）:  
https://www.sciencedirect.com/science/article/pii/S0308814625037860

PolySac3DB（多糖3D结构）:  
https://polysac3db.cermav.cnrs.fr/

CAZy（碳水化合物活性酶家族库）:  
https://www.cazy.org/

GlycanFormatConverter API（格式转换与ID检索）:  
https://api.glycosmos.org/glycanformatconverter/

SNFG指南更新（Glycobiology 2019）:  
https://academic.oup.com/glycob/article/29/9/620/5513705  
NCBI SNFG符号文件（含SVG链接索引）:  
https://www.ncbi.nlm.nih.gov/glycans/snfg-table1.tsv

SweetNet（GNN糖链表示学习）:  
https://www.cell.com/cell-reports/fulltext/S2211-1247(21)00616-1  
https://github.com/BojarLab/SweetNet

CandyCrunch（LC-MS/MS → 糖结构；Nature Methods 2024）:  
https://www.nature.com/articles/s41592-024-02314-6  
https://github.com/BojarLab/CandyCrunch

### 视觉示意：多糖机器学习端到端管线（示意图）

flowchart LR  
  A\[数据层\<br/\>DoLPHiN/CSDB/GlyTouCan/GlyGen/CAZy/UniCarb-DB/PDB\] \--\> B\[标准化与对齐\<br/\>WURCS/IUPAC/GlycoCT \+ ID映射\]  
  B \--\> C\[多糖表示学习\<br/\>GNN/Transformer/3D/谱图编码器\]  
  C \--\> D\[任务层\]  
  D \--\> D1\[结构-功能预测\<br/\>多任务学习\]  
  D \--\> D2\[谱图→结构推断\<br/\>多模态\]  
  D \--\> D3\[生成设计\<br/\>约束生成\]  
  D \--\> D4\[KG推理与发现\<br/\>证据链追踪\]  
  D \--\> E\[实验验证与反馈\<br/\>主动学习闭环\]  
  E \--\> A

---

[\[1\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821) [\[3\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821) [\[7\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821) [\[8\]](https://academic.oup.com/nar/article/49/D1/D1529/5943821) https://academic.oup.com/nar/article/49/D1/D1529/5943821

[https://academic.oup.com/nar/article/49/D1/D1529/5943821](https://academic.oup.com/nar/article/49/D1/D1529/5943821)

[\[2\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161) [\[6\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161) [\[35\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161) [\[50\]](https://www.sciencedirect.com/science/article/pii/S2211124721006161) https://www.sciencedirect.com/science/article/pii/S2211124721006161

[https://www.sciencedirect.com/science/article/pii/S2211124721006161](https://www.sciencedirect.com/science/article/pii/S2211124721006161)

[\[4\]](https://www.mdpi.com/2072-6643/14/19/4116) [\[26\]](https://www.mdpi.com/2072-6643/14/19/4116) https://www.mdpi.com/2072-6643/14/19/4116

[https://www.mdpi.com/2072-6643/14/19/4116](https://www.mdpi.com/2072-6643/14/19/4116)

[\[5\]](https://www.cazy.org/) [\[18\]](https://www.cazy.org/) [\[54\]](https://www.cazy.org/) https://www.cazy.org/

[https://www.cazy.org/](https://www.cazy.org/)

[\[9\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292) [\[21\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292) [\[56\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292) [\[57\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292) [\[70\]](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292) https://academic.oup.com/bioinformatics/article/36/12/3941/5824292

[https://academic.oup.com/bioinformatics/article/36/12/3941/5824292](https://academic.oup.com/bioinformatics/article/36/12/3941/5824292)

[\[10\]](https://glycosmos.org/) https://glycosmos.org/

[https://glycosmos.org/](https://glycosmos.org/)

[\[11\]](https://unicarb-db.expasy.org/) [\[52\]](https://unicarb-db.expasy.org/) https://unicarb-db.expasy.org/

[https://unicarb-db.expasy.org/](https://unicarb-db.expasy.org/)

[\[12\]](https://csdb.glycoscience.ru/database/) https://csdb.glycoscience.ru/database/

[https://csdb.glycoscience.ru/database/](https://csdb.glycoscience.ru/database/)

[\[13\]](https://cordis.europa.eu/project/id/BIO2930001) https://cordis.europa.eu/project/id/BIO2930001

[https://cordis.europa.eu/project/id/BIO2930001](https://cordis.europa.eu/project/id/BIO2930001)

[\[14\]](https://www.glycome-db.org/) https://www.glycome-db.org/

[https://www.glycome-db.org/](https://www.glycome-db.org/)

[\[15\]](https://glycam.org/portal/gf_home/) https://glycam.org/portal/gf\_home/

[https://glycam.org/portal/gf\_home/](https://glycam.org/portal/gf_home/)

[\[16\]](https://polysac3db.cermav.cnrs.fr/) https://polysac3db.cermav.cnrs.fr/

[https://polysac3db.cermav.cnrs.fr/](https://polysac3db.cermav.cnrs.fr/)

[\[17\]](https://www.sciencedirect.com/science/article/pii/S0308814625037860) [\[39\]](https://www.sciencedirect.com/science/article/pii/S0308814625037860) [\[46\]](https://www.sciencedirect.com/science/article/pii/S0308814625037860) https://www.sciencedirect.com/science/article/pii/S0308814625037860

[https://www.sciencedirect.com/science/article/pii/S0308814625037860](https://www.sciencedirect.com/science/article/pii/S0308814625037860)

[\[19\]](https://www.sciencedirect.com/science/article/pii/S0008621508001353) [\[45\]](https://www.sciencedirect.com/science/article/pii/S0008621508001353) https://www.sciencedirect.com/science/article/pii/S0008621508001353

[https://www.sciencedirect.com/science/article/pii/S0008621508001353](https://www.sciencedirect.com/science/article/pii/S0008621508001353)

[\[20\]](https://api.glycosmos.org/glycanformatconverter/) [\[59\]](https://api.glycosmos.org/glycanformatconverter/) [\[63\]](https://api.glycosmos.org/glycanformatconverter/) [\[65\]](https://api.glycosmos.org/glycanformatconverter/) https://api.glycosmos.org/glycanformatconverter/

[https://api.glycosmos.org/glycanformatconverter/](https://api.glycosmos.org/glycanformatconverter/)

[\[22\]](https://www.sciencedirect.com/science/article/pii/S0963996921001897) https://www.sciencedirect.com/science/article/pii/S0963996921001897

[https://www.sciencedirect.com/science/article/pii/S0963996921001897](https://www.sciencedirect.com/science/article/pii/S0963996921001897)

[\[23\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685) [\[25\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685) [\[47\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685) [\[51\]](https://www.sciencedirect.com/science/article/pii/S0144861725005685) https://www.sciencedirect.com/science/article/pii/S0144861725005685

[https://www.sciencedirect.com/science/article/pii/S0144861725005685](https://www.sciencedirect.com/science/article/pii/S0144861725005685)

[\[24\]](https://www.sciencedirect.com/science/article/pii/S0144861725006150) https://www.sciencedirect.com/science/article/pii/S0144861725006150

[https://www.sciencedirect.com/science/article/pii/S0144861725006150](https://www.sciencedirect.com/science/article/pii/S0144861725006150)

[\[27\]](https://www.sciencedirect.com/science/article/pii/S2213453021000483) https://www.sciencedirect.com/science/article/pii/S2213453021000483

[https://www.sciencedirect.com/science/article/pii/S2213453021000483](https://www.sciencedirect.com/science/article/pii/S2213453021000483)

[\[28\]](https://www.dolphindatabase.net/) [\[48\]](https://www.dolphindatabase.net/) [\[64\]](https://www.dolphindatabase.net/) [\[71\]](https://www.dolphindatabase.net/) [\[72\]](https://www.dolphindatabase.net/) https://www.dolphindatabase.net/

[https://www.dolphindatabase.net/](https://www.dolphindatabase.net/)

[\[29\]](https://pubs.rsc.org/en/content/articlelanding/2020/ra/d0ra01803a) https://pubs.rsc.org/en/content/articlelanding/2020/ra/d0ra01803a

[https://pubs.rsc.org/en/content/articlelanding/2020/ra/d0ra01803a](https://pubs.rsc.org/en/content/articlelanding/2020/ra/d0ra01803a)

[\[30\]](https://www.mdpi.com/1420-3049/28/14/5416) https://www.mdpi.com/1420-3049/28/14/5416

[https://www.mdpi.com/1420-3049/28/14/5416](https://www.mdpi.com/1420-3049/28/14/5416)

[\[31\]](https://www.sciencedirect.com/science/article/pii/S1001841720305969) [\[34\]](https://www.sciencedirect.com/science/article/pii/S1001841720305969) https://www.sciencedirect.com/science/article/pii/S1001841720305969

[https://www.sciencedirect.com/science/article/pii/S1001841720305969](https://www.sciencedirect.com/science/article/pii/S1001841720305969)

[\[32\]](https://www.sciencedirect.com/science/article/pii/S0144861721013394) [\[33\]](https://www.sciencedirect.com/science/article/pii/S0144861721013394) [\[61\]](https://www.sciencedirect.com/science/article/pii/S0144861721013394) https://www.sciencedirect.com/science/article/pii/S0144861721013394

[https://www.sciencedirect.com/science/article/pii/S0144861721013394](https://www.sciencedirect.com/science/article/pii/S0144861721013394)

[\[36\]](https://www.biorxiv.org/content/10.1101/2021.10.15.464532v1.full.pdf) [\[40\]](https://www.biorxiv.org/content/10.1101/2021.10.15.464532v1.full.pdf) https://www.biorxiv.org/content/10.1101/2021.10.15.464532v1.full.pdf

[https://www.biorxiv.org/content/10.1101/2021.10.15.464532v1.full.pdf](https://www.biorxiv.org/content/10.1101/2021.10.15.464532v1.full.pdf)

[\[37\]](https://www.nature.com/articles/s41592-024-02314-6.pdf) [\[53\]](https://www.nature.com/articles/s41592-024-02314-6.pdf) [\[66\]](https://www.nature.com/articles/s41592-024-02314-6.pdf) [\[69\]](https://www.nature.com/articles/s41592-024-02314-6.pdf) [\[74\]](https://www.nature.com/articles/s41592-024-02314-6.pdf) https://www.nature.com/articles/s41592-024-02314-6.pdf

[https://www.nature.com/articles/s41592-024-02314-6.pdf](https://www.nature.com/articles/s41592-024-02314-6.pdf)

[\[38\]](https://arxiv.org/html/2405.16206v1) [\[41\]](https://arxiv.org/html/2405.16206v1) [\[73\]](https://arxiv.org/html/2405.16206v1) https://arxiv.org/html/2405.16206v1

[https://arxiv.org/html/2405.16206v1](https://arxiv.org/html/2405.16206v1)

[\[42\]](https://www.mlsb.io/papers_2025/132.pdf) https://www.mlsb.io/papers\_2025/132.pdf

[https://www.mlsb.io/papers\_2025/132.pdf](https://www.mlsb.io/papers_2025/132.pdf)

[\[43\]](https://bojarlab.github.io/glycowork/) https://bojarlab.github.io/glycowork/

[https://bojarlab.github.io/glycowork/](https://bojarlab.github.io/glycowork/)

[\[44\]](https://www.sciencedirect.com/science/article/pii/S2666498423000868) [\[60\]](https://www.sciencedirect.com/science/article/pii/S2666498423000868) https://www.sciencedirect.com/science/article/pii/S2666498423000868

[https://www.sciencedirect.com/science/article/pii/S2666498423000868](https://www.sciencedirect.com/science/article/pii/S2666498423000868)

[\[49\]](https://www.dolphindatabase.net/detail/32734) https://www.dolphindatabase.net/detail/32734

[https://www.dolphindatabase.net/detail/32734](https://www.dolphindatabase.net/detail/32734)

[\[55\]](https://glytoucan.org/) [\[62\]](https://glytoucan.org/) https://glytoucan.org/

[https://glytoucan.org/](https://glytoucan.org/)

[\[58\]](https://github.com/morph-kgc/morph-kgc) https://github.com/morph-kgc/morph-kgc

[https://github.com/morph-kgc/morph-kgc](https://github.com/morph-kgc/morph-kgc)

[\[67\]](https://glypy.readthedocs.io/en/latest/index.html) https://glypy.readthedocs.io/en/latest/index.html

[https://glypy.readthedocs.io/en/latest/index.html](https://glypy.readthedocs.io/en/latest/index.html)

[\[68\]](https://academic.oup.com/glycob/article/29/9/620/5513705) https://academic.oup.com/glycob/article/29/9/620/5513705

[https://academic.oup.com/glycob/article/29/9/620/5513705](https://academic.oup.com/glycob/article/29/9/620/5513705)