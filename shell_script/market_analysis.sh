#!/bin/bash
export PYTHONPATH=PYTHONPATH:/workspace
# データアップデート
python /workspace/marketanalysis/controller/command.py stock_update

# 分析
python /workspace/marketanalysis/controller/command.py optimize -i "macross.EmaCross" -ot "^N225" -s "simple_strategy.SimpleTradingStrategy" -tt "1458.T"
python /workspace/marketanalysis/controller/command.py optimize -i "rsi.Rsi" -ot "^N225" -s "simple_strategy.SimpleTradingStrategy" -tt "1458.T"
python /workspace/marketanalysis/controller/command.py optimize -i "macd.Macd" -ot "^N225" -s "simple_strategy.SimpleTradingStrategy" -tt "1458.T"
python /workspace/marketanalysis/controller/command.py optimize -i "stochastic.SlowStochastic" -ot "^N225" -s "simple_strategy.SimpleTradingStrategy" -tt "1458.T"
python /workspace/marketanalysis/controller/command.py optimize -i "macross.EmaCross" -ot "1459.T" -s "simple_strategy.SimpleTradingStrategy"
python /workspace/marketanalysis/controller/command.py optimize -i "rsi.Rsi" -ot "1459.T" -s "simple_strategy.SimpleTradingStrategy"
python /workspace/marketanalysis/controller/command.py optimize -i "macd.Macd" -ot "1459.T" -s "simple_strategy.SimpleTradingStrategy"
python /workspace/marketanalysis/controller/command.py optimize -i "stochastic.SlowStochastic" -ot "1459.T" -s "simple_strategy.SimpleTradingStrategy"

