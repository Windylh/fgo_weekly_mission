### 项目说明
本插件为fgo周常任务规划插件，用于自动求解fgo周常任务消耗ap最少的刷图方案。目前只有free本的数据。

关卡数据取自[Mooncell](https://fgo.wiki/w/%E9%A6%96%E9%A1%B5)

线性规划算法使用pulp库实现
### 使用
将项目文件夹放入`Hoshino/modules`目录，并安装requirements.txt中的依赖。

在`config/__bot__.py`文件`MODULES_ON`中添加`fgo_weekly_mission`

### 指令
#### fgo周常规划
`fgo周常规划 特性/场地x个数`进行使用，多个特性/场地用空格隔开。

对于特性，`xx属性`可以直接输入关键字，eg:`龙x15`;对于`x之力`需要输入全部,eg:`地之力x3`


从者需要在特性后加上从者关键字。eg:`混沌从者x3 剑阶从者x3`

#### fgo特性列表
返回支持的特性内容。

### TODO
支持`击败『Saber』『Archer』『Lancer』职阶中任意一种敌人15个`的查询。

支持私聊