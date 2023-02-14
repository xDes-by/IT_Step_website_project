////////////////////////////////// THEME ////////////////////////////////////

var theme = (localStorage.getItem('theme') === 'dark')

applyTheme(theme)

$('#dark-btn').on('click', function () {
    theme = !theme
    applyTheme(theme)
    localStorage.setItem('theme', (theme ? 'dark' : 'light'))
})

function applyTheme(theme) {
    if (theme) {
        $(':root').css('--light-color', '#ebecf0')
        $(':root').css('--light-color-shadow-1', '#fff')
        $(':root').css('--light-color-shadow-2', '#babecc')
    } else {
        $(':root').css('--light-color', '#4b4846')
        $(':root').css('--light-color-shadow-1', '#4b4846')
        $(':root').css('--light-color-shadow-2', '#202020')
    }
}

////////////////////////////////// MAIN PAGE ROLL ////////////////////////////////////

var list = $('.main-rotate-circle .mrc-item')
var rotateElement = $('.bg-rotate')[0]
var big_circle = $('.main-rotate-circle')[0]
var blur_circle = $('.blur-rotate-circle')[0]
var length = $('.right-menu .sub-mrc').length - 1
var rotate = 0
var arrayColor = ['#F5C069', '#82B9BA', '#C47EAA', '#9989D0']
var position = 0

$('#next').on('click', function () {
    rotate = rotate + 360 / list.length
    position = position + 1 >= arrayColor.length ? 0 : position + 1
    nextitem()
    blocknext()
})

function nextitem() {
    $(rotateElement).css('transform', 'rotate(' + rotate + 'deg)')
    $(big_circle).css('transform', 'rotate(' + rotate + 'deg)')
    $(blur_circle).css('transform', 'rotate(' + (rotate - 20) + 'deg)')
    $(rotateElement).css('backgroundColor', arrayColor[position])

    $('#next').css('pointer-events', 'none')
    $(big_circle).addClass('mrc-item-blur')
    setTimeout(function () {
        $('#next').css('pointer-events', 'unset')
        $(big_circle).removeClass('mrc-item-blur')
    }, 1000)
}

$('#back').on('click', function () {
    rotate = rotate - 360 / list.length
    position = position < 0 ? arrayColor.length - 1 : position - 1
    backitem()
    blockprev()
})

function backitem() {
    $(rotateElement).css('transform', 'rotate(' + rotate + 'deg)')
    $(big_circle).css('transform', 'rotate(' + rotate + 'deg)')
    $(blur_circle).css('transform', 'rotate(' + (rotate - 20) + 'deg)')
    $(rotateElement).css('backgroundColor', arrayColor[position])

    $('#back').css('pointer-events', 'none')
    $(big_circle).addClass('mrc-item-blur')
    setTimeout(function () {
        $('#back').css('pointer-events', 'unset')
        $(big_circle).removeClass('mrc-item-blur')
    }, 1000)
}

////////////////////////////////// MAIN PAGE BLOCK SWIPE ////////////////////////////////////

$(function () {
    $('.right-menu .sub-mrc').eq(0).addClass('active').fadeIn(1000)
    updateTotal()
})

function blocknext() {
    var activeSubMrc = $('.right-menu .sub-mrc.active')
    var nextSubMrc = activeSubMrc.next('.sub-mrc')
    if (nextSubMrc.length) {
        activeSubMrc.removeClass('active').fadeOut(1000)
        nextSubMrc.addClass('active').delay(1000).fadeIn(1000)
    } else {
        activeSubMrc.removeClass('active').fadeOut(1000)
        $('.right-menu .sub-mrc').eq(0).addClass('active').delay(1000).fadeIn(1000)
    }
}

function blockprev() {
    var activeSubMrc = $('.right-menu .sub-mrc.active')
    var prevSubMrc = activeSubMrc.prev('.sub-mrc')
    if (prevSubMrc.length) {
        activeSubMrc.removeClass('active').fadeOut(1000)
        prevSubMrc.addClass('active').delay(1000).fadeIn(1000)
    } else {
        activeSubMrc.removeClass('active').fadeOut(1000)
        $('.right-menu .sub-mrc').eq(3).addClass('active').delay(1000).fadeIn(1000)
    }
}

////////////////////////////////// MAIN PAGE MOVE TO SHOP ////////////////////////////////////

