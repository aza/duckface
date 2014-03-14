function Tagger(){
	var self = this,
			trainingDataRef = new Firebase('https://duckface.firebaseio.com/training')

	this.getEntries = function( callback ){
		trainingDataRef.once('value', function(snapshot){
			var entries = snapshot.exportVal()
			if(callback) callback( entries )
		})		
	}

	function mouseMove(e){
		var el = $(e.target)		
		
		if( e.offsetX >= el.width()/2 ) {
			el.addClass('isDuck').removeClass('notDuck')
		} else {
			el.removeClass('isDuck').addClass('notDuck')
		}
	}

	function mouseOut(e){
		var el = $(e.target)
		
		el.removeClass('isDuck').removeClass('notDuck')	
		
		if( el.attr('data-tag') ){
			el.addClass( el.attr('data-tag') )
		}
	}

	function mouseClick(e){
		var el = $(e.target)
		
		el.removeClass('notYetTagged')
			.attr('data-tag', el.hasClass('isDuck') ? 'isDuck' : 'notDuck')

		var id = el.attr('id'),
			  index = el.attr('data-index')
			  tag = el.attr('data-tag')
		trainingDataRef.child(id).child('tagged').child(index).set( tag )
	}

	this._displayEntries = function( entries ){
		$('.tagger').empty()
		var displayProbability = 1

		_(entries).each(function(entry, key){
			if( Math.random() >= displayProbability ) return
			var img = $('<img>')
				.addClass('face')
				.attr('src', entry.url)
				.attr('id', key )
				.appendTo('.tagger')

			if( entry.facepp_detect && entry.facepp_detect.face ) {
				img.addClass( 'hasFaceppJson' )
				_(entry.facepp_detect.face).each(function(face, index){
					var dot = $('<div>')
						.addClass('dot')
						.css({
							top: img.offset().top + .01*(face.position.center.y - face.position.height/2)*img.height(),
							left: img.offset().left + .01*(face.position.center.x - face.position.width/2)*img.width(),
							width: face.position.width*.01*img.width(),
							height: face.position.height*.01*img.width()
						})
						.appendTo('.tagger')
						.attr('id', key)
						.attr('data-index', index)
						.bind('mousemove', mouseMove)
						.bind('mouseout', mouseOut)
						.bind('click', mouseClick)

					if( entry.tagged ){
						var tag = entry.tagged[index]
						dot.addClass( tag ).attr('data-tag', tag)
					}
					else {
						dot.addClass('notYetTagged')
					}

					//console.log( face )
				})

			}
		})



	}

	$(function(){
		self.getEntries( self._displayEntries )	
	})
	
}


var tagger = new Tagger()