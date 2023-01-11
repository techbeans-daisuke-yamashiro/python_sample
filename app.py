#使用モジュールのインポート
import sys
import os
import pandas as pd
import numpy as np
import argparse as ap
from pprint import pprint

#コマンドラインオプションの処理
def getOptions():
  parser = ap.ArgumentParser(
    description = "Python処理サンプル"
    )
  parser.add_argument('-f','--file',
    help="入力ファイル名(必須)", type = str,required = True)
  parser.add_argument('-e','--export', help="出力ファイル形式('csv'または'excel'、省略時'excel')", 
    choices=['excel','csv'],default='excel',type = str)
  return parser.parse_args()    

#データファイル読み込み
def loadFile(fileName=False):
    df = False
    ext = False
    if (fileName):
      ext = os.path.splitext(fileName)
    else:
      print('ファイル名が指定されていません' ,file=sys.stderr)
      sys.exit(1)
    try:
      if ext == '.csv':
        print('CSVを読み込みます')
        df=pd.read_csv(fileName)
      else:
        print('EXCELシートを読み込みます')
        df=pd.read_excel(fileName)
    except Exception as e:
      print('データファイルの読み込みが失敗しました。処理を中断します。' ,file=sys.stderr)
      print(e)
      sys.exit(1)
    return df

# データ処理メインルーチン
def processData( data = False ):
  return data

#データ出力
def exportData(data=False,Options=False):
  if Options == False:
    print('ファイル出力設定の読み込みが失敗しました。処理を中断します。' ,file=sys.stderr)
    sys.exit(1) 
  elif data == False:
    print('出力データの構築に失敗しました。処理を中断します。' ,file=sys.stderr)
    sys.exit(1) 

  return data

# メインループ
def main():
  options = getOptions()
  processData(loadFile(options.file))
  return 0

if __name__ == '__main__':
  main()