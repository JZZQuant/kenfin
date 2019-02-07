class Symbol(object):
    def __init__(self, symbol, configurator):
        self.symbol = symbol["symbol"]
        self.configurator = configurator
        self.model = self.load_model(self.symbol)
        self.data = self.load_data(self.symbol)

    def load_model(self, symbol):
        #todo : @varun just load the model from a pkl file
        return "loaded model from pkl file"

    def symbol_action(self):
        #todo: @varun this function should hit the kite api and get the latest data and ping the mode take a decision
        #and append back the data to seld.data dataframe
        print("Symbol loaded %s" % self.symbol)

    def load_data(self, symbol):
        #todo : @varun build the self.data dataframe early in the morning
        return "loaded daily data in the morning"
