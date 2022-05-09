$(document).ready(function() {

	$('form').on('submit', function(event) {
        var rupees = $('input[name="r[]"]').map(function(){ return this.value; }).get();
        var sens = $('input[name="s[]"]').map(function(){ return this.value; }).get();
        var spec = $('input[name="c[]"]').map(function(){ return this.value; }).get();

        var b = $('#budgetInput').val();
        
        console.log(rupees)
        console.log('Budget')
        console.log(b)
        console.log(sens)
        console.log(spec)

		$.ajax({
			data : {
				budget : b,
				r : rupees,
                s : sens,
                c : spec
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			if (data.error) {
                let placeholder = document.querySelector('#dataoutput');  
                placeholder.innerHTML =  "<p></p>";
				$('#errorAlert').text(data.error).show();
			}
			else {
                let placeholder = document.querySelector('#dataoutput');  
                let out = "<h3>Optimal allocation</h3><p><table> <tr> <th bgcolor=\"wheat\">Testing kit</th> <th bgcolor=\"wheat\">Num</th> </tr>";
                for( let k of data.kit ){
                    out += "<tr>";
                    out += "<td>"+k.id+"</td>";
                    out += "<td>"+k.num+"</td>";
                    out += "</tr>";
                }
                out += "</table></p>";
                out += "<p>Std. error: "+data.stderror+"</p>";
                placeholder.innerHTML =  out;
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
