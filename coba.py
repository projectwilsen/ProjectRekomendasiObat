$.ajax({
    type: 'post',
    url: 'https://cekbpom.pom.go.id/prev_next_pagination_obat',
    headers: {'X-Requested-With': 'XMLHttpRequest'},
    data: { 
    		offset : 1,
    		next_prev : 10,
    		count_data_obat : 24703, 
    		marked : 'next'
    	},
    	success:function(data){
    		var data = JSON.parse(data);
            console.log(data);}})