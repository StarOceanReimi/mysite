define(['jquery', 'underscore', 'backbone', 'text!templates/imageviewer.html', 'jquery-ui'], 
function($, _, Backbone, tpl){

    var ImageModel = Backbone.Model.extend({
        defaults : {
            title : '',
            desc : '',
            src : '',
            dest : ''
        }
    });    
    var Images = Backbone.Collection.extend({
        model : ImageModel
    }); 


    var images = new Images();
    var ImageViewer = function(config){

        _.extend(this, config);

        this.width = this.width || 768;
        this.height = this.height || 480;

        var ImageView = Backbone.View.extend({
            el : this.el, 
            events : {
                'click div#leftbtn' : 'prev',
                'click div#rightbtn' : 'next'
            },
            initialize : function(){
                _.bindAll(this, 'render', 'next', 'prev'); 
                this.tpl = _.template(tpl);
                this.index = 0;
                this.listenTo(this.model, 'load_complete', this.render);
                
                var self = this;
            },
            render : function(){
                var imgs = this.model.toJSON();
                html = this.tpl({width: this.width, height: this.height, images: imgs});
                $(this.el).empty();
                $(this.el).append(html);
                $(function(){
                    var imagesDiv = $('.viewer>div');
                    $(imagesDiv).eq(0).show();
                    var indexNavs = $('.indexnavi>li');
                    if(indexNavs.length > 10) {
                        $('.indexnavi:eq(0)').hide()
                    } else {
                        _.each(indexNavs, function(nav, i){
                            $(nav).click(function(){
                                var current = imageview.index;
                                if(current != i)
                                   imageview.showImage(i, current-i>0);
                            }); 
                        });
                    }
                }); 
            },
            showImage : function(next, isRight) {
                var max = this.model.length;
                var current = this.index;
                if(next == max)
                   next = 0;
                else if(next < 0)
                   next = max-1;
                var packs = $('.pack');
                if(isRight) {
                    packs.eq(current).hide('slide', {direction: 'right'}, 500);
                    packs.eq(next).show('slide', {direction: 'left'}, 500);
                } else {
                    packs.eq(current).hide('slide', {direction: 'left'}, 500);
                    packs.eq(next).show('slide', {direction: 'right'}, 500);
                }
                this.index = next;
                
            },
            next : function(){
                this.showImage(this.index+1, true);
            },
            prev : function(){
                this.showImage(this.index-1, false);
            }
        });
        var imageview = new ImageView({
            model : images
        }); 
        _.extend(imageview, this);
        images.url = "/popularimages";
        images.fetch({
            success : function(results){
                images.trigger('load_complete');
            }
        });
      
    };

    return ImageViewer;
});
