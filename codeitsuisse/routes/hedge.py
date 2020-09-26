import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def make_calculations(rho, sigma_s, sigma_f, portfolio_value, futures_price, notional_value):
    hedge_ratio = round(rho * sigma_s / sigma_f, 3)
    num_future_contract = round(hedge_ratio * portfolio_value / (futures_price * notional_value))
    return (hedge_ratio, num_future_contract)


def optimized_portfolio(portfolio, indexFutures):
    portfolio_value = portfolio["Value"]
    sigma_s = portfolio["SpotPrcVol"]

    hedge_ratio, num_future_contract = make_calculations(indexFutures[0]["CoRelationCoefficient"], 
                                        sigma_s, indexFutures[0]["FuturePrcVol"], 
                                        portfolio_value, indexFutures[0]["IndexFuturePrice"], 
                                        indexFutures[0]["Notional"])

    most_optimal = {"HedgePositionName": indexFutures[0]["Name"], 
                    "OptimalHedgeRatio": hedge_ratio,
                    "NumFuturesContract": num_future_contract,
                    "FuturesVolatility": indexFutures[0]["FuturePrcVol"]}
    
    if len(indexFutures) == 1:
        most_optimal.pop('FuturesVolatility', None)
        return most_optimal

    for index in indexFutures[1:]:
        hedge_ratio, num_future_contract = make_calculations(index["CoRelationCoefficient"], 
                                        sigma_s, index["FuturePrcVol"], 
                                        portfolio_value, index["IndexFuturePrice"], 
                                        index["Notional"])

        if hedge_ratio < most_optimal["OptimalHedgeRatio"] and index["FuturePrcVol"] < most_optimal["FuturesVolatility"]:
            most_optimal = {"HedgePositionName": index["Name"], 
                            "OptimalHedgeRatio": hedge_ratio,
                            "NumFuturesContract": num_future_contract,
                            "FuturesVolatility": index["FuturePrcVol"]}

        elif (hedge_ratio < most_optimal["OptimalHedgeRatio"] and index["FuturePrcVol"] > most_optimal["FuturesVolatility"] or 
            hedge_ratio > most_optimal["OptimalHedgeRatio"] and index["FuturePrcVol"] < most_optimal["FuturesVolatility"]):
            if num_future_contract < most_optimal["NumFuturesContract"]:
                most_optimal = {"HedgePositionName": index["Name"], 
                            "OptimalHedgeRatio": hedge_ratio,
                            "NumFuturesContract": num_future_contract,
                            "FuturesVolatility": index["FuturePrcVol"]}
            else:
                continue
        else:
            continue

    most_optimal.pop('FuturesVolatility', None)
    return most_optimal

#number of futures contract > volatility

@app.route('/optimizedportfolio', methods=["POST"])
def get_portfolio():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    entries = data.get("inputs");

    outputs = []
    for entry in entries:
        outputs.append(optimized_portfolio(entry["Portfolio"], entry["IndexFutures"]))
    
    result = {
        "outputs": outputs
    }

    logging.info("My result :{}".format(result))
    return jsonify(result);