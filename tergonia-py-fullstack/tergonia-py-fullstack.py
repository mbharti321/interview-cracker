log -> 10 GB file -> parse -> return top 3 warnings


10gb /40 =500MB

uploads  on UI -> 
	app 1 -> divide file into chunks -> upload on blob storage

app2 -> blob trigger application -> read  -> parse -> line by line / using regex -> find the warnings -> write warnings in separate file with full time stamp
	chunk1 ---> reultFile
	chunk2 ---> reultFile
	chunk3 ---> reultFile -> 
	----------



database -> logfile data -> sourcefilename - chunkname -> processed(t/f) -> 


----app.post("/log_file")
def chunk_log_file(log_file, File()):

	max_size_file = 200
	
	open file()
		# get 
		# await chunk_log_files(log_file, max_size_file)
	

def chunk_log_files(log_file: File, max_file_size: int):	
	# check the file based on max





Interface

interface IMyService{
	eat();
	fly()
}



public class parrot: IMyService
{
	void DoTask1(){
	}

	void DoTask2(){
	}

} 

class peguin:IMyService


blob

IBlobService{

read(file)
upload(file)
}


Class blobService: IBlobService{
	read(file)
	upload(file)
}

IDisposable
delegate -> why?

add()
mul()
div()


cal(a,b, method){
	retun method(a,b)	
}

call(a,b, add)
call(a,b, mul)
call(a,b, div)






