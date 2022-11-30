var BASE_URL = 'https://7r7j5qj4rf.execute-api.us-east-1.amazonaws.com/dev';

function updateWordCloud() {
    $.ajax({
        type: 'GET',
        url: BASE_URL + '/cloud-tag'
    })
    .done(function(labels) {
        var words = labels.map(function(label) {
		return {
			text: label.tag,
			weight: label.score,
			link: 'category.html?cat=' + label.tag
		};
        });
        $('#word-cloud').jQCloud('update', words);
    })
}

function wordCloudIntervalStart() {
    updateWordCloud();
    wordCloudInterval = setInterval(updateWordCloud, 120 * 1000);
}

function wordCloudIntervalClear() {
    clearInterval(wordCloudInterval);
}

function inputFileChange() {
    var filename = $('#input-image').val().split('\\').pop();
    if (filename.length) {
        $('#input-image').next('.custom-file-label').addClass("selected").html(filename);
        $('#upload-image').prop('disabled', false);
    } else {
        $('#input-image').next('.custom-file-label').removeClass("selected").html('Choose file...');
    }
}

function inputFileClear() {
    $('#input-image').next('.custom-file-label').removeClass("selected").html('Choose file...');
    $('#upload-image').prop('disabled', true);
}

function getSignedUrlAndSend(e) {
    e.preventDefault();

    var filedata = $('#input-image').get()[0].files[0];
    inputFileClear();
    $.ajax({
        type: 'GET',
	url: BASE_URL + '/signed-url'
    })
    .done(function(data) {
        sendFile(data.url, filedata);
    })
    .fail(function(err) {
        alert('File NOT uploaded');
    });
    return false;
}

function sendFile(url, filedata) {
    wordCloudIntervalClear();
    $.ajax({
        type: 'PUT',
        url: url,
        contentType: 'image/jpeg',
        processData: false,
        data: filedata
    })
    .done(function(e) {
        alert('File uploaded');
    })
    .fail(function(arguments) {
        alert('File NOT uploaded');
        console.log( arguments);
    })
    .always(function() {
        setTimeout(wordCloudIntervalStart, 5 * 1000);
    });

    return false;
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function updateCategory() {
    var category = getParameterByName('cat');
    $('#category').text(decodeURIComponent(category));
}

function getCategoryImg() {
    var category = getParameterByName('cat');
    $.ajax({
        type: 'GET',
        url: BASE_URL + '/category/' + category
    })
    .done(function(data) {
        $('#image').attr('src', data.url);
    })
    .fail(function(err) {
        console.log(err);
    });
    return false;
}

function isCategoryView() {
    return window.location.href.indexOf('category.html') >= 0;
}

var wordCloudInterval = null;
if (isCategoryView()) {
    updateCategory();
    getCategoryImg();
} else {
    $('#input-image').on('change', inputFileChange);
    $('#upload-image').on('click', getSignedUrlAndSend);
    $('#word-cloud').jQCloud([], {autoResize: true});
    wordCloudIntervalStart();
}
