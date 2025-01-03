@echo off
REM 启动 HTTP 服务器
start python -m http.server 8262

REM 打开浏览器
start http://localhost:8262/