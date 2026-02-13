from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label
from textual.containers import Horizontal
from services.crypto_service import CryptoService
from utils.charts import make_candlestick
from models.coin import Coin

class CryptoApp(App):
    CSS_PATH = "../style/style.css"

    def compose(self) -> ComposeResult:
        self.coin_list = ListView(id="sidebar")
        self.details_panel = Static("Loading coins...", id="details")
        yield Horizontal(self.coin_list, self.details_panel)

    def populate_list(self):
        self.coin_list.clear()
        for coin in self.coins:
            self.coin_list.append(ListItem(Label(f"{coin.symbol.upper()} - {coin.name}")))

    def on_mount(self):
        self.details_panel.update("Fetching coins...")
        self.coins = CryptoService.get_top_coins()
        if not self.coins:
            self.details_panel.update("⚠️ Could not fetch coins.")
            return

        for coin in self.coins:
            coin.ohlc = None
            coin.sparkline = None

        self.populate_list()
        self.details_panel.update("Select a coin to view details.")

    def on_list_view_selected(self, event: ListView.Selected):
        coin = self.coins[self.coin_list.index]

        if coin.ohlc is None:
            self.details_panel.update("Loading candlestick data...")
            ohlc = CryptoService.get_ohlc_history(coin.id)
            if not ohlc:
                self.details_panel.update("⚠️ Candlestick chart unavailable.")
                return
            coin.ohlc = ohlc
            panel_width = self.details_panel.size.width or 90
            coin.sparkline = make_candlestick(ohlc, width=panel_width, height=20)

        self.details_panel.update(self.format_coin_info(coin, self.details_panel.size.width))

    def format_coin_info(self, coin: Coin, width: int = 80) -> str:
        width = width or 80
        separator = "─" * width
        change = coin.price_change_percentage_24h
        if change is None:
            change_color = ""
            change_str = "N/A"
        else:
            change_color = "green" if change >= 0 else "red"
            change_str = f"{change:.2f}%"

        return f"""
[bold cyan]💰 {coin.name} ({coin.symbol.upper()})[/bold cyan]

[bold cyan]{separator}[/bold cyan]

[bold]Price:[/bold]      ${coin.current_price:,.2f} | [{change_color}]{change_str}[/{change_color}]
[bold]Market Cap:[/bold] ${coin.market_cap:,.0f}
[bold]Volume:[/bold]     ${coin.total_volume:,.0f}
[green][bold]High:[/bold][/green] ${coin.high_24h or 'N/A'} | [red][bold]Low:[/bold][/red] ${coin.low_24h or 'N/A'}
[green][bold]ATH:[/bold][/green] ${coin.ath or 'N/A'} | [red][bold]ATL:[/bold][/red] ${coin.atl or 'N/A'}

[bold cyan]{separator}[/bold cyan]

[bold]📉 7-Day Candlestick:[/bold]
{coin.sparkline}
"""
