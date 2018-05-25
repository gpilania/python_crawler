# Linux 后台运行python

>  nohup python -u xx.py > log.out 2>&1 &  

* 1是标准输出（STDOUT）的文件描述符，2是标准错误（STDERR）的文件描述符1> log.out 简化为 >

log.out，表示把标准输出重定向到log.out这个文件

* 2>&1 表示把标准错误重定向到标准输出，这里&1表示标准输出















> https://blog.csdn.net/youzhouliu/article/details/75948619