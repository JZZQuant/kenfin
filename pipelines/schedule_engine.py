from connector.tradables import tradables
from connector.auth_stack import AuthSingletonStack
from inference.symbol_factory import SymbolFactory
from pipelines.toric_pipeline import ToricPipeline

if __name__ == "__main__":
    while True:
        symbol_factory = SymbolFactory(tradables())
        jobs = [symbol.symbol_action for symbol in symbol_factory.symbols]
        pipeline = ToricPipeline((9, 30, 0), (15, 30, 0), jobs)
        pipeline.trigger()
        pipeline.clear()
        AuthSingletonStack().__reset__()
