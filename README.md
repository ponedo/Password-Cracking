口令猜测大作业 (Password Guessing Project)
======================================================
## 漫步猜测攻击 (Trawling Attack)
>所谓漫步攻击（Trawling Attacking）是指攻击者不关心具体的攻击对象是谁，其唯一目标是在允 许的猜测次数下，猜测出越多的口令越好．这意味 着，最优的攻击者会首先猜测排名 r=1 的口令，接 着猜测排名 r=2 的口令，依次类推．

>参考references中的《口令安全研究进展》.

## 文件及目录说明
- code: 代码目录，可大致分为三类
  1. 可运行模块
    + trainer.py: 训练模型的模块，需要提供-m/--model和-d/--dataset参数，详细说明见下.
    + tester.py: 测试模型的模块，需要提供-m/--model和-d/--dataset参数，详细说明见下.

  2. 口令生成模型构建模块
    + hmm4.py: 实现了reference《一种基于隐马尔可夫模型的口令猜测方法》的方法，感觉效果一般.
    + mc.py: 实现了reference《口令安全研究进展》中所提到的多阶马尔可夫模型的方法

  3. 辅助用模块（不用太在意的模块）
    + dataset.py: 用来加载数据集的模块.
    + sampler.py: 在生成密码时，往往需要对一个概率分布进行采样操作，此文件中的Sampler类就是进行采样操作的一个封装类.

- data: 数据集（csdn和yahoo太大了需要自行从课程网站上拿到，放在这个目录下）
  + toy_training_set: 自己随便写的一个小测试集
  + plain_txt_yahoo.txt: yahoo数据集，包含
  + www.csdn.net.sql: csdn数据集，包含用户名、密码、邮箱.

- model: 已训练模型的序列化文件

- reference: 参考资料

## 使用说明 (How to use)
>首先在命令行中，进入code目录.
1. 训练模型：
>>运行trainer.py模块，需要提供--model和--dataset参数（也可以分别缩写为-m和-d），比如下面这样
```shell
python trainer.py --model hmm4 --dataset csdn
```
>>就会使用csdn数据集训练一个隐马尔可夫模型，生成的模型以pickle序列化文件的形式（hmm4_csdn.pk）存于model中.

2. 使用模型生成口令：
>>运行tester.py模块，需要提供--model和--dataset参数（也可以分别缩写为-m和-d），比如下面这样
```shell
python tester.py --model hmm4 --dataset csdn
```
>>就会使用基于csdn数据集训练的隐马尔可夫模型，随机生成100条口令，控制台中打印出来.
```text
Password generated:
807508213881
820zailn
2777102792851
675351379982
xzuzy824
315360235
5208721625
...
```

3. 添加其他模型：
>>如果要添加除hmm4和mc之外的模型，参照hmm4.py和mc.py文件的格式，定义一个模型class，其中包含fit和generate方法即可。最后需要改一下trainer.py和tester.py，具体可见代码。

## 改进工作方向 (TODO List)
- 调研各种方法
  + 首先是references中的（不是很懂，得多看看）
    * PCFG（上下文无关》）？reference中有一篇《基于主题PCFG的口令猜测模型研究_毕红军》.
    * Zipf分布？reference中有一篇《Zipf's law in passwords》.
    * reference中提到的其他方法.
  + 其次可以看看nlp中文本生成的方法
    * 暴力一点的，比如RNN，LSTM，GAN等. reference中有一篇《Recurrent GANs Password Cracker For IoT Password Security Enhancement》可以看看.
    * reference中的《On the Semantic Patterns of Passwords and their Security Impact》.

- 改进已实现的方法
  + 按照《口令安全研究进展》中所述，将个人信息（如用户名、邮箱）与模型结合，实现Targeted models.
  + 其他改进，如对Markov Chain进行smoothing.

- 任何其他可行的东西.