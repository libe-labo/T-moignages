'use strict';

$(function() {
    $('.content__inner').prepend($('<div>', { class : 'content__item--sizer' }));
    $('.content__inner').prepend($('<div>', { class : 'content__item--gutter-sizer' }));

    var callIsotope = function() {
        var $isotope = $('.content__inner').isotope({
            itemSelector: '.content__item',
            percentPosition: true,
            masonry: {
                columnWidth: '.content__item--sizer',
                gutter: '.content__item--gutter-sizer'
            }
        });

        $isotope.imagesLoaded().progress(function() {
            $isotope.isotope('layout');
        }).then(function() {
            $isotope.isotope('layout');
            setTimeout(function() { $isotope.isotope('layout'); }, 500);
        });

        $('.content').css('height', $('.content_inner').outerHeight());
    };

    $('.content__item')
        .removeClass('content__item--unfolded')
        .addClass('content__item--folded');

    callIsotope();

    $('.content__item').each(function() {
        var $this = $(this);

        if ($this.find('.when-unfolded').length > 0) {
            $this.data('bind-unfold', function() {
                $this.css('cursor', 'pointer');

                $this.on('click.unfold', function() {
                    $this.css('cursor', '');

                    $this.off('click.unfold');

                    $this.removeClass('content__item--folded')
                         .addClass('content__item--unfolded content__item--double');

                    callIsotope();
                });
            });

            $this.data('fold', function() {
                $this.removeClass('content__item--unfolded content__item--double')
                     .addClass('content__item--folded');

                callIsotope();

                setTimeout($this.data('bind-unfold'), 100);
            });

            $this.data('bind-unfold')();
            $this.find('.when-unfolded .fa-remove').on('click.fold', $this.data('fold'));
        }
    });
});
