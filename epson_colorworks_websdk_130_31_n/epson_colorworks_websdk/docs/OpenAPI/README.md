# Web SDK API Documentation

OpenAPIフォーマットで記述されたRESTful APIドキュメントです。
YAML形式で記述しています。

## 編集方法

標準フォーマットのためテキストエディタでも編集可能ですが、Stoplight Studioを使用して作成・編集しています。

https://stoplight.io/studio/

アプリ上でYAMLファイルを読み込ませてください。

## HTML出力方法

YAMLファイルを解釈してHTMLでのドキュメントに変換する方法は様々ありますが、
ここでは、ReDoc-CLIを使用して作成しています。

ReDoc-CLIをインストールし、

```
$ npm install -g redoc-cli
```

下記のコマンドでHTMLファイルを出力します。

```
$ redoc-cli bundle LabelPrinterWebSDK.yaml
```
