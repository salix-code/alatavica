

在 /etc/systemd/system/ 目录下创建一个服务文件，例如 my_daemon.service：

ini
复制
[Unit]
Description=My Python Daemon
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/your/script
ExecStart=/usr/bin/python3 /path/to/your/script/my_daemon.py
Restart=always

[Install]
WantedBy=multi-user.target


# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start my_daemon

# 停止服务
sudo systemctl stop my_daemon

# 重启服务
sudo systemctl restart my_daemon

# 查看服务状态
sudo systemctl status my_daemon

# 设置开机自启动
sudo systemctl enable my_daemon