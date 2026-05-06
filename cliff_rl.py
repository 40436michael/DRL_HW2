import numpy as np
import random
import matplotlib.pyplot as plt

# ======================
# Environment
# ======================
class CliffWalkingEnv:
    def __init__(self, rows=4, cols=12):
        self.rows = rows
        self.cols = cols
        self.start = (rows - 1, 0)
        self.goal = (rows - 1, cols - 1)
        self.reset()

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        r, c = self.state

        # 0: Up, 1: Right, 2: Down, 3: Left
        if action == 0:
            r = max(r - 1, 0)
        elif action == 1:
            c = min(c + 1, self.cols - 1)
        elif action == 2:
            r = min(r + 1, self.rows - 1)
        elif action == 3:
            c = max(c - 1, 0)

        next_state = (r, c)

        # Cliff
        if r == self.rows - 1 and 1 <= c <= self.cols - 2:
            reward = -100
            next_state = self.start
            done = False
        elif next_state == self.goal:
            reward = 0
            done = True
        else:
            reward = -1
            done = False

        self.state = next_state
        return next_state, reward, done


# ======================
# Base Agent
# ======================
class BaseAgent:
    def __init__(self, rows, cols, actions,
                 alpha=0.1, gamma=0.9, epsilon=0.1):

        self.q = np.zeros((rows, cols, actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = actions

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.actions - 1)
        else:
            r, c = state
            return np.argmax(self.q[r, c])


# ======================
# Q-Learning
# ======================
class QLearningAgent(BaseAgent):
    def update(self, state, action, reward, next_state):
        r, c = state
        nr, nc = next_state

        best_next = np.max(self.q[nr, nc])

        self.q[r, c, action] += self.alpha * (
            reward + self.gamma * best_next - self.q[r, c, action]
        )


# ======================
# SARSA
# ======================
class SARSAAgent(BaseAgent):
    def update(self, state, action, reward, next_state, next_action):
        r, c = state
        nr, nc = next_state

        self.q[r, c, action] += self.alpha * (
            reward + self.gamma * self.q[nr, nc, next_action]
            - self.q[r, c, action]
        )


# ======================
# Training
# ======================
def train_q_learning(env, agent, episodes=500):
    rewards = []

    for ep in range(episodes):
        state = env.reset()
        total_reward = 0

        while True:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)

            agent.update(state, action, reward, next_state)

            state = next_state
            total_reward += reward

            if done:
                break

        rewards.append(total_reward)

    return rewards

def run_experiment(runs=50, episodes=500):
    q_all = np.zeros(episodes)
    sarsa_all = np.zeros(episodes)

    for _ in range(runs):
        env = CliffWalkingEnv()

        q_agent = QLearningAgent(4, 12, 4)
        sarsa_agent = SARSAAgent(4, 12, 4)

        q_rewards = train_q_learning(env, q_agent, episodes)
        sarsa_rewards = train_sarsa(env, sarsa_agent, episodes)

        q_all += np.array(q_rewards)
        sarsa_all += np.array(sarsa_rewards)

    return q_all / runs, sarsa_all / runs
def train_sarsa(env, agent, episodes=500):
    rewards = []

    for ep in range(episodes):
        state = env.reset()
        action = agent.choose_action(state)
        total_reward = 0

        while True:
            next_state, reward, done = env.step(action)
            next_action = agent.choose_action(next_state)

            agent.update(state, action, reward, next_state, next_action)

            state = next_state
            action = next_action
            total_reward += reward

            if done:
                break

        rewards.append(total_reward)

    return rewards


# ======================
# Plot Learning Curve
# ======================
def plot_learning_curves(q_rewards, sarsa_rewards):
    plt.figure(figsize=(10, 6))

    plt.plot(sarsa_rewards, label='SARSA')
    plt.plot(q_rewards, label='Q-learning')

    plt.xlabel('Episodes')
    plt.ylabel('Reward')
    plt.title('SARSA vs Q-learning (Cliff Walking)')
    plt.legend()
    plt.grid()
    plt.ylim([-200, 0]) 
    plt.savefig("learning_curve.png")
    plt.show()


