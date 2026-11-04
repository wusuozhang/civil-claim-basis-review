# 请求权基础规则库索引

## 1. 运行定位

本目录是 Skill 的公开运行时知识库。完成普通民事案件的请求权预选、要件拆解、抗辩检索、证据映射和诉请组合时，不依赖任何外部教材、整书 OCR 或用户本机私有书库。

规则卡提供“检索起点”，不替代逐案现行法核验。每张规则卡使用稳定 `rule_id`；案件中的 `basis_id` 是该规则在具体 `claim_id` 下的实例，例如：

`CLAIM-03 → BASIS-03A → RB-CON-006`

不得把 `rule_id` 直接当作法条。建立 `basis_id` 前必须按 `direct-basis-gate.md` 写明经核验的合同条款或法律、行政法规、司法解释的条、款、项，并检查该条款能否直接推出本项请求。

## 2. 规则卡字段

每张规则卡至少包含：

- `rule_id`：公开规则库中的稳定编号。
- **目标效果**：该规则直接或经清算产生什么法律效果。
- **主体结构**：谁通常可以向谁主张。
- **规范锚点**：需要核验的民法典条文群、司法解释或特别法。
- **产生要件**：请求方原则上需要陈述并证明的事实。
- **主要防御**：未发生、消灭、行使受阻或范围限制。
- **法律效果**：履行、返还、赔偿、确认、形成或优先受偿等范围。
- **证据入口**：第一轮最值得找的材料。
- **竞合/边界**：与其他规则的排斥、择一、聚合或先后关系。

规则卡没有写出的特别要件不能视为不存在。出现消费者、劳动、公司、知识产权、建设工程、金融、数据、家事等领域信号时，按 `domain-special.md` 追加特别法检索。

## 3. 按目标法律效果检索

| 目标法律效果 | 优先规则 | 继续加载 |
|---|---|---|
| 要求按合同交付、付款、办证或完成工作 | RB-CON-004、RB-CON-005、对应典型合同卡 | `domain-contract-quasi.md` |
| 要求开票、移交资料、保密、协助或履行终止后义务 | RB-CON-014 | `domain-contract-quasi.md` |
| 对方拒绝受领、不协力或需要提存 | RB-CON-015、RB-REM-009 | `domain-contract-quasi.md`、`remedy-calculation.md` |
| 多数债务人、选择给付、债务加入或以物抵债 | RB-CON-016、RB-CON-017 | `transaction-history-and-multiparty.md`、`domain-contract-quasi.md` |
| 隐名交易、间接代理、委托人介入或第三人选择 | RB-CON-018、RB-CTY-011 | `transaction-history-and-multiparty.md`、`domain-contract-quasi.md` |
| 拒绝自己先履行、要求对方提供担保 | RB-CON-006、RB-CON-007 | `domain-contract-quasi.md` |
| 解除合同、确认解除或处理解除后返还 | RB-CON-010、RB-CON-011 | `domain-contract-quasi.md`、`remedy-calculation.md` |
| 赔偿违约损失、违约金、定金 | RB-CON-008、RB-CON-009、RB-REM-001 至 006 | `domain-contract-quasi.md`、`remedy-calculation.md` |
| 确认合同不成立、无效、撤销并返还 | RB-ACT-001 至 005、RB-RET-001 | `domain-contract-quasi.md` |
| 代位、撤销债务人处分、抵销 | RB-CRD-001 至 004 | `domain-security-creditor.md` |
| 要求返还房屋、车辆、设备或其他原物 | RB-PRO-004、RB-POS-001、RB-CON-011、RB-RET-002 | `domain-property-tort.md`、`domain-contract-quasi.md` |
| 排除妨害、消除危险、停止侵害 | RB-PRO-005、RB-POS-002、RB-TOR-002、RB-PER-001 | `domain-property-tort.md`、`domain-special.md` |
| 确认所有权、办理或更正登记 | RB-PRO-001 至 003、RB-PRO-006 | `domain-property-tort.md` |
| 共有物分割、优先购买、相邻妨害或业主决议 | RB-PRO-010、RB-PRO-011 | `domain-property-tort.md` |
| 添附装修、登记错误或异议损害 | RB-PRO-009、RB-PRO-012、RB-REM-010 | `domain-property-tort.md`、`remedy-calculation.md` |
| 主张善意取得或攻击无权处分 | RB-PRO-007、RB-PRO-008 | `domain-property-tort.md` |
| 无合同依据取得利益、替他人管理事务 | RB-RET-002、RB-RET-003 | `domain-contract-quasi.md` |
| 人身、财产、产品、网络、医疗等侵权赔偿 | RB-TOR-001 至 013 | `domain-property-tort.md`、`remedy-calculation.md` |
| 要求保证人、抵押人、出质人承担责任 | RB-SEC-001 至 008 | `domain-security-creditor.md` |
| 担保物价值减少、物上代位或共同担保追偿 | RB-SEC-009、RB-SEC-010 | `domain-security-creditor.md` |
| 主张夫妻共同债务、离婚财产、继承清偿 | RB-FAM-001 至 004、RB-INH-001 至 004 | `domain-special.md` |
| 名誉、隐私、个人信息等人格权救济 | RB-PER-001 至 004 | `domain-special.md` |
| 计算本金、利息、差价、费用或精神损害 | RB-REM-001 至 008 | `remedy-calculation.md` |
| 计算受领迟延费用、使用利益、孳息与返还清算 | RB-REM-009、RB-REM-010 | `remedy-calculation.md` |

