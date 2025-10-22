"""
MT5 Live Data Module for RiskOptima Engine
Enhanced MT5 integration for real-time account data reading and historical data fetching
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import threading
import queue

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    mt5 = None

logger = logging.getLogger(__name__)

class MT5LiveDataError(Exception):
    """Raised when MT5 live data operations fail"""
    pass

class MT5DataStreamer:
    """Real-time MT5 data streaming and account monitoring"""

    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.is_streaming = False
        self.stream_thread: Optional[threading.Thread] = None
        self.data_queue = queue.Queue(maxsize=100)
        self.callbacks: List[callable] = []
        self.last_account_info: Optional[Dict[str, Any]] = None
        self.last_positions: List[Dict[str, Any]] = []

    def start_streaming(self) -> bool:
        """Start real-time data streaming"""
        if not MT5_AVAILABLE:
            logger.error("MetaTrader5 package not available")
            return False

        if self.is_streaming:
            logger.warning("Streaming already active")
            return True

        try:
            # Initialize MT5 if not already done
            if not mt5.initialize():
                error = mt5.last_error()
                logger.error(f"MT5 initialization failed: {error}")
                return False

            self.is_streaming = True
            self.stream_thread = threading.Thread(target=self._streaming_loop, daemon=True)
            self.stream_thread.start()

            logger.info("MT5 data streaming started")
            return True

        except Exception as e:
            logger.error(f"Failed to start streaming: {e}")
            self.is_streaming = False
            return False

    def stop_streaming(self) -> bool:
        """Stop real-time data streaming"""
        if not self.is_streaming:
            return True

        self.is_streaming = False

        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=5.0)

        logger.info("MT5 data streaming stopped")
        return True

    def add_callback(self, callback: callable) -> None:
        """Add callback function for data updates"""
        self.callbacks.append(callback)

    def remove_callback(self, callback: callable) -> None:
        """Remove callback function"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def get_latest_data(self) -> Optional[Dict[str, Any]]:
        """Get the most recent account and position data"""
        try:
            return self.data_queue.get_nowait()
        except queue.Empty:
            return None

    def _streaming_loop(self) -> None:
        """Main streaming loop"""
        while self.is_streaming:
            try:
                # Get account info
                account = mt5.account_info()
                if account is None:
                    logger.warning("Failed to get account info")
                    time.sleep(self.update_interval)
                    continue

                # Get positions
                positions = mt5.positions_get()
                positions_data = []
                if positions:
                    for pos in positions:
                        positions_data.append({
                            "ticket": pos.ticket,
                            "time": pos.time,
                            "symbol": pos.symbol,
                            "type": pos.type,
                            "volume": pos.volume,
                            "price_open": pos.price_open,
                            "price_current": pos.price_current,
                            "profit": pos.profit,
                            "sl": pos.sl,
                            "tp": pos.tp,
                        })

                # Prepare data packet
                data_packet = {
                    "timestamp": datetime.now().isoformat(),
                    "account": {
                        "login": account.login,
                        "balance": account.balance,
                        "equity": account.equity,
                        "margin": account.margin,
                        "margin_free": account.margin_free,
                        "margin_level": account.margin_level,
                        "profit": account.profit,
                        "leverage": account.leverage,
                        "currency": account.currency,
                    },
                    "positions": positions_data,
                    "position_count": len(positions_data),
                    "total_exposure": sum(abs(pos.get("volume", 0)) for pos in positions_data),
                }

                # Store latest data
                self.last_account_info = data_packet["account"]
                self.last_positions = positions_data

                # Add to queue (remove old data if full)
                if self.data_queue.full():
                    try:
                        self.data_queue.get_nowait()
                    except queue.Empty:
                        pass

                self.data_queue.put(data_packet)

                # Call callbacks
                for callback in self.callbacks:
                    try:
                        callback(data_packet)
                    except Exception as e:
                        logger.error(f"Callback error: {e}")

            except Exception as e:
                logger.error(f"Streaming loop error: {e}")

            time.sleep(self.update_interval)

