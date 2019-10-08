/**
 * Handle main page Events.
 *
 * Manipulação dos eventos da página principal
 *
 * @version    1.0.0
 * @package    VocatioTelecom
 * @subpackage js
 * @author     Alcindo Schleder <alcindoschleder@gmail.com>
 *
 */

var IndexEvents = function () {
    const ERROR = 1;
    const SUCCESS = 2;
    const MAP_COLOR = {
        1: 'text-danger',
        2: 'text-success'
    }

    var documentEvents = function () {
        wow = new WOW({
            animateClass: 'animated',
            offset: 100
        });
        wow.init();
        $(document).on('scroll', function () {
            if ($(window).scrollTop() > 100) {
                $('.scroll-top-wrapper').addClass('show');
            } else {
                $('.scroll-top-wrapper').removeClass('show');
            }
        });
        $('.res-nav_click').click(function() {
            $('.main-nav').slideToggle();
            return false
        });
        $('.serviceLink').scrollToFixed();
    };
    var handleDynamicLinks = function () {
        $('.main-nav li a, .servicelink').bind('click', function(event) {
            var $anchor = $(this);

            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - 102
            }, 1500, 'easeInOutExpo');
            /*
            if you don't want to use the easing effects:
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top
            }, 1000);
            */
            if ($(window).width() < 768) {
                $('.main-nav').hide();
            }
            event.preventDefault();
        });
        $('#form-test-api, #form-get-token').on('submit', function(e) {
            e.preventDefault();
            dataKey = $(this).attr('data-key');
            IndexEvents.formSubmitEvent(dataKey);
        });
    };
    var serializerJson = function(form) {
        let js = {}
        let a = $(form).serializeArray()
        $.each(a, function() {
           if (js[this.name]) {
               if (!js[this.name].push) {
                   js[this.name] = [js[this.name]];
               }
               js[this.name].push(this.value || '');
           } else {
               js[this.name] = this.value || '';
           }
       });
       return js;
    };
    var showSearchTax = function () {
        $('.test-taxes-api-userid').fadeOut('slow', function () {
            $(this).addClass('d-none');
            $('.test-taxes-api').removeClass('d-none').fadeIn('slow', clearForm(this));
        });
    }
    var clearForm = function (form) {
        $(form).find('input[type=text]').val('');
    }
    var hideSearchTax = function () {
        $('.test-taxes-api').fadeOut('slow', function () {
            $(this).addClass('d-none');
            $('.test-taxes-api').removeClass('d-none').fadeIn('slow', clearForm(this));
        });
    }
    var configureSearchTax = function () {
        if ($('.test-taxes-api-userid').hasClass('d-none')) {
            hideSearchTax();
        } else {
            showSearchTax();
        }
    }
    var getTokenToTest = function () {
        data = serializerJson('#form-get-token');
        if ((!data['g-recaptcha-response']) ||
            (data['g-recaptcha-response'] == "") ||
            (data['g-recaptcha-response'] == undefined) ||
            (data['g-recaptcha-response'] == 0)) {
            $('#captcha-help').html('Você deve marcar este campo...');
            return false;
        }
        let url = data['host-url'] + "/api/home/gen_test_token/";
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function(d) {
                d = JSON.parse(d);
                configureSearchTax();
                $('#token-access').val(d.token);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let msg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                IndexEvents.showMessageIn('#form-test-api-help', msg, ERROR);
                console.log('erro....', msg);
            },
            dataType: "json"
        });
    };
    var getQueryTax = function () {
        data = serializerJson('#form-test-api');
        let url = data['host-url'] + "/api/home/query_tax/";
        console.log(data);
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            headers: {
                "Authorization": "token " + data['token-access']
            },
            success: function(d) {
                d = JSON.parse(d);
                // display modalform with data
                IndexEvents.showMessageIn('#form-test-api-help', 'Consulta à API realizada com sucesso!', SUCCESS);
                oonsole.log(d);
                configureSearchTax();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let errMsg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                IndexEvents.showMessageIn('#form-test-api-help', errMsg, ERROR);
                console.log('erro....', errMsg);
            },
            dataType: "json"
        });
    }
    var gotoTop = function () {
        var T = $('body').offset.top;
        $('html, body').animate({scrollTop: 0}, 900, 'linear');
    };
    var autoScrollEvent = function () {
        $('.scroll-top-wrapper').on('click', function () {
            IndexEvents.scrollToTop();
        });
    };
    var showPage = function (page, url) {
    };

    return {
        //main function to initiate the module
        init: function () {
            documentEvents();
            autoScrollEvent();
            handleDynamicLinks();
        },
        scrollToTop: function () {
            gotoTop();
        },
        showMessageIn: function (element, msg, typeMsg = 0) {
            $(element).removeClass();
            if ((typeMsg > 0) && (typeMsg < 3)){
                $(element).addClass(MAP_COLOR[typeMsg]);
            } else {
                $(element).addClass('text-muted');
            };
            $(element).html(msg);
            setTimeout(function() {
                $(element).html('');
            }, 5000)
        },
        formSubmitEvent: function (formKey) {
            switch(formKey) {
                case 'get_test_token':
                    getTokenToTest();
                    break;
                case 'get_ncm_tax':
                    console.log('Call getTestTaxes() and show Result');
                    getQueryTax();
                    break;
                default:
                    console.log('Default case... nothing happen!!!');
            }
        }
    };
}();

$(window).on('load', function() {
    IndexEvents.init(); // starting home page events
});
