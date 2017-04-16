import urllib, json , time

global init_money , final_money
global startDate , endDate , endDate_real
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
def print_info ( stock_data , stock_idx , version) :
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

					#set buy_in_price
					if stock_list[stock_idx][2] == 0 :
						stock_list[stock_idx][2] = day_quote["Close"];

				elif nLoop == len(data["query"]["results"]["quote"]) - 1 :
					Price_End = day_quote["Close"];
					endDate_real = day_quote["Date"];
					stock_list[stock_idx][3] = day_quote["Close"];


			nLoop += 1;
		change_percent  = round(((float(Price_End) - float(Price_start)) / float(Price_start))  ,4)
		if debug : print change_percent;
		if debug : print Price_start , Price_End 
		if debug : print float(Price_End) - float(Price_start) ,"%4s%%"  % float(change_percent*100);

		calc_init_money_total( change_percent , stock_idx , version);

	except: 
		global stock_len;
		stock_len = stock_len - 1;
		if debug : print "stock_len - 1 : " , stock_len ,

#version  1 = add money every count
# 0 =  only one init money
def calc_init_money_total( change_percent , stock_idx , version):

	global init_money_total  , stock_list , init_money_single
	if version == 0 :
		stock_list[stock_idx][1] = stock_list[stock_idx][1] * (1 + change_percent);
		#clear init_money_total to 0 after time loop
		if stock_idx == 0  :
			init_money_total = 0 ;
		init_money_total = init_money_total + stock_list[stock_idx][1]

	elif version == 1 :
		
		if stock_list[stock_idx][1] != init_money_single :
			init_money_total -= stock_list[stock_idx][1]
			stock_list[stock_idx][1] = (stock_list[stock_idx][1] + init_money_single) * (1 + change_percent);
		else : #first loop
			stock_list[stock_idx][1] = stock_list[stock_idx][1]  * (1 + change_percent);
		init_money_total += stock_list[stock_idx][1]
	
	if debug : print "Final money of this stock : " , stock_list[stock_idx][1] ;
	if debug : print "Final money of total : " , init_money_total;

#get hsi info
def get_hsi_info():
	global startDate , endDate;
	stock_name = "^HSI";
	url = "http://query.yahooapis.com/v1/public/yql?format=json&env=store://datatables.org/alltableswithkeys&q=select * from yahoo.finance.historicaldata where symbol = '" + stock_name + "' and startDate = '" + startDate + "' and endDate = '" + endDate + "'";
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	try :
		if debug : 
			print data["query"]["results"]["quote"][0]["Symbol"]
		if debug : 
			print data["query"]["results"]["quote"][0]["Close"]
		return data["query"]["results"]["quote"][0]["Close"];
	except :
		if debug : print "error in get_hsi_info";



init_money_total = 0.0;
init_money_single = 10000.0;
version = 1 ; #version  0 =  only one init money ; 1 = add money every count


#stock_no , init_money , buy_in_price , close_price
stock_list = [ 	["0001.hk" , init_money_single , 0 , 0 ],  
				["0005.hk" , init_money_single , 0 , 0 ],
				["0700.hk" , init_money_single , 0 , 0  ],
				["3888.hk" , init_money_single , 0 , 0  ],
				["0823.hk" , init_money_single , 0 , 0  ],
				["2208.hk" , init_money_single , 0 , 0  ],
				["1211.hk" , init_money_single , 0 , 0  ],
				["0268.hk" , init_money_single , 0 , 0  ],
				["1766.hk" , init_money_single , 0 , 0  ],
				["2800.hk" , init_money_single , 0 , 0  ],
				["0388.hk" , init_money_single , 0 , 0  ] 
			] ;

#startDate , endDate			
date_list = [
#			 ['2010-01-01' , '2010-07-01' ] , 
#			 ['2010-07-01' , '2011-01-01' ] ,
#			 ['2011-01-01' , '2011-07-01' ] , 
#			 ['2011-07-01' , '2012-01-01' ] ,
			 ['2012-01-01' , '2012-07-01' ] , 
			 ['2012-07-01' , '2013-01-01' ] ,
			 ['2013-01-01' , '2013-07-01' ] , 
			 ['2013-07-01' , '2014-01-01' ] ,
			 ['2014-01-01' , '2014-07-01' ] , 
			 ['2014-07-01' , '2015-01-01' ] ,
			 ['2015-01-01' , '2015-07-01' ] , 
			 ['2015-07-01' , '2016-01-01' ] ,
			 ['2016-01-01' , '2016-07-01' ] , 
			 ['2016-07-01' , '2017-01-01' ] ,
			 ['2017-01-01' , '2017-07-01' ] ,
];

for indexDate , date in enumerate(date_list) :
	startDate = date[0];
	endDate = date[1];
	endDate_real = endDate;
	stock_len = len(stock_list);

	for index , stock in enumerate(stock_list) :
		if debug : print index , stock;
		data = get_stock_info( stock[0] );
		print_info( data , index ,version);
		if debug : print "=====",
	if debug : print ;

	print "=====From===== : " , startDate  , " to " , endDate_real ;
	print "HSI Close: " , get_hsi_info();
	if debug == 0 : 
		for nCount in stock_list :
			print nCount;

	if version == 1 :
		nLenCount = indexDate+1
	else :
		nLenCount = 1;


	print "Final Money : " , init_money_total ;
	print "Profit Money : " , init_money_total - init_money_single * stock_len * nLenCount ;
	print "Profit Percent : " , \
		round( init_money_total / (init_money_single * stock_len * nLenCount )  , 4) - 1 ;
#	print "==========";
	time.sleep(0.5);

#print "Final Money : " , init_money_total ;





