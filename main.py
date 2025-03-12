import matplotlib.pyplot as plt

# 定义数据
x = [1, 2, 3]
y = [35.14999961853027, 70.52499961853027, 70.78333282470703]

# 创建图形和坐标轴
fig, ax = plt.subplots()

# 绘制折线图
ax.plot(x, y, marker='o', linestyle='-', color='blue', label='Line Plot')

# 设置坐标轴范围（确保数据在可见范围内）
ax.set_xlim(0, 4)  # 横坐标范围
ax.set_ylim(30, 80)  # 纵坐标范围

# 添加标题、标签和图例
ax.set_title("Line Plot Example")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.legend()

# 显示图形
plt.show()