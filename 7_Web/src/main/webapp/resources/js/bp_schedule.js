$(document).ready(function() {
		
	var data = null;
	var token = $("meta[name='_csrf']").attr("content");
	var header = $("meta[name='_csrf_header']").attr("content");
	
	$(document).ajaxSend(function(e, xhr, options) {
        xhr.setRequestHeader(header, token);
    });
	
	$.ajax({
		url : $("#contextPathURL").val() + "/schedule/get",
		type : 'GET',
		contentType : 'application/x-www-form-urlencoded; charset=UTF-8',
		dataType : 'json',
		success : function(result) {
			var data = [];
			$(result).each(function(i, j){
				// ISO 날짜형식으로 변환
				Date.prototype.toIsoString = function() {
				    var tzo = -this.getTimezoneOffset(),
				        dif = tzo >= 0 ? '+' : '-',
				        pad = function(num) {
				            var norm = Math.floor(Math.abs(num));
				            return (norm < 10 ? '0' : '') + norm;
				        };
				    return this.getFullYear() +
				        '-' + pad(this.getMonth() + 1) +
				        '-' + pad(this.getDate()) +
				        'T' + pad(this.getHours()) +
				        ':' + pad(this.getMinutes()) +
				        ':' + pad(this.getSeconds()) +
				        dif + pad(tzo / 60) +
				        ':' + pad(tzo % 60);
				}
				
				data[i] = j;
				var start = new Date(j.start).toIsoString().replace('T00:00:00+09:00','');
				var end = new Date(j.end).toIsoString().replace('T00:00:00+09:00','');
				data[i].start = start;
				data[i].end = end;
				data[i].id = j.calSerialNo;
				data[i].allDay = false;
				console.log(start);
				console.log(end);
			});
			
			createCal(data);
		}
	});
	
});

function createCal(data) {
	
	$('#calendar').fullCalendar({
		 themesystem : 'Darkly',
	      header: {
	        left: 'prev,next today',
	        center: 'title',
	        right: 'month,agendaWeek,agendaDay'
	      },
	      defaultDate: null,
	      themeSystem:'bootstrap4',
	      themeName:'darky',
	      navLinks: true, // can click day/week names to navigate views
	      editable: true,	
	      eventLimit: true, // allow "more" link when too many events
	      dayClick: function(date, jsEvent, view) {
	    	    $('#selectDate').val(moment(date).format('YYYY-MM-DD[T]HH:mm')); // ISO DATE
//	    	    $('#calSerialNo').val();	
	    	    // change the day's background color just for fun
	    	    $(this).css('background-color', 'blue');
	    	    $('#moveForm').submit();

	    	  },
    	  eventClick: function(calEvent, jsEvent, view) {

    		    $('#calSerialNo').val(calEvent.id);
    		    $('#moveForm').attr('action', $("#contextPathURL").val()+'/schedule/detail');
    		    $('#moveForm').submit();
    		    $(this).css('border-color', 'red');
    		  },
	      events: data
  });
	
}
