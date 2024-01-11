import copy

from enigma.core.engine import OMSEngine
from enigma.models import (
    ContractData,
    Direction,
    Offset,
    OrderData,
    OrderRequest,
    PositionData,
    TradeData,
)


class PositionHolding:
    def __init__(self, contract: ContractData) -> None:
        self.vt_symbol = contract.vt_symbol
        self.exchange = contract.exchange

        self.active_orders: dict[str, OrderData] = {}

        self.long_pos = 0.0
        self.short_pos = 0.0

        self.long_pos_frozen = 0.0
        self.short_pos_frozen = 0.0

    def update_position(self, position: PositionData) -> None:
        if position.direction == Direction.LONG:
            self.long_pos = position.volume
        else:
            self.short_pos = position.volume

    def update_order(self, order: OrderData) -> None:
        if order.is_active():
            self.active_orders[order.vt_orderid] = order
        elif order.vt_orderid in self.active_orders:
            self.active_orders.pop(order.vt_orderid)

        self.calculate_frozen()

    def update_order_request(self, req: OrderRequest, vt_orderid: str) -> None:
        gateway_name, orderid = vt_orderid.split(".")

        order = req.create_order_data(orderid, gateway_name)
        self.update_order(order)

    def update_trade(self, trade: TradeData) -> None:
        if trade.direction == Direction.LONG:
            match trade.offset:
                case Offset.OPEN:
                    self.long_pos += trade.volume
                case Offset.CLOSE:
                    self.short_pos -= trade.volume
        else:
            match trade.offset:
                case Offset.OPEN:
                    self.short_pos += trade.volume
                case Offset.CLOSE:
                    self.long_pos -= trade.volume

        self.sum_pos_frozen()

    def calculate_frozen(self) -> None:
        self.long_pos_frozen = 0.0
        self.short_pos_frozen = 0.0

        for order in self.active_orders.values():
            if order.offset == Offset.OPEN:
                continue

            if order.offset == Offset.CLOSE:
                frozen = order.volume - order.traded  # type: ignore[operator]
                match order.direction:
                    case Direction.LONG:
                        self.short_pos_frozen += frozen
                    case Direction.SHORT:
                        self.long_pos_frozen += frozen

        self.sum_pos_frozen()

    def sum_pos_frozen(self) -> None:
        self.long_pos_frozen = min(self.long_pos, self.long_pos_frozen)
        self.short_pos_frozen = min(self.short_pos, self.short_pos_frozen)

    def convert_order_request(self, req: OrderRequest) -> list[OrderRequest]:
        if req.direction == Direction.LONG:
            pos_available = self.short_pos - self.short_pos_frozen
        else:
            pos_available = self.long_pos - self.long_pos_frozen

        reqs: list[OrderRequest] = []
        volume_left = req.volume

        if pos_available:
            close_volume = min(pos_available, volume_left)
            volume_left -= pos_available

            close_req = copy.copy(req)
            close_req.offset = Offset.CLOSE
            close_req.volume = close_volume
            reqs.append(close_req)

        if volume_left > 0:
            open_volume = volume_left

            open_req = copy.copy(req)
            open_req.offset = Offset.OPEN
            open_req.volume = open_volume
            reqs.append(open_req)

        return reqs


class OffsetConverter:
    def __init__(self, oms_engine: OMSEngine) -> None:
        self.holdings: dict[str, PositionHolding] = {}

        self.get_contract = oms_engine.get_contract

    def update_position(self, position: PositionData) -> None:
        if not self.is_convert_required(position.vt_symbol):
            return

        holding = self.get_position_holding(position.vt_symbol)
        holding.update_position(position)

    def update_trade(self, trade: TradeData) -> None:
        if not self.is_convert_required(trade.vt_symbol):
            return

        holding = self.get_position_holding(trade.vt_symbol)
        holding.update_trade(trade)

    def update_order(self, order: OrderData) -> None:
        if not self.is_convert_required(order.vt_symbol):
            return

        holding = self.get_position_holding(order.vt_symbol)
        holding.update_order(order)

    def update_order_request(self, req: OrderRequest, vt_orderid: str) -> None:
        if not self.is_convert_required(req.vt_symbol):
            return

        holding = self.get_position_holding(req.vt_symbol)
        holding.update_order_request(req, vt_orderid)

    def get_position_holding(self, vt_symbol: str) -> PositionHolding:
        holding = self.holdings.get(vt_symbol, None)
        if not holding:
            contract = self.get_contract(vt_symbol)
            holding = PositionHolding(contract)  # type: ignore[arg-type]
            self.holdings[vt_symbol] = holding
        return holding

    def convert_order_request(self, req: OrderRequest) -> list[OrderRequest]:
        if not self.is_convert_required(req.vt_symbol):
            return [req]

        return self.get_position_holding(req.vt_symbol).convert_order_request(req)

    def is_convert_required(self, vt_symbol: str) -> bool:
        contract = self.get_contract(vt_symbol)

        return bool(contract and not contract.net_position)
