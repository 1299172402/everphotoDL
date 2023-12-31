# 时光相册下载

官网：https://www.everphoto.cn/

本软件为免费软件，禁止二次牟利。本人从未在任何平台发布购买程序、购买脚本、有偿下载、代下载、指导下载、远程服务等等的内容，如果你在任何渠道付费请及时举报并联系退费。这些人一旦看见token就能获取你的照片，请注意保护好隐私。

# Q&A

- Q: 初始化为什么进不去？为什么登陆到某一页就卡住了？

  A: 如图片，按照步骤一步步来
    ![](./docs/asset/token.jpg)

- Q: 下载卡住了可以退出重来吗？要从第一步开始吗？
  
  A: 可以，有断点续传，哪一步卡住就哪一步重来。失败了不需要从第一步开始，具体操作里软件有提示。

- 顺带一提，说明问题请给出你发生的错误的步骤或者截图，请尽量详细一些

## 已知部分问题

- 脚本在下载元数据时计算的照片和视频数量可能有误，这通常与 Apple Livephoto 有关。这部分内容在下载时是正常的

- 非东八区时间的照片的时间转换存在问题，会引发写入时间时程序中断的问题

## 未正式更新的版本

之前更新了按相册分类的everphotoDL，但并未发布正式版本，如有需要从 https://github.com/1299172402/everphotoDL/actions/runs/6560791256 下载，进入的选项为 `6.5`

这是一个测试版本，可能存在未知问题。

目前大体功能都已经实现，虽然之前为了硬盘空间不足的用户，还想写一个按相册/按下载时间下载的功能，但现在因为倒卖的原因，我也不会再为此项目更新，大家将就着用吧。

## 特点

- 比网页版下载要全，至少有手机上照片和视频的数量
- 下载后做md5校验，不像网页版可能下载到空文件
- 断点续传，不用担心下到一半断开
- 直接下载就是照片，不用再额外解压占用空间
- 可以设置照片下载路径

## 下载地址

- Github Release
  
  [![img](https://img.shields.io/github/v/release/1299172402/everphotoDL?label=版本)](https://github.com/1299172402/everphotoDL/releases)
  
- 蓝奏云

  [![](https://img.shields.io/badge/蓝奏云盘-密码:ever-blue)](https://zhiyuyu.lanzout.com/b09d8e0af) 

- Github Action (beta)
  
  [![Python application](https://github.com/1299172402/everphotoDL/actions/workflows/build.yml/badge.svg)](https://github.com/1299172402/everphotoDL/actions/workflows/build.yml)


## 如何使用

程序内有详细的说明
```
时光相册下载器
作者：之雨
Github开源地址: https://github.com/1299172402/everphotoDL

请按照以下步骤一步步操作：
下载功能
1. 登录时光相册
2. 设置下载路径
3. 下载相册的元数据
4. 批量下载图片和视频

整理功能
5. 智能整理照片（推荐）
6. 按时间整理
7. 恢复照片路径到整理前

共享相册
8. 设置共享相册下载路径
9. 下载共享相册的元数据
10. 批量下载共享相册的图片
11. 整理共享相册的信息、图片、视频、动态、评论、点赞
12. 恢复共享相册的路径到整理前

13. 写入照片时间到文件信息

0. 退出程序

请输入数字：

```

## 接口来源

- 时光相册手机最后一版v6.6.0的api
- https://openapi.everphoto.cn/sf/3/v4/GetUpdates 接口获取照片数据
- https://media.everphoto.cn/origin/{图片id} 下载原始图片，不是像网页端压缩后的压缩包，就是原始图，包括视频和图片

## 待办事项

- [x] 按文件夹分类存放，来源为上传时的文件夹，无来源的放在根文件夹
- [x] 按上传时间、照片时间分类存放
- [x] 将所有的照片数据、信息等写入db文件(sqlite)
- [x] 写入拍摄时间到文件的修改时间（可以不改变原始数据）
- [x] 共享相册下载
- [x] (低优先级)为程序设计图形界面

## 开发指南

[开发指南](./docs/developer.md)

## 其他说明

- 时光相册中也记录了曾经上传过然后又删除的照片信息，但这部分照片不可下载

## 作者的碎碎念

时光相册背靠字节跳动也要关闭吗库w(ﾟДﾟ)w我收到这个消息都震惊了

虽然但是，很舍不得就是了，/(ㄒoㄒ)/~~

我不算是时光相册很多年的老用户，也是一直愿意签到白嫖的人，不过从小学到整个大学生涯的照片、和家里亲人的照片、出去看风景的照片、一起吃饭的照片、一起出去玩的照片……都放在这里，一年又一年……就突然没了

我还没倒呢！你先倒了！┭┮﹏┭┮

相聚两依依，聚散终有时。时光相册，安好~

## 捐赠作者

<details>
  <summary>如果我帮助到了你，欢迎并且谢谢你的捐赠 💃💃❤🧡💛💙💚💜🖤💃💃（点击展开）</summary>
  <img src="https://archive.biliimg.com/bfs/archive/905b63819805cf2a523c1b8f1b0ed0220de3d223.png@500h.webp" referrerpolicy="no-referrer" >
  <img src="https://archive.biliimg.com/bfs/archive/8f0c67d748500ce0b8aeaa824740791de0cdefc6.png@500h.webp" referrerpolicy="no-referrer" >
</details>
