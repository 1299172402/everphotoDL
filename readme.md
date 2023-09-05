# 时光相册下载

官网：https://www.everphoto.cn/

keywords: 时光相册, 打包下载, 批量下载, 全部下载

## 特点

- 比网页版下载要全，至少有手机上照片和视频的数量
- 下载后做md5校验，不像网页版可能下载到空文件
- 断点续传，不用担心下到一半断开
- 直接下载就是照片，不用再额外解压占用空间

## 如何使用

程序内有详细的说明
```
时光相册下载器
作者：之雨
Github开源地址: https://github.com/1299172402/everphotoDL

请按照以下步骤操作：
1. 登录时光相册
2. 设置下载路径 D:/EverPhoto
3. 下载原始数据
4. 批量下载图片和视频
0. 退出程序
请输入数字：

```

## 接口来源

- 时光相册手机最后一版v6.6.0的api
- https://openapi.everphoto.cn/sf/3/v4/GetUpdates 接口获取照片数据
- https://media.everphoto.cn/origin/{图片id} 下载原始图片，不是像网页端压缩后的压缩包，就是原始图，包括视频和图片

## 待办事项

- [ ] 为了方便整理，每个图片文件都的信息都放到一个单独的json中（包括上传时间`uploadedAt`，拍摄时间`creationTime` `taken`，宽`width`，高`height`，在手机时的路径（包括原始文件名）`source_path`，EXIF信息`exif`，文件大小`size`，文件校验`md5`）
- [ ] OCR文本识别的内容 `https://openapi.everphoto.cn/sf/3/v4/GetAssetCvInfo`
- [ ] 标签归类，包括自建的相册，人物分类，或者截屏、风景、美食等时光相册自动打的tag
- [ ] 按文件夹分类存放，来源为上传时的文件夹，无来源的放在根文件夹
- [ ] (低优先级)人脸信息`https://openapi.everphoto.cn/sf/3/v4/GetAssetFaceFeature`
- [ ] (低优先级)位置信息`https://openapi.everphoto.cn/v1/locations`
- [ ] (低优先级)为程序设计图形界面

## 打包方式

```
pyinstaller --noconfirm --onefile --console --icon "kite.ico"  "main.py"
```

## 其他说明

- 时光相册中也记录了曾经上传过然后又删除的照片信息，但这部分照片不可下载

## 作者的碎碎念

时光相册背靠字节跳动也要关闭吗库w(ﾟДﾟ)w我收到这个消息都震惊了

虽然但是，很舍不得就是了，/(ㄒoㄒ)/~~

我不算是时光相册很多年的老用户，也是一直愿意签到白嫖的人，不过从小学到整个大学生涯的照片、和家里亲人的照片、出去看风景的照片、一起吃饭的照片、一起出去玩的照片……都放在这里，一年又一年……就突然没了

我还没倒呢！你先倒了！┭┮﹏┭┮

聚散终有时啊
