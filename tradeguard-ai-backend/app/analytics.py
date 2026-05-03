class TradeAnalyzer:
    def __init__(self, trades):
        self.trades = trades

    def total_trades(self):
        return len(self.trades)

    def total_profit_loss(self):
        return round(sum(trade.profit_loss for trade in self.trades), 2)

    def win_rate(self):
        if not self.trades:
            return 0

        wins = [trade for trade in self.trades if trade.profit_loss > 0]
        return round((len(wins) / len(self.trades)) * 100, 2)

    def loss_rate(self):
        if not self.trades:
            return 0

        losses = [trade for trade in self.trades if trade.profit_loss < 0]
        return round((len(losses) / len(self.trades)) * 100, 2)

    def average_profit(self):
        winning_trades = [trade.profit_loss for trade in self.trades if trade.profit_loss > 0]

        if not winning_trades:
            return 0

        return round(sum(winning_trades) / len(winning_trades), 2)

    def average_loss(self):
        losing_trades = [trade.profit_loss for trade in self.trades if trade.profit_loss < 0]

        if not losing_trades:
            return 0

        return round(sum(losing_trades) / len(losing_trades), 2)

    def risk_score(self):
        win_rate = self.win_rate()
        total_profit = self.total_profit_loss()

        if total_profit > 0 and win_rate >= 50:
            return "Low Risk"

        if total_profit > 0 and win_rate < 50:
            return "Medium Risk"

        return "High Risk"

    def ai_feedback(self):
        win_rate = self.win_rate()
        total_profit = self.total_profit_loss()
        avg_profit = self.average_profit()
        avg_loss = abs(self.average_loss())

        if not self.trades:
            return "No trades found. Upload or add trades first."

        if total_profit < 0:
            return "Your account is losing money. Focus on reducing lot size, avoiding revenge trading, and improving risk-reward ratio."

        if win_rate > 50 and avg_loss > avg_profit:
            return "Your win rate is good, but your average loss is bigger than your average profit. Try to cut losses earlier."

        if win_rate < 40:
            return "Your win rate is low. Review your entry strategy and avoid taking low-quality setups."

        return "Your performance looks stable. Keep tracking your risk, emotions, and trading mistakes."