典型合同信号还应从 RB-CTY-001 至 014 中选择最贴近的卡。融资租赁、保理、运输、保管仓储、物业、中介、行纪、合伙等不得仅用一般合同卡代替其特殊主体和风险规则。

## 4. 按争议节点补充检索

### 法律行为与代理

出现虚假意思、重大误解、欺诈、胁迫、显失公平、恶意串通、无权代理、表见代理时，先读取 `domain-contract-quasi.md` 的 RB-ACT 规则，再决定合同请求能否进入履行层。

### 物债区分

出现“一物二卖、未登记、已交付、代持、借名、无权处分、查封、租赁占有”时，必须分别建立：

1. 原因关系请求；
2. 物权是否变动；
3. 当前占有是否有权源；
4. 第三人的防御；
5. 不能取得原物时的返款和损害赔偿。

不得以“合同有效”直接推出请求人为所有权人。

### 交易历史与多主体

出现三方以上、代付代收、名义签约与实际履行分离、授权链、转租、多重处分或内部追偿时，加载 `transaction-history-and-multiparty.md`，同时绘制主体—授权、合同关系、物与资金流、诉请责任四张图。主体不同原则上另建 `claim_id`。

### 责任主体分离

出现员工、劳务、承揽人、监护人、网络平台、安全保障义务人、产品生产者/销售者、机动车使用人、医疗机构时，先找特殊责任主体卡，再决定是否回到一般侵权。不得只起诉直接行为人或者只引用一般过错责任。

### 金额与责任范围

任何金钱请求在实体成立之后仍须另过 `remedy-calculation.md`：项目、期间、基数、因果关系、可预见性、减损、与有过失、损益相抵、责任限额、重复受偿和证据。

## 5. 最小加载策略

- **单点问答**：读取本索引＋一个相关领域文件＋`current-law-gate.md`。
- **快速检视**：读取本索引、`claim-routing.md`、`element-defense.md`、相关领域文件和 `current-law-gate.md`。
- **完整检视**：在上述基础上加载 `fact-procedure.md`、`evidence-proof.md`、`remedy-calculation.md`、`strategy-output.md`。
- **规范鉴定**：完整检视同时加载 `academic-analysis-format.md`；出现解释、规范冲突或漏洞时加载 `norm-application.md`。
- **特别法案件**：先用本库完成总控，再加载专业 Skill 或官方特别法；不得因缺少外部教材而停止普通请求权检视。

## 6. 规则使用纪律

1. 先以用户目标选择规则卡，不按法典章节顺序机械穷举。
2. 一项诉请可以链接多个规则卡，但要说明并列、备位、前提或排斥关系。
3. 每张卡必须落到具体事实和证据；只复制规则卡不构成案件分析。
4. 规则卡与现行官方法源冲突时，以核验后的现行法为准，并记录需要修订的 `rule_id`。
5. 无法确认条号、版本或特别规则时保留规则方向，结论降级为“待核现行法/特别法”。
6. 不要求用户提供本库研究时使用过的教材，不因私有知识库不存在而降低为纯法条罗列。
7. 规则卡只负责召回和拆解。正式输出必须用中文区分直接请求权基础、辅助/构成规则、行为归属规则、金额/范围/计价规则、证明规则、抗辩/限制规则和程序规则，不得让规范锚点、证据规则或计价规则冒充直接请求权基础。
