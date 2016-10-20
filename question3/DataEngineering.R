//House Keeping stuffs, installing all the package
install.packages(gbm)
require(gbm)
// Load data into R
transaction<-read.csv(file.choose(),header=FALSE,fill=TRUE)
head(transaction)

require(stringr)
//Because R does not take the empty cells as null values so one way we can check 
//for it is to compare the length of the string. Cells that does not have any
//transaction to have a string with length 0 whereas cells that does will have
//the length of 3


//Eliminate all the transaction that have only one product( the second columns
is empty)
transaction<-transaction[str_length(transaction[,2])==3,]

product1<-c()
product2<-c()
for(i in 1: dim(transaction)[1]){
	row_single<-as.character(unname(unlist(transaction[i,])))
	row_single<-row_single[str_length(row_single)==3]
	product1<-c(product1, as.character(row_single[1:length(row_single)-1]))
	product2<-c(product2, as.character(row_single[2:length(row_single)]))




write.csv(transaction_pairs,"transaction_pairs.csv")

}

// Initiate an empty data frame with two columns, product1 and product2

//Begin to attach the data into the transaction_pairs data frame 



transaction_pairs <- data.frame(matrix(ncol = 2, nrow = length(product1)))
colnames(transaction_pairs)<-c("Product1","Product2")

transaction_pairs$Product1<-as.factor(product1)
transaction_pairs$Product2<-as.factor(product2)


// Begin to build the model 

require(arules)
rules <- apriori(transaction_pairs)

 rules <- apriori(transaction_pairs,
appearance = Product2,
   default="lhs"),
  )

inspect(rules[1:20])









