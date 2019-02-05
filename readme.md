Install one of the below drivers or download driver to a locaiton  
brew install geckodriver  
brew cask install phantomjs  
brew cask install chromedriver  (prefered)  
for using selenium on mac/linux  
or  
download chromedriver from https://chromedriver.storage.googleapis.com/index.html?path=2.46/
and pass it to systempath %path  
or  
if you cant set systempath just pass it as an argument to the configurator  
usage confirgurator:  
python configurator.py -c /Users/vapnik/downloads/chromedriver

Design Idea:  
A configurator object automatically logs into the kite web  
app without launching a browser and seamless stores a kite session  
now each configurator has a unique request , access token and userid pwd  
a service object would contain a unique configurator , random forest model  
 