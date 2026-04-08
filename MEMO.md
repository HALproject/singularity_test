- selectを使う場合、res、ncpusも一つにまとめる必要がある
```bash
#PBS -q ジョブクラス -l select=1:res=small:ncpus=1
#PBS -l walltime=00:05:00
```
- select=1 は1つの計算ノードを使用することを意味します。
- ジョブクラス(キュー)が計算ノードを制限していないか、設定を確認する必要があります

### PBS/Torque `select` の意味

#### 基本構文
```
#PBS -l select=N:属性1=値1:属性2-2:...
```
- N = 要求するノード数
- 属性=各ノードに要求するリソース(CPU、メモリなど)

#### 具体例
```
#PBS -l select=1:ncpus-2:mem=4gb
```
- 1つのノードを要求
- そのノードで2CPUコアと4GBメモリを使用
```
#PBS -l select-2:ncpus-4:mem-8gb
```
- 2つのノードを要求
- 各ノードで4CPUコアと8GBメモリを使用
- 合計:8 CPUコア、16GBメモリ

#### ノード数の確認方法

ジョブ実行中に `$PBS_NUM_NODES` 環境変数で割り当てられたノード数を確認できます。
```
echo "Number of nodes: $PBS_NUM_NODES"
```
- select=1 は最もシンプルなケースで、シングルノードジョブを意味します。複数ノードが必要な並列計算ではselect=2 以上を指定します。
