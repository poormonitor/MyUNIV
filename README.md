# MyUNIV

**高考志愿填报决策分析系统**

*浙江省第二十三届全省学生信息素养提升实践活动程序设计项目一等奖作品*

## Introduction

一直以来，高考志愿如何填报一直是困扰广大考生的难题，过去存在着资讯获取不易等一系列难题。
现阶段也存在着一些志愿填报服务，包括线下和线上的服务，但仍存在着极大的问题。
2021年6月，教育部要求，各地各高校要结合本地实际，进一步完善高考相关信息发布渠道和方式，充分运用信息化手段，为考生提供形式多样的志愿填报指导服务。

本项目通过官方数据建立数据库，帮助考生找到适合自己的学校与专业。

## Usage

### Installtion

安装前，请先准备 Python 3 与 NodeJS 环境。

```shell
git clone https://git.techo.cool/poormonitor/MyIMG.git myimg
cd myimg
pip install -r requirements.txt
cd view
npm install
npm run build
```

### Config

复制模板配置文件，初始化数据库。若要使用不同的数据库，修改 .env 及 alembic.ini 中的数据库路径。

```shell
cp .env.example .env
cp alembic.ini.example alembic.ini
alembic upgrade head
```

### Run

```shell
uvicorn --port {Port} main:app  
```

若需启动为系统服务，可创建以下service文件。

```
[Unit]
Description=MyIMG

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
User=www
PermissionsStartOnly=true
WorkingDirectory={Path to MyUNIV}
ExecStart={Path to uvicorn} --port {Port} main:app
Restart=on-failure
TimeoutSec=600
```

记得设置 nginx 的反向代理。

## LICENSE

本程序是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。

发布该程序是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证。

你应该随程序获得一份 GNU 通用公共许可证的副本。如果没有，请看 [GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)。

## Copyright

© 2022 - 2023 Johnson Sun (poormonitor@outlook.com). All rights reserved.

软件著作权登记号: 2022SR1026005