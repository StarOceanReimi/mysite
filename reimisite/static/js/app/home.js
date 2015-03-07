define(['app/imageviewer'], function(ImageViewer){
    return {
        init : function (){
            new ImageViewer({el : '.test', url: '/popularimages'});
        }
    };
});
