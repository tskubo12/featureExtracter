# FeatureExtracter

指定したディレクトリから機械学習用の特徴を抽出し"result"ディレクトリに保存するプログラムです。

## ファイル
* assemblyToJson.py  
指定したディレクトリ内にあるファイルから機械語命令のみを抽出し結果を"result"ディレクトリに保存する

* byteToImage.py  
指定したディレクトリ内にあるファイルのバイナリを画像化しgist特徴量を抽出、"result"ディレクトリに保存する

* syusiML.yml  
condaによるpython環境を構成するためのyamlファイル

* malwareListMD5.csv  
対象のマルウェア名のリスト

## インストール
Anacondaのインストールを行う:  
`wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh`  
`sh Anaconda3-2019.10-Linux-x86_64.sh`  
`source ~/.bashrc`

**上記でインストール出来ない場合は[古いバージョン](https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh)を用いてインストールしてください**

condaによるpython実行環境の構築と移動を行う:  
`conda-env create -n extract -f syusiML.yml`  
`conda deactivate`  
`conda activate extract`  

gist特徴量を得るためのライブラリ[fftw](http://www.fftw.org)のインストール:  
`wget http://www.fftw.org/fftw-3.3.8.tar.gz`  
`tar -zxvf fftw-3.3.8.tar.gz`  
`cd fftw-3.3.8/`  
`./configure --enable-single --enable-shared`  
`make`  
`sudo make install`

[fftwをpythonで使用するためのラッパー](https://github.com/tuttieee/lear-gist-python)インストール:  
`git clone https://github.com/tuttieee/lear-gist-python.git`  
`cd  lear-gist-python/`  
`./download-lear.sh`  
`python setup.py build_ext`  
`python setup.py install`  

opencvのインストール:  
`pip install opencv-python`

## 特徴抽出  
byteFiles:  
特徴抽出したいマルウェアの入っているディレクトリ

`python assemblyToJson.py byteFiles/`  
`python byteToImage byteFiles/`  
