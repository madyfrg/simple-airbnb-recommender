# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 17:11:58 2020

@author: madyf
"""




import pandas as pd
#import matplotlib
from fpdf import FPDF

###
class customer:
    #constructor
    def __init__(self, customer_id):
        self.id = customer_id
        
        #print("you have created an account for this customer")
    
    def get_customer_id(self):
        return self.id
    
    def set_id(self,customer_id):
        self.id = customer_id

class reviews(customer):
    #constructor
    def __init__(self, customer_id, dataframe, dataframe_2):
        customer.__init__(self,customer_id)
        self.reviews = dataframe
        self.listings = dataframe_2
        #print("you have created an account for this customer")
    
    def get_recent_city(self):
        temp = self.reviews.loc[self.reviews["reviewer_id"]==self.id]
        listing_id = temp.iloc[0,0]
        listing_df_of_id = self.listings.loc[self.listings["id"]==listing_id]
        city = listing_df_of_id.iloc[0,44]
        return city
    
    def get_listings(self):
        return self.listings
    
    def get_customer_name(self):
        temp = self.reviews.loc[self.reviews["reviewer_id"]==self.id]
        customer_name = temp.iloc[0,4]
        return customer_name
    
    def find_match(self):
        def get_customer_instances(df, _id):
            #return all the instances of a single customer (all reviews with customer id matching self.id)//entire row not just review
            customer_reviews = df.loc[df["reviewer_id"]==_id]
            return customer_reviews
        
        #two cases: one for if the person left another review, and one for if there isn't anything else
        
        
        low = 0.5
        positive = self.reviews.loc[self.reviews["vader_score"] >= low]
        #print(len(positive))
        x = get_customer_instances(positive, self.id)
        
        
        len_x = len(x)
        
        if len_x != 0:
            #print("filter from here")
            #get listing id from reviews df
            listing_id = x["listing_id"]
            listing_id = float(listing_id)
            #print(listing_id)
            
            #use that id to get correct info from listings df
            listing = self.listings.loc[self.listings["id"] == listing_id] #returns df
            #print(listing)
            #above is fine
            
            #filter to only highly reviewed
            filtered = self.listings.loc[self.listings["review_scores_rating"]>90]
            self.listings = filtered
            
            #filter market 
            market = listing.iloc[0,44]
            #market = str(market)
            #print(type(market))
            #print(type(self.listings.iloc[0,44]))
            #print(market)
            if market == "Boston":
                filtered = self.listings.loc[self.listings["market"] == "Boston"]
            elif market == "Seattle":
                filtered = self.listings.loc[self.listings["market"] == "Seattle"]
            
            self.listings = filtered
            
            
            #filter neighborhood 
            neighborhood = listing.iloc[0,38]
            filtered = self.listings.loc[self.listings["neighbourhood"]==neighborhood]
            
            if len(filtered) >0:
                self.listings = filtered
                if len(filtered) <=3:
                    return self.listings
            else:
                return self.listings
                
            #filter price
            price = listing.iloc[0,60]
            if price <100: 
                low_price = price
            else:
                low_price = price - 100
            high_price = price + 100 
            #print(low_price, high_price)
            
            filtered = self.listings.loc[self.listings["price"]>=low_price]
            filtered = filtered.loc[filtered["price"]<=high_price]
            
            if len(filtered) >0:
                self.listings = filtered
                
                if len(self.listings) <=3:
                    #print(self.listings)
                    return self.listings
            else:
                #print(self.listings) 
                return self.listings
            
            room_type = listing.iloc[0,52]
            filtered = self.listings.loc[self.listings["room_type"] == room_type]
            
            if len(filtered) >0:
                self.listings = filtered
                if len(filtered) <=3:
                    return self.listings
            else:
                return self.listings
                
            
        else:
            print("something wrong")



def best_listings(df, highest_value):
    high_df = df.loc[df["review_scores_rating"]==highest_value]
    return high_df
def worst_listings(df, lowest_value):
    low_df = df.loc[df["review_scores_rating"]==lowest_value]
    return low_df

class filtering():
    def __init__(self, listings_df):
        self.df = listings_df
        #self.choice = choice
    
    def get_listings(self):
        return self.df
    
    def filter_price(self):
        print("You will soon enter a low and high values to consider for nightly price.")
        
        absolute_low = min(self.df["price"])
        absolute_high = max(self.df["price"])
        print("The lowest value you may enter is ",absolute_low, "\nThe highest value you may enter is ", absolute_high )
        print("Enter whole number without a decimal place.")
        low = input("Enter a low value for your nightly rate. If none enter 'NA': ")
        high = input("Enter a high value for your nightly rate. If non enter 'NA': ")
        if low != "NA":
            low = int(low)
        if high != "NA":
            high=int(high)
        
        if low == "NA":
            filtered_df = self.df.loc[self.df["price"] <= high]
            self.df = filtered_df
            return self.df
        elif high == "NA":
            filtered_df = self.df.loc[self.df["price"] >= low]
            self.df = filtered_df
            return self.df
        elif low == "NA" and high=="NA":
            return self.df
        else: 
            filtered_df = self.df.loc[self.df["price"] >= low]
            filtered_df = filtered_df.loc[filtered_df["price"] <= high]
            self.df = filtered_df
            return self.df
    
    def filter_review_score(self):
        low = input("Enter the lowest review score you are okay with(0-100): ")
        low = int(low)
        filtered_df = self.df.loc[self.df["review_scores_rating"] >= low]
        self.df = filtered_df
        return self.df
    
    def filter_room_type(self):
        #get list of all different options in self.df (cant pick something not in df)
        options = self.df["room_type"].unique() # returns an array #https://chrisalbon.com/python/data_wrangling/pandas_list_unique_values_in_column/
        print("You may choose one of the following options for your room type:")
        for room in options:
            print(room)
        room_type = input("Enter one from the above list: ")
        
        filtered_df = self.df.loc[self.df["room_type"]==room_type]
        self.df = filtered_df
        return self.df
        
    def filter_super_host(self):
        print("You may search for only listings from superhosts")
        superhost = input("Enter 'Y' for only superhosts: ")
        if superhost == "Y":
            filtered_df = self.df.loc[self.df["host_is_superhost"]=="t"]
            self.df = filtered_df
            return self.df
        else:
            return self.df
    
    def filter_market(self):
        print("You may choose either Boston, Seattle, or both.")
        market = input("Enter 'B' for Boston, 'S' for Seattle, or 'both' for either city: ")
        if market=="both":
            return self.df
        elif market=="B":
            filtered_df = self.df.loc[self.df["market"]=="Boston"]
            self.df = filtered_df
            return self.df 
        elif market=="S":
            filtered_df = self.df.loc[self.df["market"]=="Seattle"]
            self.df = filtered_df
            return self.df
    
    def filter_neighborhood(self):
        options = self.df["neighbourhood_cleansed"].unique()
        print("You may choose from the following neighborhoods:")
        for option in options:
            print(option)
        nbh = input("Enter one neighborhood from the above list: ")
        
        filtered_df = self.df.loc[self.df["neighbourhood_cleansed"]==nbh]
        self.df = filtered_df
        return self.df

    def choice_loop(self):
        print("You may now continue to filter listings by various characteristics: ")
        filter_list = ["Neighborhood", "Price", "Room Type", "Review Score", "Superhosts only", "END FILTERING"]
        for i in range(0,len(filter_list)):
            print(i,  filter_list[i])
        choice = input("Enter the number corresponding to the choice you would like to make: ")
        return choice

    def check_length(self, a):
        length = len(a)
        if length == 0:
            return "back"
        elif length == 1:
            return "stop"
        else: 
            return "ask"
    
    
    def filtering_loop(self):
        choice = self.choice_loop()
        
        if choice == "0":
            y = self.df
            x = self.filter_neighborhood()
            
            if self.check_length(x) == "back":
                print("That request returned 0 results. We will return your previous results.")
                self.df = y
                return self.df
            
            elif self.check_length == "stop":
                print("That request returned 1 result. ")
                self.df = x
                return self.df
            
            elif self.check_length(x) == "ask":
                self.df = x
                print("That request returned", len(self.df), "results.")
                print("Do you want to continue filtering or stop?")
                ask = input ("Enter 'a' to continue or 'b' to stop filtering: ")
                if ask == 'a':
                    self.filtering_loop()
                elif ask == 'b':
                    return self.df
                
        elif choice == "1":
            y = self.df
            
            x = self.filter_price()
            
            if self.check_length(x) == "back":
                
                print("That request returned 0 results. We will return your previous results.")
                
                self.df = y
                return self.df
            
            elif self.check_length == "stop":
                print("That request returned 1 result.")
                self.df = x
                return self.df
            
            elif self.check_length(x) == "ask":
                self.df = x
                print("That request returned", len(self.df), "results.")
                print("Do you want to continue filtering or stop?")
                ask = input ("Enter 'a' to continue or 'b' to stop filtering: " )
                if ask == 'a':
                    self.filtering_loop()
                elif ask == 'b':
                    return self.df
                
        elif choice == "2":
            y = self.df
            
            x = self.filter_room_type()
            
            if self.check_length(x) == "back":
                
                print("That request returned 0 results. We will return your previous results.")
                
                self.df = y
                return self.df
            
            elif self.check_length == "stop":
                print("That request returned 1 result.")
                self.df = x
                return self.df
            
            elif self.check_length(x) == "ask":
                self.df = x
                print("That request returned", len(self.df), "results.")
                print("Do you want to continue filtering or stop?")
                ask = input ("Enter 'a' to continue or 'b' to stop filtering: " )
                if ask == 'a':
                    self.filtering_loop()
                elif ask == 'b':
                    return self.df
        
        elif choice == "2":
            y = self.df
            
            x = self.filter_room_type()
            
            if self.check_length(x) == "back":
                
                print("That request returned 0 results. We will return your previous results.")
                
                self.df = y
                return self.df
            
            elif self.check_length == "stop":
                print("That request returned 1 result.")
                self.df = x
                return self.df
            
            elif self.check_length(x) == "ask":
                self.df = x
                print("That request returned", len(self.df), "results.")
                print("Do you want to continue filtering or stop?")
                ask = input ("Enter 'a' to continue or 'b' to stop filtering: " )
                if ask == 'a':
                    self.filtering_loop()
                elif ask == 'b':
                    return self.df
        
        elif choice == "3":
            y = self.df
            
            x = self.filter_review_score()
            
            if self.check_length(x) == "back":
                
                print("That request returned 0 results. We will return your previous results.")
                
                self.df = y
                return self.df
            
            elif self.check_length == "stop":
                print("That request returned 1 result.")
                self.df = x
                return self.df
            
            elif self.check_length(x) == "ask":
                self.df = x
                print("That request returned", len(self.df), "results.")
                print("Do you want to continue filtering or stop?")
                ask = input ("Enter 'a' to continue or 'b' to stop filtering: " )
                if ask == 'a':
                    self.filtering_loop()
                elif ask == 'b':
                    return self.df
        
        elif choice == "4":
            y = self.df
            
            x = self.filter_super_host()
            
            if self.check_length(x) == "back":
                
                print("That request returned 0 results. We will return your previous results.")
                
                self.df = y
                return self.df
            
            elif self.check_length == "stop":
                print("That request returned 1 result.")
                self.df = x
                return self.df
            
            elif self.check_length(x) == "ask":
                self.df = x
                print("That request returned", len(self.df), "results.")
                print("Do you want to continue filtering or stop?")
                ask = input ("Enter 'a' to continue or 'b' to stop filtering: " )
                if ask == 'a':
                    self.filtering_loop()
                elif ask == 'b':
                    return self.df
        
        elif choice == "5":
            return self.df


# https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
class PDF(FPDF):
    def header(self):
        # Logo
        self.image(r'C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\airbnblogo.png', 90, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        #self.cell(30, 10, 'Recommended Listings', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


###

reviews_df = pd.read_csv(r"clean_reviews_df.csv")
listings_df = pd.read_csv(r"both_listings.csv")


what_step = input("Enter 'S' to obtain a summary of reviews, 'M' to create a marketing email, or 'C' to act as a customer and find a listing: ")    
if what_step == "S":
    what_city = input("what city do you want a summary for? 'S'= seattle, 'B'=boston, 'both'=both combined: ")
    if what_city == "S":
        mini_df = listings_df.loc[listings_df["market"]=="Seattle"]
        data = mini_df["review_scores_rating"]
        #remove NA
        data = data.dropna()
        
        #matplotlib.pyplot.boxplot(data, notch=None, vert=None, patch_artist=None, widths=None)
        
        max_review = max(data)
        highest_reviews = best_listings(mini_df, max_review)
        print("\n")
        print("the highest review rating was: ", max_review)
        print("there were", len(highest_reviews), "listings with this review rating score")
        print("\n")
        
        min_review = min(data)
        lowest_reviews = worst_listings(mini_df, min_review)
        print("the lowest review rating was: ", min_review)
        print("the listing(s) with this review was: \n", lowest_reviews.iloc[:,0])
        
    elif what_city == "B":
        mini_df = listings_df.loc[listings_df["market"]=="Boston"]
        data = mini_df["review_scores_rating"]
        #remove NA
        data = data.dropna()
        
       # matplotlib.pyplot.boxplot(data, notch=None, vert=None, patch_artist=None, widths=None)
        
        max_review = max(data)
        highest_reviews = best_listings(mini_df, max_review)
        print("\n")
        print("the highest review rating was: \n", max_review)
        print("there were", len(highest_reviews), "listings with this review rating score")
        print("\n")
        
        min_review = min(data)
        lowest_reviews = worst_listings(mini_df, min_review)
        print("the lowest review rating was: ", min_review)
        print("the listing(s) with this review was: ", lowest_reviews.iloc[:,0])
    
    elif what_city == "both":
        
        data = listings_df["review_scores_rating"]
        #remove NA
        data = data.dropna()
        
       # matplotlib.pyplot.boxplot(data, notch=None, vert=None, patch_artist=None, widths=None)
        
        max_review = max(data)
        highest_reviews = best_listings(listings_df, max_review)
        print("\n")
        print("the highest review rating was: ", max_review)
        print("there were", len(highest_reviews), "listings with this review rating score")
        print("\n")
        
        min_review = min(data)
        lowest_reviews = worst_listings(listings_df, min_review)
        print("the lowest review rating was: ", min_review)
        print("the listing(s) with this review was: \n", lowest_reviews.iloc[:,0])
elif what_step == "M":
    print("we will now create a marketing email")
    customer_id = input("Enter the id of the customer you would like to create an email for: ")
    customer_id = int(customer_id)
    
    
    find_airbnb = reviews(customer_id,reviews_df, listings_df)
    
    customer_name = find_airbnb.get_customer_name()
    city = find_airbnb.get_recent_city()
    
    find_airbnb.find_match()
    
    x = find_airbnb.get_listings()
    #just take random 3 of them
    # Instantiation of inherited class
    

    
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(1,10,"Hi " +customer_name+"!", 0,1)
    pdf.cell(2,10,"Based on your recent trip to "+city+", here are three more listings we think you'll love. ", 0,1)
    pdf.cell(3,10,"First ", 0,1)
    #listing name
    pdf.cell(3,10, "Listing name: " + x.iloc[0,4],0,1)
    # listing link
    pdf.cell(4,10,"Link:" + x.iloc[0,1],0,1)
    #image
    #url = x.iloc[0,17]
    #pdf.image(url, 10, 5)
    pdf.cell(2,10,"Second Listing ", 0,1)
    #listing name
    pdf.cell(3,10, "Listing name: " + x.iloc[1,4],0,1)
    # listing link
    pdf.cell(4,10,"Link:" + x.iloc[1,1],0,1)
    #
    pdf.cell(2,10,"Third Listing ", 0,1)
    #listing name
    pdf.cell(3,10, "Listing name: " + x.iloc[2,4],0,1)
    # listing link
    pdf.cell(4,10,"Link:" + x.iloc[2,1],0,1)
    
    pdf.cell(4,10,"Book soon before they go!",0,1)

    pdf.output(r'C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\marketing_email.pdf', 'F') 
    
    
elif what_step =="C":
    find_me_airbnb = filtering(listings_df)
    print("This tool was developped to help you find the perfect destination for your next stay.")
    print("To begin, you may choose either Seattle, Boston, or either.")
    find_me_airbnb.filter_market()
    #choice = find_me_airbnb.choice_loop()
    find_me_airbnb.filtering_loop()
    #print(x)
    #print(find_me_airbnb.get_listings())
    x = find_me_airbnb.get_listings()
    length = len(x)
    if length > 3: 
        print("This program will only return information for up to 3 listings.")
        print("We will randomly select 3 listings that meet your criteria.")
        
    else: 
        print("This program has found", length, "airbnb listings that meet your criteria.")

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(1,10,"Here are the top three listings that match your search. ", 0,1)
    pdf.cell(2,10,"First listing ", 0,1)
    #listing name
    pdf.cell(3,10, "Listing name: " + x.iloc[0,4],0,1)
    # listing link
    pdf.cell(4,10,"Link:" + x.iloc[0,1],0,1)
    #image
    #url = x.iloc[0,17]
    #pdf.image(url, 10, 5)
    pdf.cell(2,10,"Second Listing ", 0,1)
    #listing name
    pdf.cell(3,10, "Listing name: " + x.iloc[1,4],0,1)
    # listing link
    pdf.cell(4,10,"Link:" + x.iloc[1,1],0,1)
    #
    pdf.cell(2,10,"Third Listing ", 0,1)
    #listing name
    pdf.cell(3,10, "Listing name: " + x.iloc[2,4],0,1)
    # listing link
    pdf.cell(4,10,"Link:" + x.iloc[2,1],0,1)
    pdf.output(r'C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\customer.pdf', 'F') 
        
else:
    print("invalid input")
