function Tagger(){
	var self = this,
			trainingDataRef = new Firebase('https://duckface.firebaseio.com/training')


	this.populateFaceppJson = function( ){
		trainingDataRef.on('value', function(snapshot){
			var entries = snapshot.exportVal()

			_(entries).each(function(value, key){
				console.log( value, key )
			})
		})
	}

	this.getEntries = function( callback ){
		trainingDataRef.on('value', function(snapshot){
			var entries = snapshot.val()
			if(callback) callback( entries )
		})		
	}

	this._displayEntries = function( entries ){
		$('.tagger').empty()

		_(entries).each(function(entry){
			var img = $('<img>')
				.addClass('face')
				.attr('src', entry.url)
				.appendTo('.tagger')

			if( entry.faceppJson ) {
				img.addClass( 'hasFaceppJson' )
			}
		})
	}

	self.getEntries( self._displayEntries )
	this.getNoDataEntries()
}


var tagger = new Tagger()