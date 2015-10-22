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

                    // Close everything else
                    $('.content__item').each(function() {
                        if ($(this).index() === $this.index()) { return; }
                        var fold = $(this).data('fold');
                        if (fold != null) {
                            fold();
                        }
                    });

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

        // Handle Instagram iframes
        if ($this.hasClass('content__item--has-iframe')) {
            var iframeInserted = function($iframe) {
                $iframe.attr({
                    width : '',
                    height : ''
                });
                $iframe.on('load', function() {
                    $this.off('DOMNodeInserted.iframeload');
                    $iframe.css('width', 'calc(100% + 16px)');
                    $iframe.parent().css('height', $this.innerWidth());
                    callIsotope();
                });
            };

            var $iframe = $this.find('iframe');
            if ($iframe.length > 0) {
                iframeInserted($iframe);
            } else {
                if (MutationObserver != null) {
                    var observer = new MutationObserver(function(mutations) {
                        _.each(mutations, function(mutation) {
                            _.each(mutation.addedNodes, function(newNode) {
                                if (newNode.tagName === 'IFRAME') {
                                    iframeInserted($(newNode));
                                    observer.disconnect();
                                }
                            });
                        });
                    });
                    observer.observe($this.find('.content__item--has-iframe__wrapper')[0], {
                        childList : true
                    });
                } else {
                    $this.on('DOMNodeInserted.paulloz', function(ev) {
                        if (ev.target.tagName === 'IFRAME') {
                            iframeInserted($(ev.target));
                            $this.off('DOMNodeInserted.paulloz');
                        }
                    });
                }
            }
        }

        // Resize instagram wrappers on window resize
        $(window).on('resize', _.debounce(function() {
            $('.content__item--has-iframe__wrapper').each(function() {
                $(this).css('height', $(this).parent().innerWidth());
            });

            callIsotope();
        }, 200));
    });
});
