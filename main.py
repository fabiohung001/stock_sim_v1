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
		#if debug : print data["query"]["results"]["quote"];
		for day_quote in reversed(data["query"]["results"]["quote"]) :
			if nLoop == 0 or nLoop == len(data["query"]["results"]["quote"]) - 1 :
				if debug :
					print "Date : " , day_quote["Date"];
					print "Close : " , day_quote["Close"];

				if nLoop == 0 :
#					Price_start = day_quote["Close"];
					#set buy_in_price
					if stock_list[stock_idx][2] == 0 :
						stock_list[stock_idx][2] = day_quote["Close"];
						Price_start = stock_list[stock_idx][2];
					else :
						Price_start = stock_list[stock_idx][3];

				elif nLoop == len(data["query"]["results"]["quote"]) - 1 :
					Price_End = day_quote["Close"];
					endDate_real = day_quote["Date"];
					stock_list[stock_idx][3] = day_quote["Close"];
			#lowest
			if float(stock_list[stock_idx][4]) > float(day_quote["Low"]) or stock_list[stock_idx][4] == 0 :
				stock_list[stock_idx][4] = day_quote["Low"];
			#highest
			if float(stock_list[stock_idx][5]) < float(day_quote["High"]) :
				stock_list[stock_idx][5] = day_quote["High"];

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

def get_stock_list():
	global stock_list;
	#print "stock_no\tvalue\t\tbuy\tclose\tlowest\thighest";
	print '{: <10}'.format("stock_no") , '{: ^10}'.format("value") ,
	print '{: ^10}'.format("buy") , '{: ^10}'.format("close") ,
	print '{: ^10}'.format("lowest") , '{: ^10}'.format("highest");
	for nCount in reversed( sorted( stock_list , key = lambda x:( x[1]) ) ) :
		for index , nItem in enumerate(nCount) :
			if index == 1 :
				print '{: <10}'.format('{:8.2f}'.format(nItem)) ,
			elif index != 0 :
				print '{: <10}'.format('{:8.2f}'.format(float(nItem))) ,
			else :
				print '{: <10}'.format(nItem) ,
		print ;




init_money_total = 0.0;
init_money_single = 10000.0;
version = 0 ; #version  0 =  only one init money ; 1 = add money every count
startDate_real = 0;

#stock_no , init_money , buy_in_price , close_price ,lowest , highest

stock_list = [ 	
				["0001.hk" , init_money_single , 0 , 0  , 0 , 0],  
				["0005.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0700.hk" , init_money_single , 0 , 0  , 0 , 0],
				["3888.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0823.hk" , init_money_single , 0 , 0  , 0 , 0],
				["2208.hk" , init_money_single , 0 , 0  , 0 , 0],
				["1211.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0268.hk" , init_money_single , 0 , 0  , 0 , 0],
				["1766.hk" , init_money_single , 0 , 0  , 0 , 0],
				["2800.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0388.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0806.hk" , init_money_single , 0 , 0  , 0 , 0],
			] ;
'''
#hkconsumer's stock_list , 
#credit from http://hkconsumer.blogspot.hk/search/label/%E4%BA%94%E5%8D%81%E8%90%AC%E5%AF%A6%E6%88%B0%E5%80%89
stock_list_hkconsumer = [
			 	["2018.hk" , init_money_single , 0 , 0  , 0 , 0],  
				["0823.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0011.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0939.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0388.hk" , init_money_single , 0 , 0  , 0 , 0],
			] ;

#visimon's stock_list ,
#credit from http://visimon.blogspot.hk/search/label/%E5%83%B9%E5%80%BC%E6%8A%95%E8%B3%87%E5%80%89
stock_list_visimon = [
			 	["0016.hk" , init_money_single , 0 , 0  , 0 , 0],  
				["1398.hk" , init_money_single , 0 , 0  , 0 , 0],
				["1044.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0857.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0083.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0005.hk" , init_money_single , 0 , 0  , 0 , 0],
				["0001.hk" , init_money_single , 0 , 0  , 0 , 0],
				["3988.hk" , init_money_single , 0 , 0  , 0 , 0],
				["2128.hk" , init_money_single , 0 , 0  , 0 , 0],
			] ;
 
#purposelife42583's stock_list ,
#credit from http://purposelife42583.blogspot.hk/search/label/%E8%B6%B3%E7%90%83%E9%99%A3%E5%AE%B9%E6%8A%95%E8%B3%87%E6%B3%95
#todo

#stock_list = stock_list_visimon[:] ;
'''

#startDate , endDate			
date_list = [

#			 ['2007-01-01' , '2007-07-01' ] , 
#			 ['2007-07-01' , '2008-01-01' ] ,
#
#			 ['2007-11-01' , '2008-01-01' ] , # highest of 2007
#
#			 ['2008-01-01' , '2008-07-01' ] , 
#			 ['2008-07-01' , '2009-01-01' ] ,
#
#			 ['2008-10-27' , '2009-01-01' ] , #lowest of 2018
#
#			 ['2009-01-01' , '2009-07-01' ] , 
#			 ['2009-07-01' , '2010-01-01' ] ,
#			 ['2010-01-01' , '2010-07-01' ] , 
#			 ['2010-07-01' , '2011-01-01' ] ,
#			 ['2011-01-01' , '2011-07-01' ] , 
#			 ['2011-07-01' , '2012-01-01' ] ,
#			 ['2012-01-01' , '2012-07-01' ] , 
#			 ['2012-07-01' , '2013-01-01' ] ,
#			 ['2013-01-01' , '2013-07-01' ] , 
#			 ['2013-07-01' , '2014-01-01' ] ,
#			 ['2014-01-01' , '2014-07-01' ] , 
#			 ['2014-07-01' , '2015-01-01' ] ,
#			 ['2015-01-01' , '2015-07-01' ] ,
#
			 ['2015-04-27' , '2015-07-01' ] , # highest of 2015
#
			 ['2015-07-01' , '2016-01-01' ] ,
			 ['2016-01-01' , '2016-07-01' ] ,
#
#			 ['2016-02-12' , '2016-07-01' ] , #lowest of 2016 
#
			 ['2016-07-01' , '2017-01-01' ] ,
			 ['2017-01-01' , '2017-07-01' ] ,
];

for indexDate , date in enumerate(date_list) :
	startDate = date[0];
	if startDate_real == 0 : startDate_real = startDate;
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
	get_stock_list()

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

#get_stock_list();
print "=====From===== : " , startDate_real  , " to " , endDate_real  , " version : " , version;
print "Pincipal :  " , init_money_single * stock_len * nLenCount ;
print "Final Money : " , init_money_total ;





