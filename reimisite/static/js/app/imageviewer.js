define(['jquery', 'underscore', 'backbone', 'text!templates/imageviewer.html', 'jquery-ui'], 
function($, _, Backbone, tpl){

    Backbone.sync = function(method, model, success, error) {
        model.push([{title: 'Hancock1', desc:'I love boa hancock!', src:'http://4.bp.blogspot.com/-8PmtiQjQZTE/Ud0Ng32nGQI/AAAAAAAADzg/JteT3GG0BCs/s1600/luffy_and_hancock_wallpaper_by_heroakemi-d41bg4z+%5Banimefullfights.com%5D.jpg', dest:'#'},
                    {title: 'Hancock2', desc:'I love boa hancock!', src:'http://animelivewallpaper.com/wp-content/uploads/2013/06/boa-hancock-1024.jpg', dest:'#'}]);
        model.trigger('change');
    };
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
                this.listenTo(this.model, 'change', this.render);
                var self = this;
            },
            render : function(){
                var imgs = this.model.toJSON();
                html = this.tpl({width: this.width, height: this.height, images: imgs});
                $(this.el).empty();
                $(this.el).append(html);
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
        images.url = "/getPopularImages";
        images.fetch();
        $(function(){
            var imagesDiv = $('.viewer>div');
            $(imagesDiv).eq(0).show();
            var indexNavs = $('.indexnavi>li');
            _.each(indexNavs, function(nav, i){
                $(nav).click(function(){
                    var current = imageview.index;
                    if(current != i)
                       imageview.showImage(i, current-i>0);
                }); 
            });
        });
    };

    return ImageViewer;
});
