import json
import webbrowser
import customtkinter as ctk

# Load news data from JSON file
with open('news_data.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

def create_news_frame(parent, news_info):
    frame = ctk.CTkFrame(parent)
    frame.pack(side="bottom", padx=10, pady=5, fill="x")

    def open_news_url():
        webbrowser.open_new(news_info["url"])

    def on_enter(event):
        title_label.configure(cursor="hand2")

    def on_leave(event):
        title_label.configure(cursor="")

    title_label = ctk.CTkLabel(frame, text=news_info["title"], font=("Arial", 12, "bold"), wraplength=600)
    title_label.pack(anchor="w", padx=10, pady=5)
    title_label.bind("<Button-1>", lambda event: open_news_url())
    title_label.bind("<Enter>", on_enter)
    title_label.bind("<Leave>", on_leave)

    date_label = ctk.CTkLabel(frame, text=news_info["data"], font=("Arial", 10))
    date_label.pack(anchor="w", padx=10, pady=(0, 5))

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

def get_exchange_rate(currency_from, currency_to):
    exchange_rate = 27.5
    return exchange_rate

usd_to_uah_rate = get_exchange_rate("USD", "UAH")
btc_to_usd_rate = get_exchange_rate("BTC", "USD")

def update_usd_to_uah():
    usd_to_uah_label.configure(text=f"Курс доллара к гривне: {usd_to_uah_rate}")

def update_btc_to_usd():
    btc_to_usd_label.configure(text=f"Курс биткоина к доллару: {btc_to_usd_rate}")

app = ctk.CTk()
app.title("Новости")

top_frame = ctk.CTkFrame(app)
top_frame.pack(side="top", fill="both", expand=True)


usd_frame = ctk.CTkFrame(top_frame)
usd_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

usd_to_uah_label = ctk.CTkLabel(usd_frame, font=("Arial", 12, "bold"))
usd_to_uah_label.pack(anchor="w", padx=10, pady=5)
update_usd_to_uah()

btc_frame = ctk.CTkFrame(top_frame)
btc_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

btc_to_usd_label = ctk.CTkLabel(btc_frame, font=("Arial", 12, "bold"))
btc_to_usd_label.pack(anchor="w", padx=10, pady=5)
update_btc_to_usd()

for news_item in reversed(news_data):
    create_news_frame(app, news_item)

app.geometry("600x800")
app.mainloop()
