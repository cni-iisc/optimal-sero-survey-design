$(document).ready(function() {



    // setting the input field as editable based on option selected
    $('input:radio[name="option"]').change(function(){
        if($(this).val() == 'cost'){
          $("label[for='margin']").text("Margin of error");
          $("label[for='budget']").text("Budget (₹)");
          $("#budget").prop('readonly', true);
          $("#margin").prop('readonly', false);
        }
        if($(this).val() == 'error'){
          $("label[for='margin']").text("Margin of error");
          $("label[for='budget']").text("Budget (₹)");

          $("#budget").prop('readonly', false);
          $("#margin").prop('readonly', true);
        }
    });

	$('form').on('submit', function(event) {
        var rupees = $('input[name="r[]"]').map(function(){ return this.value; }).get();
        var sens = $('input[name="s[]"]').map(function(){ return this.value; }).get();
        var spec = $('input[name="c[]"]').map(function(){ return this.value; }).get();

        var b = $('#budget').val();
        var mar = $('#margin').val();


        var option = 0;
        if(document.getElementById('option1').checked) {
            option = 1;
        } else if(document.getElementById('option2').checked) {
            option = 2;
        }

        console.log("Rupees:",rupees)
        console.log('Budget')
        console.log(b)
        console.log(sens)
        console.log(spec)
        console.log(mar)
        console.log(option)

		$.ajax({
			data : {
				budget : b,
				r : rupees,
                s : sens,
                c : spec,
                m : mar,
                opt: option
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
                let out = "<h3>Optimal allocation</h3><p><table> <tr> <th bgcolor=\"wheat\">Testing kit</th> <th bgcolor=\"wheat\">Number of tests</th> <th bgcolor=\"wheat\">Total Cost ( &#8377;  )</th> </tr>";
                for( let k of data.kit ){
                    out += "<tr style=\"border-bottom: 1px solid wheat;\"  >";
                    out += "<td>"+"Kit #"+k.id+"</td>";
                    out += "<td>"+k.num+"</td>";
                    out += "<td>"+k.alloc+"</td>";
                    out += "</tr>";
                }
                out += "</table></p>";
                out += "<p><h4>Margin of error: "+data.stderror+"</h4></p>";
                placeholder.innerHTML =  out;
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
