requirejs.config({
    baseUrl: '/static/js',
    paths: {
        jquery : 'lib/jquery-1.11.2',
        'jquery-ui' : 'lib/jquery-ui.min', 
        underscore : 'lib/underscore',
        backbone : 'lib/backbone'
    },
    urlArgs: "bust=" + (new Date()).getTime()
});
