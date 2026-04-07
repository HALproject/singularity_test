# 補足教材1：Singularity / Apptainer の `.def` ファイルを理解する

## この教材の目的

この補足教材では、Singularity / Apptainer の **Definition File (`.def`)** が何をしているのかを理解します。

ハンズオン本編では、受講者は主に **`.sif` ファイルを使って実行**しました。

しかし、実務では次のような場面がよくあります。

- 必要な Python パッケージを追加したい
- 解析ツールをコンテナに含めたい
- 他人に配る前に環境を整えたい
- 何が入っているコンテナなのかを確認したい

そのために必要なのが **`.def` ファイル** です。

---

# 1. `.def` と `.sif` の関係

まず一番大事な理解です。

## `.def`
> **コンテナの設計図 / レシピ**

## `.sif`
> **完成した実行用コンテナイメージ**

つまり、流れとしては：

1. `.def` に「何を入れるか」を書く
2. build して `.sif` を作る
3. 実行時は `.sif` を使う

です。

---

# 2. 今回の `.def` ファイル

今回のハンズオンで使った例は以下です。

```def
Bootstrap: docker
From: python:3.11-slim

%labels
    Author YourName
    Version v1.0
    Description "Python handson environment for PBS + Singularity"

%environment
    export PYTHONUNBUFFERED=1
    export MPLBACKEND=Agg

%post
    apt-get update && apt-get install -y \
        gcc \
        gfortran \
        libfreetype6-dev \
        libpng-dev \
        && rm -rf /var/lib/apt/lists/*

    pip install --no-cache-dir \
        numpy \
        matplotlib

%runscript
    exec python "$@"
```

これを順番に見ていきます。

---

# 3. `Bootstrap` と `From`

## `Bootstrap: docker`

```def
Bootstrap: docker
```

これは：

> **Docker イメージを土台として使う**

という意味です。

Singularity / Apptainer では、ゼロから環境を作るのではなく、  
既存の Docker イメージをベースとして流用することがよくあります。

---

## `From: python:3.11-slim`

```def
From: python:3.11-slim
```

これは：

> **Python 3.11 が入った軽量 Linux イメージを使う**

という意味です。

この時点で、最低限の Python 実行環境がすでに入っています。

---

# 4. `%labels`

```def
%labels
    Author YourName
    Version v1.0
    Description "Python handson environment for PBS + Singularity"
```

ここは：

> **コンテナのメタ情報（説明書き）**

を書く場所です。

たとえば：

- 誰が作ったか
- バージョン
- 何の用途か

を記録できます。

---

## なぜ大事なのか？

時間が経つと、以下のようなことが起こりがちです。

- このコンテナ、何のためのものだっけ？
- どの講義で使ったんだっけ？
- v1 と v2 の違いは？

こういう時に、ラベルがあるとかなり助かります。

---

# 5. `%environment`

```def
%environment
    export PYTHONUNBUFFERED=1
    export MPLBACKEND=Agg
```

ここは：

> **コンテナ実行時の環境変数を設定する場所**

です。

つまり、このコンテナを使ってプログラムを動かしたときに、  
毎回自動で設定される値です。

---

## `PYTHONUNBUFFERED=1`

```bash
export PYTHONUNBUFFERED=1
```

これは：

> **Python の標準出力をバッファせず、すぐに表示しやすくする**

ための設定です。

### なぜ便利？
PBS でジョブを流すと、ログを後から確認することが多いです。

この設定があると、`print()` の内容がログに反映されやすくなり、  
**デバッグや進捗確認がしやすくなります。**

---

## `MPLBACKEND=Agg`

```bash
export MPLBACKEND=Agg
```

これは：

> **matplotlib を画面表示なしで画像保存できるモードにする**

ための設定です。

### なぜ大事？
HPC 環境では多くの場合、GUI（画面表示）がありません。

そのため、matplotlib がデフォルト設定のままだと、

