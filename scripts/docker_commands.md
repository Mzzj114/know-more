# 总结一句话

👉 你真正需要记住的就这 5 个：

```bash
docker compose up -d
docker compose logs -f
docker compose ps
docker compose exec web bash
docker compose down
```


---



# 一、先建立一个心智模型

你主要会用两套命令：

### 1️⃣ compose 层（管理整个项目）

```bash
docker compose ...
```

### 2️⃣ container 层（操作单个容器）

```bash
docker ...
```

# 二、最常用的一组（强烈建议记住）

## 1️⃣ 查看运行状态

```bash
docker compose ps
```
👉 类似 Docker Desktop 的容器列表


## 2️⃣ 查看日志（非常常用）

```bash
docker compose logs -f
```
只看一个服务：
```bash
docker compose logs -f web
```


## 3️⃣ 启动 / 后台运行

```bash
docker compose up -d
```
重新构建：

```bash
docker compose up -d --build
```

## 4️⃣ 停止 / 删除容器
```bash
docker compose down
```
👉 会删除容器，但保留 volume（默认）


## 5️⃣ 重启服务

```bash
docker compose restart
```


# 三、进入容器（你会很常用）

## 进入 shell

```bash
docker compose exec web bash
```

如果没有 bash：

```bash
docker compose exec web sh
```


# 四、看容器细节（调试用）

## 查看所有容器（包括停止的）

```bash
docker ps -a
```

## 查看资源占用（很好用）

```bash
docker stats
```

## 查看详细信息

```bash
docker inspect <container>
```

# 五、日志文件相关（你刚刚在配的）

## 看某个容器日志路径

```bash
docker inspect <container-id> | grep LogPath
```
默认在 /var/lib/docker/containers/<container-id>/

```bash
du -sh /var/lib/docker/containers/
```
du(disk usage) 列出大小，
-s 表示汇总，
-h 表示人类可读

```bash
df -h
```
硬盘分区大小

## 清空日志（紧急用）

```bash
sudo truncate -s 0 /var/lib/docker/containers/*/*.log
```

---

# 六、镜像管理（偶尔用）

## 查看镜像

```bash
docker images
```


## 删除无用镜像（非常推荐定期做）

```bash
docker image prune -a
```


# 七、清理系统（救命命令）

```bash
docker system prune -a
```

👉 会删除：

* 停止的容器
* 未使用的镜像
* 网络

⚠️ 小心用（生产环境别乱执行）


# 八、volume（数据库很关键）

## 查看 volume

```bash
docker volume ls
```

## 删除 volume

```bash
docker volume rm <name>
```

👉 MySQL 数据就在这里

# 九、一个非常实用的“组合技能”

👉 查看日志 + 进入容器调试

```bash
docker compose logs -f web
# 另开一个窗口
docker compose exec web bash
```


# 十、给你一个“日常操作流”（很接近真实使用）

你以后大概率会这样用：

```bash
# 更新代码
git pull

# 重建并后台运行
docker compose up -d --build

# 看日志
docker compose logs -f

# 进容器排查
docker compose exec web bash
```

