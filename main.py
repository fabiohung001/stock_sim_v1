import urllib, json

global init_money , final_money
global startDate , endDate  , endDate_real

init_money_total = 0.0
init_money_single = 10000.0
startDate = '2017-01-01'
endDate = '2017-07-01'

#get stock data from yahoo
def get_stock_info( stock_name ) :
	global startDate , endDate;
	url = "http://query.yahooapis.com/v1/public/yql?format=json&env=store://datatables.org/alltableswithkeys&q=select * from yahoo.finance.historicaldata where symbol = '" + stock_name + "' and startDate = '" + startDate + "' and endDate = '" + endDate + "'";
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data;

#print info of data
def print_info ( stock_data ) :
	print data["query"]["results"]["quote"][0]["Symbol"];
	global endDate_real;
	nLoop = 0
	Price_start = 0
	Price_End = 0

	for day_quote in reversed(data["query"]["results"]["quote"]) :
		if nLoop == 0 or nLoop == len(data["query"]["results"]["quote"]) - 1 :
			print "Date : " , day_quote["Date"];
			print "Close : " , day_quote["Close"];
			if nLoop == 0 :
				Price_start = day_quote["Close"];
			elif nLoop == len(data["query"]["results"]["quote"]) - 1 :
				Price_End = day_quote["Close"];
				endDate_real = day_quote["Date"];
		nLoop += 1;
	change_percent  = round(((float(Price_End) - float(Price_start)) / float(Price_start))  ,4)
	print change_percent;
	print Price_start , Price_End 
	print float(Price_End) - float(Price_start) ,"%4s%%"  % float(change_percent*100);

	calc_init_money_total( change_percent );

def calc_init_money_total( change_percent ):

	global init_money_total , init_money_single
	final_money = init_money_single * (1 + change_percent);
	init_money_total = init_money_total+ final_money
	print "Final money of this stock : " , final_money ;
	print "Final money of total : " , init_money_total;


stock_list = ["0001.hk" , "0005.hk" , "0700.hk" , "3888.hk" , "0823.hk" , \
			"2208.hk" , "1211.hk" , "0268.hk" , "1766.hk" , "2800.hk" , \
			"0388.hk" ] ;

for stock in stock_list :
	data = get_stock_info(stock);
	print_info(data);
	print "=====";

print "From : " , startDate  , " to " , endDate_real ;
print stock_list;
print "Final Money : " , init_money_total ;
print "Profit Money : " , init_money_total - init_money_single * len(stock_list)  ;
print "Profit Percent : " , round( init_money_total / (init_money_single * len(stock_list))  , 4) - 1;
print "==========";






