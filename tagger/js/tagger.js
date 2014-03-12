function Tagger(){
	var self = this,
			trainingDataRef = new Firebase('https://duckface.firebaseio.com/training'),
			faceppKey = '83c6d84242b88722bbd88bb2000af93e',
			faceppSecret = 'Tuoci57URDmmzD_IArfn3xSVxziVGb9K'

	var faceppUrl = 'http://apius.faceplusplus.com/v2/detection/detect'


	function fetchAndSaveFaceppData(id, entry){
		$.get(faceppUrl, {
				api_key: faceppKey,
				api_secret: faceppSecret,
				url: entry.url
			}, function(data){
				var trainedDataRef = trainingDataRef.child(id).child('facepp_detect')
				trainedDataRef.set( data )
				console.log( "RETURN DATA", data )
			})
	}

	this.populateFaceppJson = function( ){
		trainingDataRef.on('value', function(snapshot){
			var entries = snapshot.exportVal()

			_(entries).each(function(value, key){
				if( !value.facepp_detect ){
					fetchAndSaveFaceppData( key, value )	
					console.log( value, key )
				}
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

			if( entry.facepp_detect ) {
				img.addClass( 'hasFaceppJson' )
			}
		})
	}

	self.getEntries( self._displayEntries )
	self.populateFaceppJson()
}


var tagger = new Tagger()