class MT5HistoricalData:
    """MT5 historical data fetching and management"""

    def __init__(self):
        self.connected = False

    def connect(self, timeout: int = 30) -> bool:
        """Connect to MT5 terminal"""
        if not MT5_AVAILABLE:
            logger.error("MetaTrader5 package not available")
            return False

        try:
            if not mt5.initialize(timeout=timeout * 1000):
                error = mt5.last_error()
                logger.error(f"MT5 connection failed: {error}")
                return False

            self.connected = True
            logger.info("Connected to MT5 for historical data")
            return True

        except Exception as e:
            logger.error(f"MT5 connection error: {e}")
            return False

    def disconnect(self) -> bool:
        """Disconnect from MT5"""
        if not self.connected:
            return True

        try:
            mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MT5")
            return True
        except Exception as e:
            logger.error(f"MT5 disconnection error: {e}")
            return False

    def get_historical_trades(
        self,
        symbol: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        max_trades: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Fetch historical trades from MT5

        Args:
            symbol: Specific symbol to fetch (None for all)
            start_date: Start date for trade history
            end_date: End date for trade history
            max_trades: Maximum number of trades to return

        Returns:
            List of trade dictionaries
        """
        if not self.connected:
            logger.error("Not connected to MT5")
            return []

        try:
            # Set default date range (last 30 days)
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=30)

            # Convert to MT5 time format
            start_time = start_date.timestamp()
            end_time = end_date.timestamp()

            # Get deal history
            deals = mt5.history_deals_get(
                date_from=start_time,
                date_to=end_time,
                group="*" if symbol is None else f"*{symbol}*"
            )

            if deals is None:
                logger.warning("No deals found in specified date range")
                return []

            # Convert to dictionaries
            trades = []
            for deal in deals[-max_trades:]:  # Get most recent trades
                trade = {
                    "ticket": deal.ticket,
                    "order": deal.order,
                    "time": datetime.fromtimestamp(deal.time).isoformat(),
                    "time_msc": deal.time_msc,
                    "type": deal.type,
                    "entry": deal.entry,
                    "magic": deal.magic,
                    "position_id": deal.position_id,
                    "reason": deal.reason,
                    "volume": deal.volume,
                    "price": deal.price,
                    "commission": deal.commission,
                    "swap": deal.swap,
                    "profit": deal.profit,
                    "fee": deal.fee,
                    "symbol": deal.symbol,
                    "comment": deal.comment,
                    "external_id": deal.external_id,
                }
                trades.append(trade)

            logger.info(f"Fetched {len(trades)} historical trades")
            return trades

        except Exception as e:
            logger.error(f"Error fetching historical trades: {e}")
            return []

    def get_account_history(
        self,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[Dict[str, Any]]:
        """
        Get account balance/equity history

        Args:
            start_date: Start date for history
            end_date: End date for history

        Returns:
            List of account snapshots
        """
        if not self.connected:
            logger.error("Not connected to MT5")
            return []

        try:
            # Set default date range
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=30)

            # Get account history (this is a simplified implementation)
            # MT5 doesn't directly provide balance history, so we use deals
            deals = self.get_historical_trades(start_date=start_date, end_date=end_date)

            # Calculate running balance (simplified)
            balance = 0.0
            history = []

            for deal in sorted(deals, key=lambda x: x["time"]):
                balance += deal.get("profit", 0) + deal.get("commission", 0) + deal.get("swap", 0)

                history.append({
                    "timestamp": deal["time"],
                    "balance": balance,
                    "profit": deal.get("profit", 0),
                    "commission": deal.get("commission", 0),
                    "swap": deal.get("swap", 0),
                    "symbol": deal.get("symbol", ""),
                })

            return history

        except Exception as e:
            logger.error(f"Error getting account history: {e}")
            return []

    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get detailed symbol information"""
        if not self.connected:
            return None

        try:
            info = mt5.symbol_info(symbol)
            if info is None:
                return None

            return {
                "name": info.name,
                "description": info.description,
                "currency_base": info.currency_base,
                "currency_profit": info.currency_profit,
                "currency_margin": info.currency_margin,
                "point": info.point,
                "digits": info.digits,
                "spread": info.spread,
                "spread_float": info.spread_float,
                "tick_value": info.tick_value,
                "tick_size": info.tick_size,
                "contract_size": info.contract_size,
                "volume_min": info.volume_min,
                "volume_max": info.volume_max,
                "volume_step": info.volume_step,
                "margin_initial": info.margin_initial,
                "margin_maintenance": info.margin_maintenance,
                "swap_long": info.swap_long,
                "swap_short": info.swap_short,
                "swap_rollover3days": info.swap_rollover3days,
                "trade_mode": info.trade_mode,
                "trade_flags": info.trade_flags,
                "bid": info.bid,
                "ask": info.ask,
                "last": info.last,
                "volume": info.volume,
                "volume_real": info.volume_real,
                "time": info.time,
                "session_open": info.session_open,
                "session_close": info.session_close,
            }

        except Exception as e:
            logger.error(f"Error getting symbol info for {symbol}: {e}")
            return None

    def get_available_symbols(self) -> List[str]:
        """Get list of available trading symbols"""
        if not self.connected:
            return []

        try:
            symbols = mt5.symbols_get()
            if symbols is None:
                return []

            return [symbol.name for symbol in symbols]

        except Exception as e:
            logger.error(f"Error getting available symbols: {e}")
            return []

# Global instances
data_streamer = MT5DataStreamer()
historical_data = MT5HistoricalData()

def start_live_streaming(update_interval: float = 1.0) -> bool:
    """Start live data streaming"""
    return data_streamer.start_streaming()

def stop_live_streaming() -> bool:
    """Stop live data streaming"""
    return data_streamer.stop_streaming()

def get_live_account_data() -> Optional[Dict[str, Any]]:
    """Get latest live account data"""
    return data_streamer.get_latest_data()

def connect_mt5_historical(timeout: int = 30) -> bool:
    """Connect to MT5 for historical data"""
    return historical_data.connect(timeout)

def disconnect_mt5_historical() -> bool:
    """Disconnect from MT5 historical data"""
    return historical_data.disconnect()

def fetch_historical_trades(
    symbol: str = None,
    days_back: int = 30,
    max_trades: int = 1000
) -> List[Dict[str, Any]]:
    """Fetch historical trades from MT5"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return historical_data.get_historical_trades(symbol, start_date, end_date, max_trades)

def get_mt5_account_history(days_back: int = 30) -> List[Dict[str, Any]]:
    """Get account balance history"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return historical_data.get_account_history(start_date, end_date)

def get_mt5_symbol_info(symbol: str) -> Optional[Dict[str, Any]]:
    """Get symbol information"""
    return historical_data.get_symbol_info(symbol)

def get_mt5_available_symbols() -> List[str]:
    """Get available symbols"""
    return historical_data.get_available_symbols()