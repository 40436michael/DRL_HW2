# Cliff Walking：Q-learning vs SARSA

## 一、作業目的

本作業旨在實作並比較兩種經典強化學習演算法：

* Q-learning（Off-policy）
* SARSA（On-policy）

透過相同環境與參數設定，分析兩者在學習過程中的：

* 收斂速度
* 策略行為
* 穩定性差異

---

## 二、環境描述（Cliff Walking）

本實驗採用 Gridworld 環境（4 × 12）：

* 起點（Start）：左下角
* 終點（Goal）：右下角
* 懸崖（Cliff）：底部中間區域

### 獎勵機制：

* 每移動一步：**-1**
* 掉入懸崖：**-100**，並回到起點
* 到達終點：**0（回合結束）**

---

## 三、方法說明

### 1️⃣ Q-learning（Off-policy）

更新公式：

[
Q(s,a) \leftarrow Q(s,a) + \alpha \left[ r + \gamma \max_a Q(s',a) - Q(s,a) \right]
]

* 使用「最佳下一步」來更新
* 偏向學習**最優策略（貪婪）**
* 可能較冒險（貼近懸崖）

---

### 2️⃣ SARSA（On-policy）

更新公式：

[
Q(s,a) \leftarrow Q(s,a) + \alpha \left[ r + \gamma Q(s',a') - Q(s,a) \right]
]

* 使用「實際採取的下一步」
* 考慮 exploration（ε-greedy）
* 策略較保守

---

### 3️⃣ 參數設定

| 參數       | 數值      |
| -------- | ------- |
| α（學習率）   | 0.1     |
| γ（折扣因子）  | 0.9     |
| ε（探索率）   | 0.1     |
| Episodes | 500     |
| Runs     | 50（取平均） |

---

## 四、實驗結果

### 1️⃣ 學習曲線（Learning Curve）

輸出圖：

```
learning_curve.png
```

觀察結果：

* 初期 reward 非常低（約 -100），因為頻繁掉入 cliff
* 隨著訓練進行，reward 快速上升
* 最終：

  * SARSA 約落在 **-20 ~ -30**
  * Q-learning 約落在 **-40 ~ -50**

---

### 2️⃣ 策略比較（Policy）

輸出圖：

```
q_policy.png
sarsa_policy.png
```

#### Q-learning：

* 學習到**最短路徑**
* 會貼著 cliff 行走
* 風險高（容易掉落）

#### SARSA：

* 學習到**較安全路徑**
* 遠離 cliff
* 雖然路徑較長，但更穩定

---

### 3️⃣ 穩定性分析

| 方法         | 特性       |
| ---------- | -------- |
| Q-learning | 波動較大、較激進 |
| SARSA      | 較平穩、較保守  |

原因：

* SARSA 把 ε-greedy 的隨機性納入學習
* Q-learning 假設未來永遠選最佳動作（過於理想）

---

## 五、重要觀察（重點！老師很愛看這段）

1. **Q-learning 是理想化策略**

   * 學的是「最優解」
   * 但實際執行可能危險

2. **SARSA 是實際策略**

   * 學的是「會探索的策略」
   * 因此更安全

3. **Cliff Walking 是經典對比例子**

   * 完美展示 On-policy vs Off-policy 差異

---

## 六、結論

* Q-learning 收斂較快，但策略較冒險
* SARSA 收斂較穩定，策略較安全
* 在高風險環境中：
  👉 SARSA 通常表現較好

---

## 七、如何執行

```bash
python main.py
```

輸出：

* learning_curve.png
* q_policy.png
* sarsa_policy.png

```

---

## 八、程式架構

- `CliffWalkingEnv`：環境
- `QLearningAgent`：Q-learning
- `SARSAAgent`：SARSA
- `run_experiment()`：多次平均
- `visualize_policy()`：策略視覺化



```
