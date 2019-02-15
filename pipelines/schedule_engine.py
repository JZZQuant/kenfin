from connector.auth_stack import AuthSingletonStack
from inference.symbol_factory import SymbolFactory
from pipelines.toric_pipeline import ToricPipeline
import settings

if __name__ == "__main__":
    # todo : this todo needs to go inside the pipeline object
    # while True:
        symbol_factory = SymbolFactory(settings.get_tradables())
        jobs = [symbol.symbol_action for symbol in symbol_factory.symbols]
        pipeline = ToricPipeline(settings.start_time, settings.end_time, jobs,
                                 intra_action_delta=settings.intra_action_delta,
                                 execution_heart_beat=settings.execution_heart_beat,
                                 schedule_heart_beat=settings.schedule_heart_beat)
        pipeline.trigger()
