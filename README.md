# MotionDetections
OpenCVとDlibを使用して様々な顔の動作検知を実装しています。

## faceDirectionDetection.py
顔が正面を向いているかどうかを検知します。

・推定されたオイラー角に基づいて、顔が正面を向いているかどうかを判定

・正面を向いている場合は緑色の枠と「I Love You」というテキストを表示し、そうでない場合は赤色の枠と「Look At Me!」というテキストを表示

## nodDetection.py
頷きを検知し、その回数を表示します。

・現在の鼻の座標と前の鼻の座標の変化量を計算

・鼻のY座標の変化量が閾値より大きい場合、頷きと判定

## smileDetection.py
笑顔の強度を検知します。

## tiltDetection.py
首の傾げを検知します。
