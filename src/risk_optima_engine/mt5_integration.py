"""
MT5 Integration Module for RiskOptima Engine
Handles connection to MetaTrader 5 terminal and real-time data retrieval
"""

import logging
from typing import Dict, Any, Optional, Tuple
import time

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    mt5 = None

logger = logging.getLogger(__name__)

class MT5ConnectionError(Exception):
    """Raised when MT5 connection fails"""
    pass

class MT5Integration:
    """Handles MT5 terminal integration"""

    def __init__(self):
        self.connected = False
        self.terminal_info = None
        self.account_info = None

    def initialize(self, timeout: int = 30) -> bool:
        """
        Initialize connection to MT5 terminal

        Args:
            timeout: Connection timeout in seconds

        Returns:
            bool: True if connection successful
        """
        if not MT5_AVAILABLE:
            logger.error("MetaTrader5 package not available")
            raise MT5ConnectionError("MetaTrader5 package not installed")

        try:
            # Initialize MT5
            if not mt5.initialize():
                error = mt5.last_error()
                logger.error(f"MT5 initialization failed: {error}")
                raise MT5ConnectionError(f"MT5 initialization failed: {error}")

            # Wait for terminal to connect
            start_time = time.time()
            while time.time() - start_time < timeout:
                if mt5.terminal_info() is not None:
                    break
                time.sleep(0.1)

            # Check if terminal is connected
            terminal_info = mt5.terminal_info()
            if terminal_info is None:
                raise MT5ConnectionError("MT5 terminal not responding")

            self.terminal_info = terminal_info
            self.connected = True
            logger.info("Successfully connected to MT5 terminal")
            return True

        except Exception as e:
            logger.error(f"MT5 connection failed: {e}")
            self.connected = False
            raise MT5ConnectionError(f"Connection failed: {e}")

    def disconnect(self) -> bool:
        """
        Disconnect from MT5 terminal

        Returns:
            bool: True if disconnection successful
        """
        if not self.connected:
            return True

        try:
            if MT5_AVAILABLE and mt5:
                result = mt5.shutdown()
                if result:
                    self.connected = False
                    self.terminal_info = None
                    self.account_info = None
                    logger.info("Successfully disconnected from MT5")
                    return True
                else:
                    error = mt5.last_error()
                    logger.error(f"MT5 shutdown failed: {error}")
                    return False
        except Exception as e:
            logger.error(f"MT5 disconnection error: {e}")
            return False

    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """
        Get current account information

        Returns:
            Dict containing account data or None if failed
        """
        if not self.connected:
            logger.warning("MT5 not connected")
            return None

        try:
            account = mt5.account_info()
            if account is None:
                error = mt5.last_error()
                logger.error(f"Failed to get account info: {error}")
                return None

            # Convert to dictionary
            account_data = {
                "login": account.login,
                "balance": account.balance,
                "equity": account.equity,
                "margin": account.margin,
                "margin_free": account.margin_free,
                "margin_level": account.margin_level,
                "profit": account.profit,
                "leverage": account.leverage,
                "currency": account.currency,
                "server": account.server,
                "company": account.company,
            }

            self.account_info = account_data
            return account_data

        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return None

    def get_terminal_info(self) -> Optional[Dict[str, Any]]:
        """
        Get terminal information

        Returns:
            Dict containing terminal data or None if failed
        """
        if not self.connected:
            logger.warning("MT5 not connected")
            return None

        try:
            terminal = mt5.terminal_info()
            if terminal is None:
                error = mt5.last_error()
                logger.error(f"Failed to get terminal info: {error}")
                return None

            # Convert to dictionary
            terminal_data = {
                "name": terminal.name,
                "path": terminal.path,
                "data_path": terminal.data_path,
                "community_account": terminal.community_account,
                "community_connection": terminal.community_connection,
                "connected": terminal.connected,
                "dlls_allowed": terminal.dlls_allowed,
                "trade_allowed": terminal.trade_allowed,
                "tradeapi_disabled": terminal.tradeapi_disabled,
                "email_enabled": terminal.email_enabled,
                "ftp_enabled": terminal.ftp_enabled,
                "notifications_enabled": terminal.notifications_enabled,
                "mqid": terminal.mqid,
                "build": terminal.build,
                "maxbars": terminal.maxbars,
                "codepage": terminal.codepage,
                "ping_last": terminal.ping_last,
                "community_balance": terminal.community_balance,
                "cpu_cores": terminal.cpu_cores,
                "cpu_usage": terminal.cpu_usage,
                "disk_space": terminal.disk_space,
                "memory_physical": terminal.memory_physical,
                "memory_total": terminal.memory_total,
                "memory_available": terminal.memory_available,
                "memory_used": terminal.memory_used,
                "memory_used_percent": terminal.memory_used_percent,
            }

            return terminal_data

        except Exception as e:
            logger.error(f"Error getting terminal info: {e}")
            return None

    def get_positions(self) -> Optional[list]:
        """
        Get current open positions

        Returns:
            List of position dictionaries or None if failed
        """
        if not self.connected:
            logger.warning("MT5 not connected")
            return None

        try:
            positions = mt5.positions_get()
            if positions is None:
                error = mt5.last_error()
                logger.error(f"Failed to get positions: {error}")
                return None

            # Convert to list of dictionaries
            positions_data = []
            for pos in positions:
                position_data = {
                    "ticket": pos.ticket,
                    "time": pos.time,
                    "time_msc": pos.time_msc,
                    "time_update": pos.time_update,
                    "time_update_msc": pos.time_update_msc,
                    "type": pos.type,
                    "magic": pos.magic,
                    "identifier": pos.identifier,
                    "reason": pos.reason,
                    "volume": pos.volume,
                    "price_open": pos.price_open,
                    "sl": pos.sl,
                    "tp": pos.tp,
                    "price_current": pos.price_current,
                    "swap": pos.swap,
                    "profit": pos.profit,
                    "symbol": pos.symbol,
                    "comment": pos.comment,
                    "external_id": pos.external_id,
                }
                positions_data.append(position_data)

            return positions_data

        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return None

    def is_connected(self) -> bool:
        """
        Check if MT5 is connected

        Returns:
            bool: Connection status
        """
        return self.connected

    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get comprehensive connection status

        Returns:
            Dict with connection details
        """
        status = {
            "connected": self.connected,
            "mt5_available": MT5_AVAILABLE,
            "terminal_info": None,
            "account_info": None,
        }

        if self.connected:
            status["terminal_info"] = self.get_terminal_info()
            status["account_info"] = self.get_account_info()

        return status

# Global MT5 integration instance
mt5_integration = MT5Integration()

def connect_mt5(timeout: int = 30) -> Tuple[bool, Optional[str]]:
    """
    Connect to MT5 terminal

    Args:
        timeout: Connection timeout in seconds

    Returns:
        Tuple of (success, error_message)
    """
    try:
        success = mt5_integration.initialize(timeout)
        return success, None
    except MT5ConnectionError as e:
        return False, str(e)

def disconnect_mt5() -> bool:
    """
    Disconnect from MT5 terminal

    Returns:
        bool: True if successful
    """
    return mt5_integration.disconnect()

def get_mt5_account_info() -> Optional[Dict[str, Any]]:
    """
    Get MT5 account information

    Returns:
        Account info dict or None
    """
    return mt5_integration.get_account_info()

def get_mt5_connection_status() -> Dict[str, Any]:
    """
    Get MT5 connection status

    Returns:
        Status dict
    """
    return mt5_integration.get_connection_status()