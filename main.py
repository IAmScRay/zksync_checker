import random
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.messagebox import showwarning
from tkinter import ttk, END
import webbrowser

from resources.fetcher import Fetcher, get_price


def get_random_color() -> str:
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    red_hex = hex(red).upper()
    if len(red_hex) == 3:
        red_hex = "0" + red_hex[2]
    else:
        red_hex = red_hex[2::].upper()

    green_hex = hex(green).upper()
    if len(green_hex) == 3:
        green_hex = "0" + green_hex[2]
    else:
        green_hex = green_hex[2::].upper()

    blue_hex = hex(blue).upper()
    if len(blue_hex) == 3:
        blue_hex = "0" + blue_hex[2]
    else:
        blue_hex = blue_hex[2::].upper()

    return red_hex + green_hex + blue_hex


def open_era_explorer(address: str):
    webbrowser.open(f"https://explorer.zksync.io/address/{address}", 2)


def open_etherscan(address: str):
    webbrowser.open(f"https://etherscan.io/address/{address}", 2)


def show_stats(address: str):
    if len(address) != 42:
        showwarning("Неверный ввод!", "Строка адреса должна быть длиной 42 символа.\n\n"
                                      "Убедитесь в правильности адреса.")
        return
    else:

        top_level = tk.Toplevel()
        window.withdraw()

        top_level.protocol(
            "WM_DELETE_WINDOW",
            lambda: [
                top_level.destroy(),
                window.wm_deiconify(),
                window.winfo_children()[2].winfo_children()[1].delete(0, END)
            ]
        )

        top_level.bind("<Escape>", lambda event: [
            top_level.destroy(),
            window.wm_deiconify(),
            window.winfo_children()[2].winfo_children()[1].delete(0, END)
        ])

        fetcher = Fetcher(address)

        results = fetcher.fetch_and_sort()
        balances = fetcher.get_balances()

        header_frame = tk.Frame(
            master=top_level
        )

        addr_lbl = tk.Label(
            master=header_frame,
            text="Адрес",
            font=("Helvetica", 14, "normal")
        )
        addr_lbl.grid(row=0, column=0, padx=3, pady=5)

        addr = tk.Label(
            master=header_frame,
            text=address,
            font=("Helvetica", 14, "bold")
        )
        addr.grid(row=0, column=1, padx=3, pady=5)

        header_frame.pack(padx=3, pady=3)

        table_frame = tk.Frame(
            master=top_level
        )

        column = 0
        for project, tx_count in results.items():
            p_lbl = None

            if project != "total" and project != "total_fee":
                p_lbl = tk.Label(
                    master=table_frame,
                    text=project,
                    font=("Helvetica", 12, "bold")
                )
            else:
                if project == "total":
                    p_lbl = tk.Label(
                        master=table_frame,
                        text="Всего транзакций",
                        font=("Helvetica", 12, "bold")
                    )

            if p_lbl is not None:
                p_lbl.grid(row=0, column=column, padx=3)

                tx_lbl = tk.Label(
                    master=table_frame,
                    text=str(tx_count),
                    font=("Helvetica", 12, "normal")
                )
                tx_lbl.grid(row=1, column=column, padx=3)

                column += 1

        table_frame.pack(padx=3, pady=3)

        ttk.Separator(
            master=top_level,
            orient=tk.HORIZONTAL
        ).pack(padx=3, pady=3, fill=tk.X)

        bal_lbl = tk.Label(
            master=top_level,
            text="Активы",
            font=("Helvetica", 18, "bold")
        )
        bal_lbl.pack(padx=3, pady=3)

        balances_frame = tk.Frame(
            master=top_level
        )

        column = 0
        for symbol, balance in balances.items():
            symbol_lbl = tk.Label(
                master=balances_frame,
                text=symbol
            )

            if symbol == "ETH":
                img = ImageTk.PhotoImage(
                    Image.open("resources/eth_logo.png").resize((32, 32))
                )

                symbol_lbl.configure(
                    text="",
                    image=img
                )
                symbol_lbl.image = img
            elif symbol == "USDC":
                img = ImageTk.PhotoImage(
                    Image.open("resources/usdc_logo.png").resize((32, 32))
                )

                symbol_lbl.configure(
                    text="",
                    image=img
                )
                symbol_lbl.image = img
            elif symbol == "USDT":
                img = ImageTk.PhotoImage(
                        Image.open("resources/usdt_logo.png").resize((32, 32))
                )

                symbol_lbl.configure(
                    text="",
                    image=img
                )
                symbol_lbl.image = img
            else:
                symbol_lbl.configure(
                    font=("Helvetica", 12, "bold"),
                    background=f"#{get_random_color()}",
                    fg="white"
                )

            symbol_lbl.grid(row=0, column=column, padx=3)

            balance_lbl = tk.Label(
                master=balances_frame,
                text=str(balance["balance"]),
                font=("Helvetica", 12, "bold")
            )
            balance_lbl.grid(row=1, column=column, padx=3)

            usd_value_lbl = tk.Label(
                master=balances_frame,
                text=f"${str(balance['usd_value'])}",
                font=("Helvetica", 10, "normal")
            )
            usd_value_lbl.grid(row=2, column=column, padx=3)

            column += 1

        fee_img = ImageTk.PhotoImage(
            Image.open("resources/fire.png").resize((32, 32))
        )

        fee_lbl = tk.Label(
            master=balances_frame,
            image=fee_img
        )
        fee_lbl.image = fee_img

        fee_lbl.grid(row=0, column=column)

        fee = tk.Label(
            master=balances_frame,
            text=str(results["total_fee"]),
            font=("Helvetica", 12, "bold")
        )
        fee.grid(row=1, column=column, padx=3)

        burnt_lbl = tk.Label(
            master=balances_frame,
            text=f"${str(round(results['total_fee'] * get_price('ETH'), 2))}",
            font=("Helvetica", 10, "normal")
        )
        burnt_lbl.grid(row=2, column=column, padx=3)

        fee_txt = tk.Label(
            master=balances_frame,
            text="сожжено на комиссии",
            font=("Helvetica", 10, "normal")
        )
        fee_txt.grid(row=3, column=column, padx=3)

        balances_frame.pack(padx=3, pady=3)

        ttk.Separator(
            master=top_level,
            orient=tk.HORIZONTAL
        ).pack(padx=3, pady=3, fill=tk.X)

        buttons_frame = tk.Frame(
            master=top_level
        )

        era_explr_btn = tk.Button(
            master=buttons_frame,
            text="Открыть Era Explorer",
            font=("Helvetica", 12, "normal"),
            command=lambda: [
                open_era_explorer(address)
            ]
        )

        era_explr_btn.grid(row=0, column=0, padx=3)

        etherscan_explr_btn = tk.Button(
            master=buttons_frame,
            text="Открыть Etherscan",
            font=("Helvetica", 12, "normal"),
            command=lambda: [
                open_etherscan(address)
            ]
        )

        etherscan_explr_btn.grid(row=0, column=1, padx=3)

        buttons_frame.pack(padx=3, pady=3)

        close_btn = tk.Button(
            master=top_level,
            text="Закрыть",
            font=("Helvetica", 12, "normal"),
            command=lambda: [
                top_level.destroy(),
                window.wm_deiconify(),
                window.winfo_children()[2].winfo_children()[1].delete(0, END)
            ]
        )

        close_btn.pack(padx=3, pady=3)


