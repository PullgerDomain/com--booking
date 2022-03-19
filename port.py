#import undetected_chromedriver.v2 as uc
from pyPullgerFootPrint.com.booking.www.pages import hotels as bookingHotelsFootPrint
from pyPullgerFootPrint.com.booking.www.pages import reviews as bookingReviewsFootPrint
from squirrels import SquairrelsCore
#from pcardext import df
#from websocket import _url

class CriticalErrorInitialization(Exception): pass

class Phantom:
    languageWeb = None;
    #driver = None;
    squirrel = None;
    
    def __init__(self, idLanguageWeb):
        self.languageWeb = LanguageWeb(idLanguageWeb);

        self.squirrel = SquairrelsCore.Squirrel('selenium')
        self.squirrel.initialize()
        self.squirrel.get('https://www.booking.com/content/about.' + self.languageWeb.id + '.html')
        
        '''
        chrome_options = uc.ChromeOptions()
        
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--user_agent=DN")
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-service-autorun')
        chrome_options.add_argument('--password-store=basic')
        
        self.driver = uc.Chrome(options=chrome_options)
        '''
        
        #url = 'https://www.booking.com/content/about.' + self.languageWeb.id + '.html';
        #self.driver.execute_script('window.location.href = "' + url + '"');
        #self.driver.get('https://www.booking.com/content/about.' + self.languageWeb.id + '.html');
    
    def close(self):
        self.squirrel.close();
        
    def setLanguage(self, inLanguage):
        inLanguageType = type(inLanguage);
        
        if inLanguageType == 'str':
            language = Language(inLanguage);
        elif  inLanguageType =='class':
            language = inLanguage;

    def getLanguageByIDName(self, idName):
        if idName == 'uk':
            return Language(idName);
    
    def getHotelByIDName(self, country, idHotelName):
        return _Hotel(self.squirrel, country, self.languageWeb, idHotelName)
    
class _Hotel:
    id = None;
    country = None;
    languageWeb = None;
    reviewCount = None;
    squirrel = None;
    
    def __init__(self, squirrel, country, languageWeb, idHotelName):
        self.country = country;
        self.languageWeb = languageWeb;
        self.id = idHotelName;
        self.squirrel = squirrel;
        
        url = 'https://www.booking.com/hotel/' + country.id + '/' + idHotelName + '.' + languageWeb.id + '.html';
        #self.driver.execute_script('window.location.href = "' + url + '"');
        #driver.get('https://www.booking.com/hotel/' + country.id + '/' + idHotelName + '.' + languageWeb.id + '.html');
        self.squirrel.get(url)
        self.reviewCount = bookingHotelsFootPrint.getReviewCount(self.squirrel);

    def fetchReviews(self):
        return FetchReview(self.squirrel, self);

class Review:
    hotel = None
    userName = None;
    uuid_reviews = None;
    post_date = None;
    rate = None;
    review_good = None;
    review_good_lang = None;
    review_bad = None;
    review_bad_lang = None;
    
    _squirrel = None;
    _url = None;
    _listOfReviews = None;
    
    def __init__(self, squirrel, hotel):
        self._squirrel = squirrel;
        self._url = self._squirrel.current_url;
        self.hotel = hotel;
    
    def getReviewByCountOnPage(self, countOnPage):
        if self._listOfReviews == None or self._url != self._squirrel.current_url:
            self._listOfReviews = bookingReviewsFootPrint.getListOfReviews(self._squirrel)
            self._url = self._squirrel.current_url
        
        if self._listOfReviews == None:
            return None;
        elif len(self._listOfReviews) == 0:
            return None;
        else:
            elReviews = self._listOfReviews[countOnPage];
            self.userName = elReviews["name"];
            self.uuid_reviews = elReviews["uuid_reviews"];
            self.post_date = elReviews["post_date"];
            self.rate = elReviews["rate"];
            self.review_good = elReviews["review_good"];
            self.review_good_lang = Language(elReviews["review_good_lang"]);
            self.review_bad = elReviews["review_bad"];
            self.review_bad_lang = Language(elReviews["review_bad_lang"]);

            return True;  

class FetchReview:
    squirrel = None;
    curentNum = None;
    el = None;
    _curentNumOnPagination = None;
    _countReviewOnCurentPagination = None;
    
    def __new__(cls, squirrel, hotel):
        cls.squirrel = squirrel;
        
        url = 'https://www.booking.com/reviewlist.' + hotel.languageWeb.id + '.html?cc1=' + hotel.country.id + '&pagename=' + hotel.id + ';sort=f_recent_desc';
        #cls.driver.execute_script('window.location.href = "' + url + '"');
        #cls.driver.get('https://www.booking.com/reviewlist.' + hotel.languageWeb.id + '.html?cc1=' + hotel.country.id + '&pagename=' + hotel.id + ';sort=f_recent_desc');
        cls.squirrel.get(url);

        cls._countReviewOnCurentPagination = bookingReviewsFootPrint.getCountOfReviewsElements(cls.squirrel);
        
        if cls._countReviewOnCurentPagination != 0:
            cls.el = Review(cls.squirrel, hotel);
        
        if cls.el == None:
            return None;
        else:
            return super().__new__(cls)
    '''  
    def __init__(self, driver, hotel):
        test = 1;
    '''
        
    def next(self):
        if self.curentNum == None:
            self.curentNum = 0;
            self._curentNumOnPagination = 0;
        else:
            self.curentNum += 1;
            self._curentNumOnPagination += 1;
            if (self._curentNumOnPagination + 1) > self._countReviewOnCurentPagination:
                self._curentNumOnPagination = 0;
                if bookingReviewsFootPrint.goToNextPaginationPage(self.squirrel) == True:
                    self._countReviewOnCurentPagination = bookingReviewsFootPrint.getCountOfReviewsElements(self.squirrel);
                else:
                    self.curentNum -= 1
                    return False;
         
        resultStatus = self.el.getReviewByCountOnPage(self._curentNumOnPagination);
        
        if resultStatus != True:
            raise Exception('Error in Fetch-Next');
        
        return True;

class Country:
    id = None;
    idCountryISO = None;
    
    def __init__(self, idCountryISO):
        self.id = idCountryISO;
        self.idCountryISO = idCountryISO;

class LanguageWeb:
    id = None;
    link = None;
    
    def __init__(self, idLanguageWebName):
        self.id = idLanguageWebName;
        self.link = self;
        
class Language:
    idLanguageISO = None;
    
    def __init__(self, idLanguageISO):
        self.idLanguageISO = idLanguageISO;
        
    def __str__(self):
        if self.idLanguageISO == None:
            return "";
        else: 
            return self.idLanguageISO

def bb(a,b):
    return a + b;

#test = Hotel("df");
