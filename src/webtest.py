from flask import Flask, jsonify,request,redirect,url_for,flash
import json
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)

# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allwed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ファイルを受け取る方法の指定
@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # アップロード後のページに転送
            return redirect(url_for('uploads_file'))
    return '''
    <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>
                ファイルをアップロードして判定しよう
            </title>
        </head>
        <body>
            <h1>
                ファイルをアップロードして判定しよう
            </h1>
            <form method = post enctype = multipart/form-data>
            <p><input type=file name = file>
            <input type = submit value = Upload>
            </form>
        </body>
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)