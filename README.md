# UbuntuLaptopPowerCheck
装有Ubuntu笔记本的电量检查预警脚本，供电断开或电量小于阈值会向邮箱发送预警邮件。

在python文件内配置自己的邮箱、密码和smtp服务器地址

每60s查询一次状态，不会重复发送预警，电源恢复后会充值状态。
