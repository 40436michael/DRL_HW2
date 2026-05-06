

# 📌 Cliff Walking：Q-learning vs SARSA
對話紀錄放在 Cliff Walking 強化學習比較
## 一、實驗目的

本實驗比較兩種強化學習方法在 Cliff Walking 環境中的表現：

* Q-learning（Off-policy）
* SARSA（On-policy）

主要分析以下三個面向：

* 學習收斂速度
* 策略行為差異（冒險 vs 保守）
* 學習穩定性

---

## 二、實驗環境與設定

### 📍 Cliff Walking 環境

* Gridworld 大小：4 × 12
* 起點：左下角
* 終點：右下角
* 懸崖區：底部中間區域

### 🎯 Reward 設計

| 行為   | Reward     |
| ---- | ---------- |
| 每一步  | -1         |
| 掉入懸崖 | -100（回到起點） |
| 抵達終點 | 0          |

---

### ⚙️ 訓練參數

| 參數       | 數值      |
| -------- | ------- |
| 學習率 α    | 0.1     |
| 折扣因子 γ   | 0.9     |
| 探索率 ε    | 0.1     |
| Episodes | 500     |
| Runs     | 50（取平均） |

---

## 三、訓練過程

在實驗中：

* Q-learning 與 SARSA 使用相同環境
* 使用 **ε-greedy 策略**
* 保證探索條件一致（公平比較）
* 每回合紀錄 total reward
* 重複 50 次取平均結果

---

## 四、結果分析

---

## 1️⃣ 學習表現（Learning Curve）

輸出圖：
<img width="1000" height="600" alt="learning_curve" src="https://github.com/user-attachments/assets/0c89ccf1-e055-4c81-bad0-0a85f8dadd23" />

```
learning_curve.png
```

### 📊 觀察結果

* 初期 reward 非常低（頻繁掉入 cliff）
* 隨訓練逐漸改善並收斂
* 最終結果：

| 方法         | 表現             |
| ---------- | -------------- |
| SARSA      | reward 較高、較穩定  |
| Q-learning | reward 較低、波動較大 |

### 📌 收斂速度

* Q-learning：收斂較快
* SARSA：收斂較慢但穩定

---

## 2️⃣ 策略行為分析（Policy）

輸出圖：


<img width="1400" height="400" alt="q_policy" src="https://github.com/user-attachments/assets/8c82b5eb-c164-4d49-ac4c-29613a6c6199" />


<img width="1400" height="400" alt="sarsa_policy" src="https://github.com/user-attachments/assets/d0f1b863-c694-4a92-a58d-508827904884" />

```
q_policy.png
sarsa_policy.png
```

### 🧠 Q-learning 行為

* 傾向走最短路徑
* 經常貼近 cliff
* 高風險策略（容易掉落）

👉 特性：

* 冒險
* 追求最優解

---

### 🧠 SARSA 行為

* 明顯避開 cliff
* 路徑較安全但較長
* 穩定性較高

👉 特性：

* 保守
* 考慮探索風險

---

## 3️⃣ 穩定性分析

| 方法         | 穩定性 | 波動 |
| ---------- | --- | -- |
| Q-learning | 較差  | 高  |
| SARSA      | 較好  | 低  |

### 📌 原因分析

* Q-learning 假設未來永遠採取最佳行為
* SARSA 會考慮 ε-greedy 探索帶來的不確定性

👉 因此 SARSA 更貼近「實際行為」

---

## 五、理論比較與討論

### 🔵 Q-learning（Off-policy）

* 學習目標是「理論上的最佳策略」
* 更新時不考慮實際探索行為
* 收斂較快
* 但可能產生危險行為

---

### 🟢 SARSA（On-policy）

* 學習「實際執行的策略」
* 更新包含探索行為影響
* 收斂較穩定
* 更安全可靠

---

### 📌 Cliff Walking 的意義

此環境清楚展示：

* Off-policy vs On-policy 差異
* 風險敏感學習（risk-aware learning）
* 探索策略對結果的影響

---

## 六、結論

### 📊 實驗總結

| 項目   | Q-learning | SARSA |
| ---- | ---------- | ----- |
| 收斂速度 | 較快         | 較慢    |
| 穩定性  | 較差         | 較好    |
| 策略風險 | 高          | 低     |
| 路徑   | 最短但危險      | 較安全   |

---

### 📌 最終結論

* **收斂最快：Q-learning**
* **最穩定：SARSA**

---

### 📍 適用情境

#### Q-learning 適用於：

* 環境可安全探索
* 追求最優策略
* 模擬或理論問題

#### SARSA 適用於：

* 高風險環境
* 真實世界應用（例如機器人控制）
* 需要穩定行為

---

## 七、執行方式

```bash
python main.py
```

---

## 八、輸出結果

執行後會產生：

* learning_curve.png（學習曲線）
* q_policy.png（Q-learning 策略）
* sarsa_policy.png（SARSA 策略）

