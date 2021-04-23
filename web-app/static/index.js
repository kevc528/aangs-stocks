$(function() {
    initHelperModeMessage();
    initCreateStock();
    initTrackedStockList();
});

function initHelperModeMessage() {
    $("input[name='mode-input']").change(function() {
        mode = $('input[name="mode-input"]:checked').val()
        if (mode == "buy") {
            $("#helper-mode-message").text("We'll email you once the stock drops to or below the price.")
        } else {
            $("#helper-mode-message").text("We'll email you once the stock reaches or exceeds the price.")
        }
    })
}

function initCreateStock() {
    $("#create-stock-form").submit(function( event ) {
        let formData = {
            ticker : $("#stock-input").val(),
            price : $("#price-input").val(),
            mode: $('input[name="mode-input"]:checked').val()
        }
        $.ajax({
            type: "POST",
            url: "/stock",
            data: JSON.stringify(formData),
            success: function() {
                window.location = window.location.pathname;
            },
            error: function() {
                alert("This stock symbol does not exist, or you are already tracking this stock!");
            },
            dataType: "json",
            contentType : "application/json"
        });
        event.preventDefault();
    });
}

function initTrackedStockList() {
    $.getJSON( "/user/me", function( data ) {
        data.stocks.forEach(stock => {
            avatar_color = "green"
            if (stock.mode == "buy") {
                avatar_color = "blue"
            }
            html = `
            <li class="collection-item avatar">
                <i class="material-icons circle ${avatar_color}">insert_chart</i>
                <span class="title stock-info">
                    <strong>
                    <span class="stock-ticker">${stock.ticker}</span> - <span class="green-text stock-price">$${stock.current_price}</span>
                    </strong>
                </span>
                <p>
                    <span class="track-info">You are <strong>waiting to <span class="track-mode"></span>${stock.mode}</strong> at $<span class="track-price">${stock.price}</span>.</span>
                    <span class="track-id" hidden>${stock.id}</span>
                </p>
                <i class="secondary-content material-icons red-text delete-stock-button">delete_forever</i>
            </li>
            `
            $("#tracked-stocks-list").append(html)
        })
        initDeleteStockButtons();
    });
}

function initDeleteStockButtons() {
    $(".delete-stock-button").click(function() {
        stockID = $(this).parent().find(".track-id").first().text();
        $.ajax({
            type: "DELETE",
            url: "/stock/" + stockID,
            success: function() {
                window.location = window.location.pathname;
            },
        });
    });
}
