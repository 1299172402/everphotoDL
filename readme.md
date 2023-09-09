# 时光相册下载

官网：https://www.everphoto.cn/

keywords: 时光相册, 打包下载, 批量下载, 全部下载

## 特点

- 比网页版下载要全，至少有手机上照片和视频的数量
- 下载后做md5校验，不像网页版可能下载到空文件
- 断点续传，不用担心下到一半断开
- 直接下载就是照片，不用再额外解压占用空间

## 下载地址

- Github Release
  
  [![img](https://img.shields.io/github/v/release/1299172402/BBDown_GUI?label=%E7%89%88%E6%9C%AC)](https://github.com/1299172402/BBDown_GUI/releases)
  
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

下载功能
请按照以下步骤一步步操作：
1. 登录时光相册 
2. 设置下载路径 D:/EverPhoto
3. 下载相册的元数据
4. 批量下载图片和视频

整理功能
5. 智能整理照片（推荐）
6. 按时间整理
7. 恢复照片路径到整理前

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
- [ ] 写入EXIF
- [x] 共享相册下载
- [x] (低优先级)为程序设计图形界面

## 打包方式

```
pyinstaller --noconfirm --onefile --console --icon "kite.ico"  "main.py"
```

## 其他说明

- 时光相册中也记录了曾经上传过然后又删除的照片信息，但这部分照片不可下载

- 如果遇到程序闪退，请尝试以下操作：
  1. 退出程序
  2. 删除与程序同一目录下的`original_response`文件夹
  3. 启动程序，并从头重新开始操作


## 作者的碎碎念

时光相册背靠字节跳动也要关闭吗库w(ﾟДﾟ)w我收到这个消息都震惊了

虽然但是，很舍不得就是了，/(ㄒoㄒ)/~~

我不算是时光相册很多年的老用户，也是一直愿意签到白嫖的人，不过从小学到整个大学生涯的照片、和家里亲人的照片、出去看风景的照片、一起吃饭的照片、一起出去玩的照片……都放在这里，一年又一年……就突然没了

我还没倒呢！你先倒了！┭┮﹏┭┮

聚散终有时啊
