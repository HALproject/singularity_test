# Singularity / PBS ハンズオン 早見表

## まず一言で

### Singularity / Apptainer
> **「動く環境ごと持ち運ぶ箱」**

### PBS
> **「共有計算機の交通整理係」**

---

# 1. このハンズオンでやること

このハンズオンでは次を体験します。

1. Singularity コンテナで Python を動かす
2. PBS ジョブとして実行する
3. Array Job で複数データをまとめて処理する

---

# 2. ディレクトリ構成

```text
handson_singularity_pbs/
├── README.md
├── CHEATSHEET.md
├── analyze.py
├── make_sample_data.py
├── run_local.sh
├── run_pbs.sh
├── run_array.sh
├── sample_data/
└── output/
```

---

# 3. まず使う基本コマンド

## 作業ディレクトリへ移動

```bash
cd handson_singularity_pbs
pwd
ls
```

---

## サンプルデータ作成

```bash
python3 make_sample_data.py
```

確認：

```bash
ls sample_data
```

---

# 4. Singularity / Apptainer の基本

## コンテナ内で Python バージョン確認

```bash
singularity exec python_env_handson_v1.sif python --version
```

> 環境によっては `singularity` の代わりに `apptainer`

---

## 必要ライブラリ確認

```bash
singularity exec python_env_handson_v1.sif python -c "import numpy, matplotlib; print('OK')"
```

---

## Python スクリプトをコンテナ内で実行

```bash
singularity exec python_env_handson_v1.sif \
    python analyze.py sample_data/data_01.csv output
```

---

# 5. まずは PBS なしで 1件実行

```bash
bash run_local.sh
```

確認：

```bash
ls output
cat output/data_01_summary.txt
ls output/*.png
```

---

# 6. PBS ジョブとして 1件実行

## ジョブ投入

```bash
qsub run_pbs.sh
```

例：

```bash
12345.server
```

---

## ジョブ状態確認

```bash
qstat
```

必要なら詳細：

```bash
qstat -f 12345
```

---

## 結果確認

```bash
ls output_pbs
cat output_pbs/data_02_summary.txt
```

---

# 7. PBS Array Job で複数ファイル処理

## 配列ジョブ投入

```bash
qsub run_array.sh
```

---

## 状態確認

```bash
qstat
```

---

## 結果確認

```bash
ls output_array
```

---

# 8. このハンズオンで覚えたい「役割分担」

## Singularity / Apptainer の役割
- Python 環境を揃える
- ライブラリをまとめる
- 同じ環境で再現可能に実行する

---

## PBS の役割
- 計算ノードで実行する
- CPU数・時間などを管理する
- 複数ジョブを順番に回す

---

# 9. よく使う PBS 用語

## ジョブ
> PBS に投入した1つの実行単位

---

## ジョブID
例：

```text
12345.server
```

ジョブを識別する番号

---

## Array Job
> **同じ処理を複数入力にまとめて流す仕組み**

例：

```bash
#PBS -J 1-5
```

---

## `PBS_ARRAY_INDEX`
Array Job の何番目かを表す番号

例：

```bash
FILE=$(printf "sample_data/data_%02d.csv" ${PBS_ARRAY_INDEX})
```

---

# 10. よく使う PBS スクリプトの意味

例：

```bash
#PBS -N singularity_array
#PBS -l select=1:ncpus=1
#PBS -l walltime=00:05:00
#PBS -J 1-5
#PBS -j oe
```

---

## `#PBS -N`
ジョブ名

---

## `#PBS -l select=1:ncpus=1`
使う計算資源の指定

- `select=1` → ノード数
- `ncpus=1` → CPU数

---

## `#PBS -l walltime=00:05:00`
最大実行時間

---

## `#PBS -J 1-5`
Array Job の範囲

---

## `#PBS -j oe`
標準出力と標準エラーをまとめる

---

# 11. よく使う補助コマンド

## 今いる場所を確認

```bash
pwd
```

---

## ファイル一覧を見る

```bash
ls
ls sample_data
ls output
```

---

## ファイル内容を見る

```bash
cat output/data_01_summary.txt
```

---

## 作業ディレクトリに戻る

```bash
cd ~/handson_singularity_pbs
```

（環境に応じて読み替え）

---

# 12. 受講者が一番覚えておくべきこと

## 1. なぜ Singularity を使う？
> **「同じ環境で動かすため」**

---

## 2. なぜ PBS を使う？
> **「重い処理を計算ノードで安全に回すため」**

---

## 3. なぜ Array Job が便利？
> **「同じ処理を大量データに一気に回せるため」**

---

# 13. よくあるトラブル

## `singularity: command not found`

環境によっては：

```bash
apptainer --version
```

---

## `qsub` したのに結果が出ない

確認：

```bash
qstat
ls *.o*
ls *.e*
```

---

## ファイルが見つからない

確認：

```bash
pwd
ls
ls sample_data
```

---

## 出力がどこにあるか分からない

確認：

```bash
ls output
ls output_pbs
ls output_array
```

---

# 14. 最後に一言

> **Singularity は「何で動かすか」を揃える道具**  
> **PBS は「どこで・どう回すか」を管理する道具**

---

# 最重要まとめ

## Singularity
> **環境を揃える**

## PBS
> **計算資源を管理する**

## HPC でよくあること
> **同じ解析を大量データに対して繰り返す**