$('.slide-item').on('click', function (e) {
    e.preventDefault()
    const $this = $(this)
    const data = {
        cid: $this.data('cid'),
    }
    window.location.replace("http://127.0.0.1:8000/filter/?category=" + data.cid);
})

////////////////////////////////// SHOW TO CART ////////////////////////////////////

function showingCart() {
    cardItems = UpdateSC()
    cardItems.toggleClass('hidden')
}

function UpdateSC(){
    const cardItems = $('.card-items')
    const startOrder = $('.start-order')
    if (startOrder.hasClass('auth')) {
        console.log(cardItems.find('ul li').length)
        if (cardItems.find('ul li').length == 0) {
            startOrder.text("Корзина пуста").off('click').on('click', function (e) {
                e.preventDefault()
            })
        } else {
            startOrder.text("Перейти в корзину").off('click').on('click', function (e) {
                e.preventDefault()
                window.location.href = "/order"
            })
        }
    }
    return cardItems
}

$('#card-btn').on('click', function (e) {
    e.preventDefault()
    showingCart()
})

///////////////////////////////////// ORDER PAGE ////////////////////////////////////////////

if (location.pathname === '/order/') {
    $('#card-btn').remove()
} else {
    $('#open-shop-btn').remove()
}

$('.del-item').on('click', function (e) {
    e.preventDefault()
    const $this = $(this)
    const data = {
        pid: $this.data('pid'),
        remove: $this.data('remove')
    }
    ajax(data)
    $this.closest('div').remove()
    updateTotal()
})

$('.minus-btn, .plus-btn').on('click', function (e) {
    e.preventDefault()
    const $this = $(this)
    const $input = $this.closest('div').find('input')
    const value = parseInt($input.val())
    const data = {
        pid: $this.data('pid'),
        del: $this.data('del'),
        name: $this.data('name'),
        price: $this.data('price')
    }
    var newValue = value
    if ($this.hasClass('minus-btn')) {
        newValue = (value > 1) ? value - 1 : 0
    } else {
        if ($(this).data('count') > value) {
            newValue = value + 1
        } else {
            return
        }
    }
    const newTotalPrice = parseFloat(parseInt(data.price) * newValue).toFixed(2)
    $this.closest('.order-quantity').closest('.order-item').find('.order-total-price').text(newTotalPrice)
    ajax(data)
    updateTotal()
    $input.val(newValue)
})

function updateTotal() {
    const items = $('.order-total-price')
    var totalItemsPrice = 0
    items.each(function () {
        totalItemsPrice += parseFloat($(this).text())
    })
    $('.total-item-price').text(`Total price: ${totalItemsPrice.toFixed(2)} BYN`)
}

/////////////////////////////////////////////////////// SHOW COUNT PRODUCTS //////////////////////////

$(function () {
    const cardCount = $('.card-count')
    cardCount.css('background-color', cardCount.text().length > 59 ? 'red' : 'none')
})

/////////////////////////////////////////////////////// ADD TO CART //////////////////////////

$(".submit_btn").click(function (e) {
    e.preventDefault()
    const data = {
        pid: $(this).data("pid"),
        name: $(this).data("name"),
        price: $(this).data("price")
    }
    const button = $(this)
    ajax(data, button)
})

/////////////////////////////////////////////////////// AJAX //////////////////////////  

function ajax(data, button) {
    const form = $('.add_cart')
    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: data,
        cache: true,
        success: function (data) {
            if (data.can_buy === 'false') {
                if (button) {
                    button.text('Нет на складе')
                }
            }
            if (data.product_count) {
                const cardCount = $('.card-count')
                cardCount.css('background-color', 'red')
                cardCount.text(data.product_count)
                $('.card-items ul').html("")
                $.each(data.products, function (k, v) {
                    $('.card-items ul').append('<li>' + v.name + ', ' + v.count + 'шт. сумма: ' + v.total_price + 'BYN' + '</li>')
                })
                UpdateSC()
            }else{
                window.location.replace("http://127.0.0.1:8000/shop/");
            }
        },
        error: function () {
            console.log("error")
        }
    })
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

$(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
})

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=")
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1
            c_end = document.cookie.indexOf(";", c_start)
            if (c_end == -1) c_end = document.cookie.length
            return unescape(document.cookie.substring(c_start, c_end))
        }
    }
    return ""
}

////////////////////////////////////////////////////////////////////////////////