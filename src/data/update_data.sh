# cd /liubinxu/liubinxu/quantaxis_docker
# sudo docker-compose up -d
DATESTR=`date +"%Y%m%d"`

cd /liubinxu/liubinxu/finance/learning/easymoney_data
python3 ../easymoney_pinglun_0825.py 1 5000 > ${DATESTR}.tmp.json
cd /liubinxu/liubinxu/finance/learning/
/liubinxu/liubinxu/miniconda3/bin/python src/data/easy_money_senti_mongo.py easymoney_data/${DATESTR}.tmp.json

/liubinxu/liubinxu/miniconda3_py38/bin/python /liubinxu/liubinxu/finance/learning/src/data/update_etf_every_week.py
/liubinxu/liubinxu/miniconda3_py38/bin/python /liubinxu/liubinxu/finance/learning/src/data/update_stock_transaction.py


# cd /liubinxu/liubinxu/finance/learning/easymoney_data
# python3 ../easymoney_pinglun_0825.py 1 5000 > ${DATESTR}.tmp.json
# cd /liubinxu/liubinxu/finance/learning/
# /liubinxu/liubinxu/miniconda3/bin/python src/data/easy_money_senti_mongo.py easymoney_data/${DATESTR}.tmp.json