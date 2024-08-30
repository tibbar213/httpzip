# httpzip

从 zip 文件中下载单个文件，而无需下载整个压缩包。

## Docker部署

```bash
cd httpzip
docker build --network=host -t flask-zip-viewer . && docker run -d -p 5000:5000 --name flask-zip-viewer-container flask-zip-viewer
```