- 画面表示をしようとして失敗する
- 描画周りでエラーになる

ことがあります。

`Agg` にしておくと、**PNG保存などのバッチ処理が安定しやすい**です。

---

# 6. `%post`

```def
%post
    apt-get update && apt-get install -y \
        gcc \
        gfortran \
        libfreetype6-dev \
        libpng-dev \
        && rm -rf /var/lib/apt/lists/*

    pip install --no-cache-dir \
        numpy \
        matplotlib
```

ここは一番大事です。

> **コンテナ build 時に実行される処理**

です。

つまり：

> **「このコンテナに何を入れるか」**

を書く場所です。

---

## `apt-get install`

```bash
apt-get update && apt-get install -y \
    gcc \
    gfortran \
    libfreetype6-dev \
    libpng-dev
```

ここでは、Linux レベルのパッケージを追加しています。

今回の用途では主に：

- Python 科学計算系ライブラリの補助
- matplotlib の描画系依存

を満たすために入れています。

---

## `pip install`

```bash
pip install --no-cache-dir \
    numpy \
    matplotlib
```

ここで Python パッケージを入れています。

つまり今回のハンズオンでは、この build の時点で：

- NumPy
- matplotlib

がすでに使えるようになっています。

そのため受講者は、各自で `pip install` をしなくても済みます。

---

# 7. `%runscript`

```def
%runscript
    exec python "$@"
```

ここは：

> **このコンテナを `run` した時に、何を実行するか**

を決める場所です。

たとえば：

```bash
singularity run python_env_handson_v1.sif --version
```

のように実行すると、この `%runscript` が呼ばれます。

今回の設定では：

```bash
exec python "$@"
```

なので、**Python をそのまま実行するコンテナ**として振る舞います。

---

# 8. `exec` と `run` の違い（初学者向け）

Singularity / Apptainer ではよく以下を使います。

---

## `exec`

```bash
singularity exec python_env_handson_v1.sif python analyze.py sample_data/data_01.csv output
```

これは：

> **コンテナの中で、指定したコマンドをそのまま実行する**

方法です。

ハンズオン本編では主にこちらを使いました。

---

## `run`

```bash
singularity run python_env_handson_v1.sif --version
```

これは：

> **`.def` の `%runscript` に書かれたデフォルト動作を使う**

方法です。

今回のコンテナでは `%runscript` に Python 実行が設定されているため、  
`run` でも Python が起動します。

---

# 9. build のイメージ

`.def` を `.sif` にするには build を行います。

例：

```bash
sudo singularity build python_env_handson_v1.sif python_env_handson_v1.def
```

または環境によっては：

```bash
sudo apptainer build python_env_handson_v1.sif python_env_handson_v1.def
```

---

# 10. 実務での使い方の流れ

実際には次のような役割分担になることが多いです。

---

## コンテナ作成者（講師 / 管理者 / 開発者）
- `.def` を編集する
- build して `.sif` を作る
- `.sif` を配布する

---

## 利用者（受講者 / 研究者 / 利用者）
- `.sif` を使ってジョブを実行する
- 必要に応じて PBS スクリプトから呼び出す

---

# 11. まとめ

この補足教材で一番大事なことは以下です。

---

## `.def`
> **コンテナの作り方を書くファイル**

## `.sif`
> **完成して配布・実行に使うファイル**

## `%post`
> **何をインストールするかを書く**

## `%environment`
> **実行時の設定を書く**

## `%runscript`
> **`run` したときのデフォルト動作を書く**

---

# 12. 発展課題

余裕があれば、以下を試してみてください。

1. `.def` に `scipy` を追加して build し直す
2. `%labels` に自分の名前や日付を入れる
3. `%environment` に他の環境変数を追加する
4. `pip install pandas` を追加して使えるか確認する

---

# 一言まとめ

> **Singularity / Apptainer の本質は、環境構築手順を「コードとして残すこと
