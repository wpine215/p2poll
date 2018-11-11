// 2D array votes [index,voterid,pollid,value,date,blocknumber]
// Generate VOTES

votes = []
votes.push([1,12,14,'C',"Monday",1])

votes.push([2,13,13,'A',"Monday",2])
votes.push([3,14,14,'B',"Monday",3])
votes.push([4,12,14,'A',"Monday",4]) //changed vote!


votes.push([5,16,14,'A',"Monday",5])
votes.push([6,10,14,'B',"Monday",6])


pollnumber = 14; //change poll number

var voterDict = {}
var tally = {}


var rvotes = votes.reverse();
for (var k=0; k < votes.length; k++){
	if ((Object.keys(voterDict).includes("" + rvotes[k][1])) && rvotes[k][2] == pollnumber){
		continue;
	}
	else{     
		voterDict[rvotes[k][1]] = rvotes[k][3] 

		if ((Object.keys(tally).includes(rvotes[k][3]))&& rvotes[k][2] == pollnumber)	{
			
			tally[rvotes[k][3]] = tally[rvotes[k][3]] + 1;
		}
		else{
			tally[rvotes[k][3]] = 1;
		}	
    	// console.log(rvotes[k]);
    }
}


console.log(tally)