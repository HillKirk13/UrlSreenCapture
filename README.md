# UrlSreenCapture
批量获取网站的截图
## use
需要提前安装好浏览器驱动，将驱动文件安装到浏览器安装目录
安装好pip相关依赖
### ubuntu安装驱动方法
编辑/etc/apt/sources.list文件，可以使用任何文本编辑器
在文件末尾添加以下行来添加Google Chrome的软件源：
  deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
下载和安装Google签名密钥以确保下载的文件来自Google：
  wget https://dl.google.com/linux/linux_signing_key.pub
  sudo apt-key add linux_signing_key.pub
  sudo apt update
  sudo apt install google-chrome-stable
