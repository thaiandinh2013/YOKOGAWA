##########################################
#For this question , I worked on the assumption that we have a csv file in our local computer
# we load it to HDFS first then the method below will create a table in Hbase with a single 
# column family , here denoted as cf1. 

#This function can be used to upload both the transaction and relationship file, but since I wrote this 
#function mainly for the transaction.csv so if it is implemented for the relationship file, ideally the header should be removef. 

# Variables in the function 
	
	#path :the path to the file, for example :/user/thaiantamk9454/.jarHives/
	#filename : name of the csv file. for example transaction.csv
	#table _name : name of the table we want to create in Hbase
#I have employed  some of the python libraries, so please make sure that they are installed 
#For the library pydoop, please set JAVA_HOME by the following command 
#export JAVA_HOME=/usr/lib/jvm/java/ or export JAVA_HOME=/usr/lib/jvm/jre-1.7.0 or export JAVA_HOME=/usr/lib/jvm/jre-1.7.0-openjdk.x86_64/
create a schema in hbase 
hbase shell 
create 'transaction', 'cf1'
create 'relationship', 'cf1'

def import_hbase(path, filename,table_name):
	import pandas as pd 
	import pydoop.hdfs as hd
	import happybase
	import csv
	import os

	path_filename=path+filename
	with hd.open(path_filename) as f:
		df =  pd.read_csv(f,header=None)
    
	# Please adjust the HOST and PORT arguements accordingly    		
   	connection = happybase.Connection('HOST','PORT')
	connection.open()
	
   
 	connection.create_table(table_name,
    {'cf1': dict()})

	table = connection.table(table_name)

	numrow=df.shape[0]
 	numcol=df.shape[1]

 	dict_trans={}
	for i in range(0, numrow):
		for j in range(0,numcol):
		# If a cell is not null, we all it into the dictionary 
			if pd.isnull(df.ix[i,j])==False:
				dict_trans['cf1'+':'+'c'+str(j+1)]=str(df.ix[i,j])
	# Put the key value pairs into the table. 	
		table.put(str(i),dict_trans)
		dict_trans={}



##########################################################################
## For simple file such as relationship, the file can be store easily to Hbase 
##using other components in the Hadoop eco system such as PIG 

##Using PIG
#Create a table in Hbase 
hbase shell
create 'transaction', 'cf1'

# Open PIG Shell
pig

relationship = LOAD '/home/relationship.csv' USING PigStorage( ',' ) AS ( product1: chararray, product2: chararray);

STORE relationship INTO 'hbase://relationship' USING
org.apache.pig.backend.hadoop.hbase.HBaseStorage ('cf1:product1 , cf2:product2');
