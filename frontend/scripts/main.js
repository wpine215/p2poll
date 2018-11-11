$(document).ready(function() {
    $('.ui.radio.checkbox')
        .checkbox()
    ;

    $("#submitvote").click(function(){
        var voterid = document.getElementById("idnum").value;
        var choices = document.getElementsByName("candidate");
        var vote = '';
        for(var i = 0; i < choices.length; i++){
            if(choices[i].checked){
                vote = choices[i].value;
                break;
            }
        }

        if (voterid == '') {
            alert("Please enter a valid voter ID.")
        }
        else if (vote == '') {
            alert("Please vote for a candidate.")
        }
        else {
            var input = {
                "voterid": voterid,
                "vote": vote
            }
            $.ajax({
                type: "post",
                data: input,
                cache: false,
                dataType: "text",
                error: function(xhr, status, error) {
                    var err = eval("(" + xhr.responseText + ")");
                    alert(err.Message);
                },
                success: function(result) {
                    alert("time to validate :D");
                }
            })
            document.getElementById("validation").style.display = "block";
        }
    });

    $("#submitvalidate").click(function(){
        alert("Thank you for voting! :)");
    });

    $("#viewvote").click(function(){
        var voterid = document.getElementById("voterid").value;
        if (voterid == '') {
            alert("Please enter a valid voter ID.")
        }
        else {
            alert(voterid);
            document.getElementById("yourVote").innerHTML = "You voted for...";
            /*$.ajax({
                type: "post",
                data: {"voterid": voterid},
                cache: false,
                dataType: "text",
                error: function(xhr, status, error) {
                    var err = eval("(" + xhr.responseText + ")");
                    alert(err.Message);
                },
                success: function(result) {
                    document.getElementById("yourVote").innerHTML = "You voted for " + result + ".";
                }
            })*/
        }
    });
})

