import json
import requests


def get_price(token: str) -> float:
    resp = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={token}&tsyms=USD").json()

    return float(resp["USD"])


class Fetcher:

    API_URL = "https://block-explorer-api.mainnet.zksync.io"

    def __init__(
            self,
            address: str
    ):
        self.address = address

        with open("contracts.json", "r") as file:
            self.contracts = json.load(file)["contracts"]

    def fetch_and_sort(self) -> dict:
        results = {}

        response = requests.get(
            url=f"{Fetcher.API_URL}/transactions",
            params={
                "address": self.address,
                "limit": 100
            }
        ).json()["items"]

        for tx in response:
            for name, data in self.contracts.items():
                if name not in results:
                    results[name] = 0

                if str(tx["to"]).lower() == str(data["contract"]).lower() and tx["status"] != "failed":
                    results[name] += 1

            if "Era Bridge" not in results:
                results["Era Bridge"] = 0

            if tx["isL1Originated"]:
                results["Era Bridge"] += 1

            if "total" not in results:
                results["total"] = len(response)

            if "total_fee" not in results:
                results["total_fee"] = 0

            if str(tx["from"]).lower() == self.address.lower():
                results["total_fee"] += round(float(int(tx["fee"], base=16) / 10 ** 18), 6)

        return results

    def get_balances(self) -> dict:
        results = {}

        response = requests.get(
            url=f"{Fetcher.API_URL}/address/{self.address}"
        ).json()["balances"]

        for address, data in response.items():
            if data["token"] is None:
                continue

            symbol = data["token"]["symbol"]

            decimals = data["token"]["decimals"]
            balance = round(int(data["balance"]) / 10 ** decimals, 6)

            if balance == 0:
                continue

            results[symbol] = {
                "balance": balance,
                "usd_value": round(balance * get_price(symbol), 2) if symbol in ["ETH", "USDT", "USDC"] else "* * *"
            }

        return results


