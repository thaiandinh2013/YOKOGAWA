## Begin to build the model using association rules
//load the file in to R , execute these command and open 
file<-read.csv(file.choose())

// take out all the distinct of product 2 
product2<-unique(file$Product2)

//Initiate an empty data frame to store the result 
result <- data.frame(matrix(ncol = 6, nrow = 0))

colnames(result)<-c("lhs","","rhs", "support", "confidence","lift" )

for(i in 1:length(product2)){
	temp<-file[file$Product2==product2[i],]
	if(dim(temp)[1]>0){
		rules <- apriori(temp)
		tempresult<-inspect(rules)
		result<-rbind(result,tempresult)
	}

}

dim(result)
//Post - process the result and put in a desired format 

require(stringr)
result<-result[str_length(result[,1])>2,]
result<-result[str_detect(result[,1],"Product1")==TRUE,]

//Initiate a new data frame to store the final result 
final_result <- data.frame(matrix(ncol = 2, nrow = dim(result)[1]))

colnames(final_result)<-c("Product1","Product2" )


final_result$Product1<-substr(result[,1],11,13)
final_result$Product2<-substr(result[,3],11,13)

write.csv(final_result,"finalresult.csv")
write.csv(result,"rawresult.csv")