# ======================
# Policy Extraction
# ======================
def get_policy(agent, rows=4, cols=12):
    policy = np.zeros((rows, cols), dtype=int)

    for y in range(rows):
        for x in range(cols):
            policy[y, x] = np.argmax(agent.q[y, x])

    return policy
def extract_path(env, policy, max_steps=100):
    path = []
    state = env.start
    path.append(state)

    for _ in range(max_steps):
        r, c = state
        action = policy[r, c]

        next_state, _, done = env.step(action)
        path.append(next_state)

        if done:
            break

        state = next_state

    return path

# ======================
# Policy Visualization
# ======================
def visualize_policy(policy, title, filename, path=None):
    action_symbols = {0: '↑', 1: '→', 2: '↓', 3: '←'}
    rows, cols = policy.shape

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.set_title(title, fontsize=16)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.invert_yaxis()
    ax.axis('off')

    # Grid
    for i in range(rows + 1):
        ax.plot([0, cols], [i, i], color='black')
    for j in range(cols + 1):
        ax.plot([j, j], [0, rows], color='black')

    # 轉成 set（方便查詢）
    path_set = set(path) if path else set()

    for y in range(rows):
        for x in range(cols):

            # Cliff
            if y == rows - 1 and 1 <= x <= cols - 2:
                rect = plt.Rectangle((x, y), 1, 1,
                                     facecolor='lightblue')
                ax.add_patch(rect)

            # Path（綠色）
            elif (y, x) in path_set:
                rect = plt.Rectangle((x, y), 1, 1,
                                     facecolor='lightgreen', alpha=0.6)
                ax.add_patch(rect)

            # Start
            if y == rows - 1 and x == 0:
                ax.text(x + 0.5, y + 0.5,
                        'Start\n↑',
                        ha='center', va='center',
                        fontsize=12, color='blue', fontweight='bold')

            # Goal
            elif y == rows - 1 and x == cols - 1:
                ax.text(x + 0.5, y + 0.5,
                        'Goal',
                        ha='center', va='center',
                        fontsize=12, fontweight='bold')

            # 一般格子（箭頭）
            elif not (y == rows - 1 and 1 <= x <= cols - 2):
                symbol = action_symbols[policy[y, x]]
                ax.text(x + 0.5, y + 0.5,
                        symbol,
                        ha='center', va='center',
                        fontsize=18, fontweight='bold')

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# ======================
# Main
# ======================
if __name__ == "__main__":

    # ===== 1️⃣ 多次實驗（畫 learning curve）=====
    print("Running 50 runs for learning curve...")
    q_rewards, sarsa_rewards = run_experiment()

    plot_learning_curves(q_rewards, sarsa_rewards)


    # ===== 2️⃣ 單次訓練（拿 policy）=====
    print("Training single run for policy visualization...")

    env = CliffWalkingEnv()

    q_agent = QLearningAgent(4, 12, 4)
    sarsa_agent = SARSAAgent(4, 12, 4)

    train_q_learning(env, q_agent)
    train_sarsa(env, sarsa_agent)


    # ===== 3️⃣ 取得 policy =====
    q_policy = get_policy(q_agent)
    sarsa_policy = get_policy(sarsa_agent)


    # ===== 4️⃣ 產生 path =====
    env.reset()
    q_path = extract_path(env, q_policy)

    env.reset()
    sarsa_path = extract_path(env, sarsa_policy)


    # ===== 5️⃣ 畫圖 =====
    visualize_policy(q_policy, "Q-learning Policy", "q_policy.png", q_path)
    visualize_policy(sarsa_policy, "SARSA Policy", "sarsa_policy.png", sarsa_path)


    print("Done! 已輸出圖片：")
    print("- learning_curve.png")
    print("- q_policy.png")
    print("- sarsa_policy.png")