# 寮の自転車貸し出しシステム

## メモ
- 開発環境  
    - Linux Mint 19.3  
    - python 3.6.9  
    - Django 3.1.7  
    - PlatformIO  
- ファイル（フォルダー）の説明
    - step_test1→鍵収納BOX用Arduinoプログラム
    - booking→貸出簿、予約表のプログラム
## Djangoのインストール
1. インストール  
`python3 -m pip install Django`  
2. バージョンの確認  
`python3 -m django --version`  
3. 一応、python Shellでもエラーが出ないことを確認  
`python3`  
`>>>import django`  
`>>>print(django.get_version())`  
`>>>exit()`
## Bootstrap4のインストール
1. インストール  
`pip install bootstrap4`
