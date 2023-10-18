# 开发指南

## 仓库文件说明

### 主目录
```
├─.github/workflows/build.yml  # 自动构建脚本
├─asset/kite.ico # 资源文件(程序图标)
├─src # 源代码
├─.gitattributes
├─.gitignore
├─developer.md # 开发指南
├─readme.md # 说明文档
├─requirements.txt # 依赖库
```

### 代码目录
```
# 主程序，包括初始化数据库，显示主菜单，追踪异常，具体功能从 function包 中调用
│  main.py 
│
# 各个功能模块
└─function
    # 1. 登录时光相册
    │  A_save_token.py 
    # 2. 设置下载路径 / 8. 设置共享相册下载路径
    │  B_set_dl_path.py
    # 3. 下载相册的元数据
    │  C_get_meta.py
    # 4. 批量下载图片和视频
    │  D_dl_picture.py
    # 5. 智能整理照片（推荐）
    │  E_organize_photos.py
    # 6. 按时间整理
    │  F_time_sort_photos.py
    # 7. 恢复照片路径到整理前 / 12. 恢复共享相册的路径到整理前
    │  G_revert_photo_path.py
    # 9. 下载共享相册的元数据
    │  H_get_share_meta.py
    # 10. 批量下载共享相册的图片
    │  I_dl_shared_album.py
    # 11. 整理共享相册的信息、图片、视频、动态、评论、点赞
    │  J_sort_shared_album.py
    # 13. 写入照片时间到文件信息
    │  K_write_time.py
    │
    # 一些工具函数
    └─tools
            # config.json 的读写
            config_io.py
            # 时光相册的api，包括获取元数据GetUpdates和下载照片Download_Media
            everphotoAPI.py
```

## 打包方式

从仓库根目录运行
```
pyinstaller --noconfirm --onefile --console --icon "asset/kite.ico"  "src/main.py"
```
