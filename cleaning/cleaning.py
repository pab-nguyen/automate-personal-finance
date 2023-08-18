# %%
import os
import glob
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType,BooleanType,DateType,IntegerType,DoubleType
from pyspark.sql.window import Window
import pyspark.pandas as ps
#create spark Session
spark = SparkSession.builder.appName("PF").config("spark.sql.caseSensitive", "True").getOrCreate()
# %%
#read master ledger file, this file will also be the output of this notebook
#read using pandas then convert to spark dataframe
print('Hello')
df_out = spark.createDataFrame(pd.read_excel('./data/other_input/Master Ledger.xlsx',sheet_name="Master Ledger"))
print(type(df_out))
print('Hello1')

#change column type to the appropriate type
df_out = df_out.withColumn("ID",col("ID").cast(IntegerType()))\
        .withColumn("Amount",col("Amount").cast(DoubleType()))\
        .withColumn("Subscriptions",col("Subscriptions").cast(BooleanType()))\
        .withColumn("Return",col("Return").cast(BooleanType()))\
        .withColumn("Real Amount",col("Real Amount").cast(DoubleType()))
#change format of Date
df_out = df_out.withColumn("Date",to_date(col("Date"),"MM/dd/yyyy"))

#print Schema
# df_out.printSchema()

#drop all rows that don't have any ID, fill NaN with blank
df_out = df_out.dropna(how="all",subset= ["ID"]).drop('ID','Limit')
df_out = df_out.replace('NaN',"")
#show dataframe
df_out.orderBy("ID", ascending=False)

# %%
#read all supplementary inputs
acc_meta = spark.read.options(inferSchema='True',header='True').csv('./data/other_input/account_metadata.csv')
inv_bal = spark.read.options(inferSchema='True',header='True').csv('./data/other_input/investment_balance.csv')

#create a category mapping based on past data to auto-assign category
category_map = df_out.groupby(['Account','Item','Categories','Categories 2','Transaction Type']).count().orderBy('count',ascending=False)


# %%
#read all csv files exported from Empower, merge into one spark dataframe
path = glob.glob('./data/empower_input/*.csv')
emp_data = spark.read.options(inferSchema='True',header='True').csv(path)


#add more columns to emp_data (all empower transactions), so that it matches columns in df_out (master ledger)
emp_data = emp_data.join(acc_meta,on='Account')\
.drop("Limit")\
.filter(~(col('Account Type') == "Investment"))\
.withColumn("Item",col("Description")).drop("Description")\
.withColumn("Real Amount",col("Amount"))\
.withColumn("Amount",abs(col("Amount")))\
.withColumn("Transaction Type",when(col("Real Amount") <0, "Expense").otherwise("Income"))\
.drop("Category")\
.withColumn("Owner",lit(None))\
.withColumn("Subscriptions",lit(False))\
.withColumn("Return",lit(False))\
.drop("Tags")\

#print schema and show
# emp_data.printSchema()
# emp_data.orderBy("Date", ascending=False).show()

# %%
#find the latest date in master ledger file
max_date = df_out.select(max("Date")).first()[0]

# union master ledger with empower, where the empower dataframe is filtered on max_date - 5. 
# This is to ensure it captures all transactions, because sometimes the transactions are updated few days after, so 5 days is a good limit. 
df_out = df_out.unionByName(emp_data.filter(col("Date")> lit(max_date)-5), allowMissingColumns=True)
df_out = df_out.drop("Account Type","Owner","Statement Day").join(acc_meta, on = 'Account').na.fill("")

#auto-assign category using category mapping 
category_map = df_out.filter(col("Categories") == lit("")).drop('Categories','Categories 2').join(category_map, on=['Account','Item','Transaction Type'], how='left')
df_out = df_out.filter(~(col("Categories") == lit(""))).unionByName(category_map, allowMissingColumns=True).drop('count')

#further drop duplicates, in case the Note column are already filled using window partition
#group all transactions which have the same date, account, item and amount into a partition, then assign row number
#if any of them has row_number value higher than 1, and their Note columns is blank, indicate these as dup and filter them out
window = Window.partitionBy(['Date','Account','Item','Real Amount']).orderBy(col("Note").desc())
df_out = df_out.withColumn("row_number",row_number().over(window))\
    .withColumn('dup',when((col('row_number')>1) & (col('Note') == ""),True).otherwise(False))\
    .filter(col('dup') == False)\
    .drop("row_number","dup")
    

# check investment accounts balance, insert transactions to change 
df_inv_sum = df_out.filter(col('Account Type') == 'Investment')\
    .groupBy('Account')\
    .agg(sum('Real Amount').alias("Old Balance"))\
    .join(inv_bal, on='Account')\
    .withColumn('Real Amount', col('Balance')- col('Old Balance'))\
    .filter(col('Real Amount') != 0)\
    .withColumn('Item', lit('Adjustment'))\
    .withColumn('Amount', abs(col('Real Amount')))\
    .withColumn('Date', col('Last Updated'))\
    .withColumn('Categories', lit('Investment'))\
    .withColumn('Categories 2', lit('Balance Change'))\
    .withColumn('Transaction Type', when(col('Real Amount')>0,lit('Income3')).otherwise(lit('Expense3')))\
    .withColumn('Note', lit(None))\
    .withColumn('Subscriptions', lit(False))\
    .withColumn('Return', lit(False))\
    .join(acc_meta, on='Account')\
    .drop('Last Updated','Balance', 'Old Balance')

df_out = df_out.unionByName(df_inv_sum).orderBy("Date")

# %%
#export to csv and add column ID
df_out.toPandas().to_csv("./data/output/out.csv", index_label="ID")


