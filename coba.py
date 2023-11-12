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


$.ajax({
						type: 'post',
						url: 'https://cekbpom.pom.go.id/prev_next_pagination_obat',
						headers: {'X-Requested-With': 'XMLHttpRequest'},
						data: { 
								offset : 17031,
								next_prev : 17040,
								count_data_obat : 24703, 
								marked : 'next'
							},
							success:function(data){
								var data = JSON.parse(data);
								offset = data.offset;
								next_prev = data.next_prev;
								count_data_obat = data.count_data_obat.JUMLAH;


								$('.paginggall span').remove();
								$('.paginggall').append('<span class="kt-inbox__perpage" data-toggle="dropdown">'+data.offset+' - '+data.next_prev+' dari '+count_data_obat+ ' Data ' + '</span>');

								$('#inbox-list div').remove();
								$('#inbox-list hr').remove();
								
								$.each(data.data_obat, function(index, element) {
									var param = element.PRODUCT_ID+'*'+element.APPLICATION_ID;
									var eOnclick = "get_detail('"+param+"')";
									var eOnclick1 = "aksi_produk('"+btoa('hapus_produk*'+param)+"')";
									var eOnclick2 = "aksi_produk('"+btoa('berlaku_produk*'+param)+"')";
									var eOnclick3 = "aksi_produk('"+btoa('berlakubulk_produk*'+param)+"')";
									var eOnclick4 = "aksi_produk('"+btoa('ekspor_produk*'+param)+"')";
									var eOnclick5 = "aksi_produk('"+btoa('dicabut_perusahaan_produk*'+param)+"')";
									var eOnclick6 = "aksi_produk('"+btoa('dicabut_mutu_produk*'+param)+"')";
									var eOnclick7 = "aksi_produk('"+btoa('dicabut_sesuai_produk*'+param)+"')";
									var eOnclick8 = "aksi_produk('"+btoa('batal_produk*'+param)+"')";
									var eOnclick14 = "aksi_produk('"+btoa('produk_warning_new*'+param)+"')";
									var eOnclick9 = "aksi_produk('"+btoa('ubah_warning_produk*'+param)+"')";
									var eOnclick10 = "aksi_produk('"+btoa('rilis_warning_produk*'+param)+"')";
									var eOnclick11 = "aksi_produk('"+btoa('draft_warning_produk*'+param)+"')";
									var eOnclick12 = "aksi_produk('"+btoa('hapus_warning_produk*'+param)+"')";
									var eOnclick13 = "aksi_produk('"+btoa('input_recall_produk*'+param)+"')";

									if (sessionlogin == 1) {
										if (element.APPLICATION_ID == 2) {
											var status2 = element.STATUS2;
										}
										else{
											var status2 = "";
										}

										if (data.arrproc == 'isread_iswarn') {
											$('#inbox-list').append(
												'<div class="kt-inbox__item kt-inbox__item--unread" data-id="2" data-type="inbox">' +
												'<div class="kt-inbox__info" style="margin: auto">' + '<div class="kt-inbox__sender" onclick='+eOnclick+' data-toggle="view">' + '<span class="kt-media kt-media--sm kt-media--danger" data-toggle="kt-tooltip" title="Obat">'+ '<span>'+ 'OB' + '</span>' + '</span>' + '</div>' + '</div>' + 
												'<div class="dropdown" style="margin: auto">' +
												'<button type="button" class="btn btn-primary btn-icon btn-sm" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
												'<i class="flaticon-more-v2"></i>' +
												'</button>' +
												'<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick+'>Detail</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick1+'>Hapus</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick2+'>Berlaku</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick3+'>Berlaku Bulk</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick4+'>Berlaku Khusus Ekspor</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick5+'>Dicabut Atas Permohonan Perusahaan</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick6+'>Dicabut Karena Keamanan Mutu</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick7+'>Dicabut Karena Data Tidak Sesuai</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick8+'>Dicabut/Dibatalkan</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick14+'>Input Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick9+'>Ubah Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="https://cekbpom.pom.go.id/produk_warning_upload">Upload Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick10+'>Rilis Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick11+'>Draft Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick12+'>Hapus Public Warning</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick13+'>Input Recall Baru</a>' +
												'</div>' +
												'</div>' + 
												'<div class="kt-inbox__details" onclick='+eOnclick+' data-toggle="view" style="width: 180px; min-width: 180px; max-width: 180px ; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_ID + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ element.SUBMIT_DATE + '<br>' + element.PERMOHONAN + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" onclick='+eOnclick+' data-toggle="view" style="width: 180px; min-width: 180px; max-width: 180px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_REGISTER + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ element.PRODUCT_DATE + '<br>' + element.PRODUCT_EXPIRED + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" onclick='+eOnclick+' data-toggle="view" style="width: 350px; min-width: 350px; max-width: 350px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_NAME + '</span>' + '&nbsp;'+ '<br>'+ '<span class="kt-inbox__summary">' + element.PRODUCT_BRANDS + '<br>' + element.PRODUCT_PACKAGE + '</span>' +
												'</div>' +
												'</div>' + 
												'<div class="kt-inbox__details" data-toggle="view" style="width: 300px; min-width: 300px; max-width: 300px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">' + (element.PENDAFTAR==null?'':element.PENDAFTAR) + '</span>' + '<br>' + '<span class="kt-inbox__summary">' + element.NPWP_PENDAFTAR + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" data-toggle="view" style="width: 131px; min-width: 131px; max-width: 131px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">' + element.STATUS + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ status2 + '</span>' +
												'</div>' +
												'</div>' +
												'</div>' +
												'<hr>'
												);
										}
										else if(data.arrproc == 'iswarn'){
											$('#inbox-list').append(
												'<div class="kt-inbox__item kt-inbox__item--unread" data-id="2" data-type="inbox">' +
												'<div class="kt-inbox__info" style="margin: auto">' + '<div class="kt-inbox__sender" onclick='+eOnclick+' data-toggle="view">' + '<span class="kt-media kt-media--sm kt-media--danger" data-toggle="kt-tooltip" title="Obat">'+ '<span>'+ 'OB' + '</span>' + '</span>' + '</div>' + '</div>' + 
												'<div class="dropdown" style="margin: auto">' +
												'<button type="button" class="btn btn-primary btn-icon btn-sm" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
												'<i class="flaticon-more-v2"></i>' +
												'</button>' +
												'<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick+'>Detail</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick14+'>Input Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick9+'>Ubah Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="https://cekbpom.pom.go.id/produk_warning_upload">Upload Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick10+'>Rilis Produk Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick11+'>Draft Public Warning</a>' +
												// '<a class="dropdown-item" href="javascript:;" onclick='+eOnclick12+'>Hapus Public Warning</a>' +
												'<a class="dropdown-item" href="javascript:;" onclick='+eOnclick13+'>Input Recall Baru</a>' +
												'</div>' +
												'</div>' + 
												'<div class="kt-inbox__details" onclick='+eOnclick+' data-toggle="view" style="width: 180px; min-width: 180px; max-width: 180px ; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_ID + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ element.SUBMIT_DATE + '<br>' + element.PERMOHONAN + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" onclick='+eOnclick+' data-toggle="view" style="width: 180px; min-width: 180px; max-width: 180px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_REGISTER + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ element.PRODUCT_DATE + '<br>' + element.PRODUCT_EXPIRED + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" onclick='+eOnclick+' data-toggle="view" style="width: 350px; min-width: 350px; max-width: 350px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_NAME + '</span>' + '&nbsp;'+ '<br>'+ '<span class="kt-inbox__summary">' + element.PRODUCT_BRANDS + '<br>' + element.PRODUCT_PACKAGE + '</span>' +
												'</div>' +
												'</div>' + 
												'<div class="kt-inbox__details" data-toggle="view" style="width: 300px; min-width: 300px; max-width: 300px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">' + (element.PENDAFTAR==null?'':element.PENDAFTAR) + '</span>' + '<br>' + '<span class="kt-inbox__summary">' + element.NPWP_PENDAFTAR + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" data-toggle="view" style="width: 131px; min-width: 131px; max-width: 131px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">' + element.STATUS + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ status2 + '</span>' +
												'</div>' +
												'</div>' +
												'</div>' +
												'<hr>'
												);

										}
										else{
											$('#inbox-list').append(
												'<div class="kt-inbox__item kt-inbox__item--unread" data-id="2" onclick='+eOnclick+' data-type="inbox">' +
												'<div class="kt-inbox__info" style="margin: auto">' + '<div class="kt-inbox__sender" data-toggle="view">' + '<span class="kt-media kt-media--sm kt-media--danger" data-toggle="kt-tooltip" title="Obat">'+ '<span>'+ 'OB' + '</span>' + '</span>' + '</div>' + '</div>' + 
												'<div class="kt-inbox__details" data-toggle="view" style="width: 180px; min-width: 180px; max-width: 180px ; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_ID + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ element.SUBMIT_DATE + '<br>' + element.PERMOHONAN + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" data-toggle="view" style="width: 180px; min-width: 180px; max-width: 180px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_REGISTER + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ element.PRODUCT_DATE + '<br>' + element.PRODUCT_EXPIRED + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" data-toggle="view" style="width: 350px; min-width: 350px; max-width: 350px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">'+ element.PRODUCT_NAME + '</span>' + '&nbsp;'+ '<br>'+ '<span class="kt-inbox__summary">' + element.PRODUCT_BRANDS + '<br>' + element.PRODUCT_PACKAGE + '</span>' +
												'</div>' +
												'</div>' + 
												'<div class="kt-inbox__details" data-toggle="view" style="width: 300px; min-width: 300px; max-width: 300px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">' + (element.PENDAFTAR==null?'':element.PENDAFTAR) + '</span>' + '<br>' + '<span class="kt-inbox__summary">' + element.NPWP_PENDAFTAR + '</span>' +
												'</div>' +
												'</div>' +
												'<div class="kt-inbox__details" data-toggle="view" style="width: 131px; min-width: 131px; max-width: 131px; padding-left: 7px">' +
												'<div class="kt-inbox__message">' +
												'<span class="kt-inbox__subject">' + element.STATUS + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ status2 + '</span>' +
												'</div>' +
												'</div>' +
												'</div>' +
												'<hr>'
												);
										}
										
									}
									else{

										$('#inbox-list').append(
											'<div class="kt-inbox__item kt-inbox__item--unread" data-id="2" onclick='+eOnclick+' data-type="inbox">' +
											'<div class="kt-inbox__info" style="margin: auto">' + '<div class="kt-inbox__sender" data-toggle="view">' + '<span class="kt-media kt-media--sm kt-media--danger" data-toggle="kt-tooltip" title="Obat">'+ '<span>'+ 'OB' + '</span>' + '</span>' + '</div>' + '</div>' + 
											'<div class="kt-inbox__details" data-toggle="view" style="width: 131px; min-width: 131px; max-width: 131px">' +
											'<div class="kt-inbox__message">' +
											'<span class="kt-inbox__subject">'+ element.PRODUCT_REGISTER + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ element.PRODUCT_DATE + '</span>' +
											'</div>' +
											'</div>' +
											'<div class="kt-inbox__details" data-toggle="view" style="padding-left: 140px">' +
											'<div class="kt-inbox__message">' +
											'<span class="kt-inbox__subject">'+ element.PRODUCT_NAME + '</span>' + '&nbsp;'+ '<br>'+ '<span class="kt-inbox__summary">' + element.PRODUCT_BRANDS + '<br>' + element.PRODUCT_PACKAGE + '</span>' +
											'</div>' +
											'</div>' + 
											'<div class="kt-inbox__details" data-toggle="view" style="min-width: 450px; max-width: 450px; padding-left: 7px">' +
											'<div class="kt-inbox__message">' +
											'<span class="kt-inbox__subject">' + element.PENDAFTAR + '</span>' + '<br>' + '<span class="kt-inbox__summary">'+ '-' + '</span>' +
											'</div>' +
											'</div>' +
											'</div>' +
											'<hr>'
										);
									}
								});

								$.unblockUI();
							}
						});		