window = tk.Tk()


def main():
    window.title("ZKSync Viewer")

    main_img = Image.open("resources/zksync_logo.png").resize((256, 256))
    logo = ImageTk.PhotoImage(main_img)
    window.wm_iconphoto(True, logo)

    window.bind("<Button-1>", lambda event: event.widget.focus())
    window.bind("<Return>", lambda event: show_stats(addr.get()))

    main_lbl = tk.Label(
        master=window,
        text="ZKSync",
        fg="white",
        background="black",
        font=("Helvetica", 24)
    )
    main_lbl.pack(pady=10)

    txt = tk.Label(
        master=window,
        text="Введите адрес, статистику которого нужно просмотреть.\n",
        font=("Helvetica", 14)
    )

    txt.pack(pady=10)

    frame = tk.Frame(
        master=window
    )

    addr_lbl = tk.Label(
        master=frame,
        text="Адрес: ",
        font=("Helvetica", 12, "bold")
    )
    addr_lbl.grid(row=0, column=0, padx=3)

    addr = tk.Entry(
        master=frame,
        font=("Helvetica", 10, "normal")
    )

    addr.grid(row=0, column=1, padx=3)

    frame.pack(pady=10)

    ttk.Separator(
        master=window,
        orient=tk.HORIZONTAL
    ).pack(padx=3, pady=3, fill=tk.X)

    proceed_btn = tk.Button(
        master=window,
        text="Продолжить",
        font=("Helvetica", 12, "normal"),
        command=lambda: [
            show_stats(addr.get())
        ]
    )

    proceed_btn.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    main()
