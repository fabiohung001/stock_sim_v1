import urllib, json , time

global init_money , final_money
global startDate , endDate  , endDate_real
global stock_list , stock_len
global debug
debug = 0

#get stock data from yahoo
def get_stock_info( stock_name ) :
	global startDate , endDate;
	url = "http://query.yahooapis.com/v1/public/yql?format=json&env=store://datatables.org/alltableswithkeys&q=select * from yahoo.finance.historicaldata where symbol = '" + stock_name + "' and startDate = '" + startDate + "' and endDate = '" + endDate + "'";
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data;

#print info of data
def print_info ( stock_data , stock_idx ) :
	global endDate_real ;
	nLoop = 0
	Price_start = 0
	Price_End = 0
	try :
		if debug : print data["query"]["results"]["quote"][0]["Symbol"] , 
		for day_quote in reversed(data["query"]["results"]["quote"]) :
			if nLoop == 0 or nLoop == len(data["query"]["results"]["quote"]) - 1 :
				if debug :
					print "Date : " , day_quote["Date"];
					print "Close : " , day_quote["Close"];

				if nLoop == 0 :
					Price_start = day_quote["Close"];
				elif nLoop == len(data["query"]["results"]["quote"]) - 1 :
					Price_End = day_quote["Close"];
					endDate_real = day_quote["Date"];
			nLoop += 1;
		change_percent  = round(((float(Price_End) - float(Price_start)) / float(Price_start))  ,4)
		if debug : print change_percent;
		if debug : print Price_start , Price_End 
		if debug : print float(Price_End) - float(Price_start) ,"%4s%%"  % float(change_percent*100);

		calc_init_money_total( change_percent , stock_idx );

	except: 
		global stock_len;
		stock_len = stock_len - 1;
		if debug : print "stock_len - 1 : " , stock_len ,

def calc_init_money_total( change_percent , stock_idx):

	global init_money_total  , stock_list
	stock_list[stock_idx][1] = stock_list[stock_idx][1] * (1 + change_percent);
	#clear init_money_total to 0 after time loop
	if stock_idx == 0 :
		init_money_total = 0 ;

	init_money_total = init_money_total + stock_list[stock_idx][1]
	if debug : print "Final money of this stock : " , stock_list[stock_idx][1] ;
	if debug : print "Final money of total : " , init_money_total;


init_money_total = 0.0;
init_money_single = 10000.0;

stock_list = [ 	["0001.hk" , init_money_single ],  
				["0005.hk" , init_money_single ],
				["0700.hk" , init_money_single ],
				["3888.hk" , init_money_single ],
				["0823.hk" , init_money_single ],
				["2208.hk" , init_money_single ],
				["1211.hk" , init_money_single ],
				["0268.hk" , init_money_single ],
				["1766.hk" , init_money_single ],
				["2800.hk" , init_money_single ],
				["0388.hk" , init_money_single ] 
			] ;

#startDate , endDate			
date_list = [#['2010-01-01' , '2010-07-01' ] , 
			 #['2010-07-01' , '2011-01-01' ] ,
			 #['2011-01-01' , '2011-07-01' ] , 
			 #['2011-07-01' , '2012-01-01' ] ,
			 #['2012-01-01' , '2012-07-01' ] , 
			 #['2012-07-01' , '2013-01-01' ] ,
			 #['2013-01-01' , '2013-07-01' ] , 
			 ['2013-07-01' , '2014-01-01' ] ,
			 ['2014-01-01' , '2014-07-01' ] , 
			 ['2014-07-01' , '2015-01-01' ] ,
			 ['2015-01-01' , '2015-07-01' ] , 
			 ['2015-07-01' , '2016-01-01' ] ,
			 ['2016-01-01' , '2016-07-01' ] , 
#			 ['2016-07-01' , '2017-01-01' ] ,
#			 ['2017-01-01' , '2017-07-01' ] ,
]

for date in date_list:
	startDate = date[0];
	endDate = date[1];
	endDate_real = endDate;
	stock_len = len(stock_list);
	for index , stock in enumerate(stock_list) :
		if debug : print index , stock;
		data = get_stock_info( stock[0] );
		print_info( data , index );
		if debug : print "=====",
	if debug : print ;

	print "From : " , startDate  , " to " , endDate_real ;

	if debug : 
		for nCount in stock_list :
			print nCount;

#	print "Final Money : " , init_money_total ;
#	print "Profit Money : " , init_money_total - init_money_single * stock_len  ;
#	print "Profit Percent : " , round( init_money_total / (init_money_single * stock_len)  , 4) - 1;
#	print "==========";
	time.sleep(0.5);

print "Final Money : " , init_money_total ;





