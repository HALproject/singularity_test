# Singularity + PBS ハンズオン

## 目的

このハンズオンでは、以下を体験します。

- Singularity コンテナを使って Python スクリプトを実行する
- PBS を使ってジョブを投入する
- 複数データを Array Job でまとめて処理する
- 出力ファイルやログを確認する

---

# 事前確認

以下のコマンドが使えることを確認してください。

```bash
singularity --version
qstat
qsub --version
```

> 環境によっては `apptainer` コマンドの場合があります。

---

# ディレクトリ構成

```text
handson_singularity_pbs/
├01_main_handson/
│   ├README.md
│   ├analyze.py
│   ├make_sample_data.py
│   ├run_local.sh
│   ├run_pbs.sh
│   ├run_array.sh
│   ├sample_data/
│   ├output_pbs/
│   └output/
├02_supplement_def/
│   ├README_def.md
│   └python_env_handson_v1.def
├03_supplement_operations/
│   └README_operations.md
├04_instructor_notes/
│   └Linstructor_notes.md
└containers/
     └python_env.def
```

---

# Step 0. 作業ディレクトリへ移動

```bash
cd handson_singularity_pbs
pwd
ls
```

---

# Step 1. サンプルデータを作る

まずは解析対象となる CSV データを作ります。

```bash
python3 make_sample_data.py
```

確認：

```bash
ls sample_data
```

以下のようなファイルができていればOKです。

```bash
data_01.csv
data_02.csv
data_03.csv
data_04.csv
data_05.csv
```

---

# Step 2. Singularity で Python を動かす

## 2-1. コンテナ内の Python バージョン確認

```bash
singularity exec python_env.sif python --version
```

## 2-2. 必要ライブラリが使えるか確認

```bash
singularity exec python_env.sif python -c "import numpy, matplotlib; print('OK')"
```

### ポイント

ここで大事なのは：

- 自分で `pip install` していない
- それでも Python / NumPy / matplotlib が使える

という点です。

つまり、**「必要な実行環境がコンテナに入っている」** というのが Singularity のメリットです。

---

# Step 3. 1つのデータをローカル実行する

```bash
bash run_local.sh
```

確認：

```bash
ls output
cat output/data_01_summary.txt
```

PNG画像も作られているか確認：

```bash
ls output/*.png
```

### ポイント

ここで実行しているのは：

```bash
singularity exec python_env.sif python analyze.py ...
```

です。

つまり、**Python を直接実行するのではなく、コンテナ環境の中で実行している**ことが重要です。

---

# Step 4. PBS ジョブとして 1件流す

## 4-1. ジョブ投入

```bash
qsub run_pbs.sh
```

例：

```bash
12345.server
```

## 4-2. ジョブ状態確認

```bash
qstat
```

必要に応じて：

```bash
qstat -f 12345
```

## 4-3. 実行後に出力確認

```bash
ls output_pbs
cat output_pbs/data_02_summary.txt
```

### ポイント

PBS を使う理由は：

- ログインノードで重い処理をしない
- 計算ノードで処理を行う
- CPU数や実行時間を指定できる

からです。

つまり PBS は **「計算資源の交通整理役」** です。

---

# Step 5. Array Job で複数データをまとめて処理する

## 5-1. 配列ジョブ投入

```bash
qsub run_array.sh
```

## 5-2. ジョブ確認

```bash
qstat
```

## 5-3. 出力確認

```bash
ls output_array
```

成功すると、以下のようなファイルができます。

```bash
data_01_summary.txt
data_01_hist.png
data_02_summary.txt
data_02_hist.png
...
```

### ポイント

PBS Array Job を使うと、**同じ処理を複数の入力ファイルにまとめて実行**できます。

これは実際の研究や解析で非常によく使われるパターンです。

---

# まとめ

## Singularity の役割
- 必要な実行環境をまとめる
- 同じ環境で再現可能に実行する

## PBS の役割
- 計算ノードでジョブを実行する
- 計算資源（CPU、時間など）を管理する
- 複数ジョブを安全に回す

## HPCでよくある実務
- 同じ解析を大量データに対して実行する
- そのために PBS + Singularity を組み合わせる

---

# 発展課題

余裕があれば以下も試してみてください。

1. `sample_data` のファイル数を増やす
2. `run_array.sh` の `#PBS -J 1-5` を変更する
3. `analyze.py` に中央値や分位点を追加する
4. `#PBS -l select=1:ncpus=2` などに変更して意味を考える

---

# トラブルシュート

## 1. `python_env.sif` がない

講師配布の Singularity イメージが必要です。

```bash
ls *.sif
```

## 2. `singularity: command not found`

環境によっては以下です。

```bash
apptainer --version
```

## 3. `qsub` は通るが出力が出ない

ジョブログを確認してください。

```bash
ls *.o*
ls *.e*
```

または

```bash
cat <ジョブ出力ファイル>
```

## 4. 作業ディレクトリが違う

PBSジョブスクリプトには以下が入っています。

```bash
cd $PBS_O_WORKDIR
```

これは **「qsub を実行した場所に移動する」** という意味です。
