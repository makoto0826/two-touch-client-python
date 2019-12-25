# Python アプリケーション

# 概要
Raspberry PI 3 Model B+で動作するタイムレコーダーアプリケーションになります。

# 必要な機器
- Sony PaSoRi RC-S380
- 液晶ディスプレイ(タッチ対応)

# ソフトウェア
- Rasbian

# セットアップ
1. Raspberry PIにSony PaSoRi RC-S380と液晶ディスプレイが接続した状態にします。

2. アプリケーションの動作に必要なソフトウェアのインストールと設定をします。

下記のコマンドを実行します。

``` sh
setup.sh install
```

3. Web APIの情報を設定します。

下記のコマンドを実行します。

``` sh
setup.sh api <API KEY> <Firebase リージョン> <Firebase プロジェクトID>
```

    引数の説明を下記に記載します。

|項目|説明|
|---|---|
|API KEY | FirestoreのdeivcesコレクションのapiKeyの値を設定してください。|
|Firebase リージョン| Cloud Functionsのリージョンを設定します。 Firebase コンソールから確認できます。|
|Firebase プロジェクトID| Firebase プロジェクトIDは、Firebase コンソールから確認できます。|

4. 再起動します。

# タッチパネル設定 
.kivy/config.initの[Input]に下記の値を設定します。

``` 
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
```

※ .kivy/config.iniが存在しない場合、アプリケーションを一度実行してください。

# 自動起動設定
下記のコマンドを実行します。

``` sh
setup.sh auto-start
```

※ 常にフルスクリーンでアプリケーションが表示されますので、停止はSSH経由で実施する必要があります。

# 自動起動設定停止
下記のコマンドを実行します。

``` sh
sudo systemctl stop two-touch
sudo systemctl disable two-touch
```


